"""
Multi-Judge Scorer - Evaluate AI responses using multiple judge models
"""

from inspect_ai.scorer import scorer, Score, accuracy, stderr
from inspect_ai.model import get_model, ChatMessageUser
from inspect_ai.solver import TaskState
from typing import List, Dict, Any, Set
from urllib.parse import urlparse
import json
import re


def extract_json(text: str) -> Dict[str, Any]:
    """Extract JSON from text, handling various formats."""
    
    if not text:
        return None
    
    # Try direct JSON parsing
    try:
        return json.loads(text)
    except:
        pass
    
    # Try extracting from markdown code blocks
    patterns = [
        r'```json\s*(.*?)\s*```',
        r'```\s*(.*?)\s*```',
        r'\{.*\}',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            try:
                return json.loads(match)
            except:
                continue
    
    return None


def create_empty_response() -> Dict[str, Any]:
    """Create an empty response structure for failed extractions."""
    return {
        "prospects": [
            {"name": "Matthew Christy", "first_line": "", "evidence_url": "", "evidence_quote": ""},
            {"name": "Isaac Reback", "first_line": "", "evidence_url": "", "evidence_quote": ""},
            {"name": "Tiffany Porter", "first_line": "", "evidence_url": "", "evidence_quote": ""}
        ]
    }


def extract_tool_usage_from_state(state: TaskState) -> Dict[str, Any]:
    """Extract which tools were used and what URLs were visited from message history."""
    
    tool_usage = {
        "tavily_search": [],
        "tavily_extract": [],
        "all_visited_urls": set()
    }
    
    # Scan all messages for tool calls
    if hasattr(state, 'messages'):
        for message in state.messages:
            if hasattr(message, 'tool_calls') and message.tool_calls:
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function if hasattr(tool_call, 'function') else None
                    
                    if tool_name:
                        if tool_name == "tavily_search":
                            if hasattr(tool_call, 'arguments'):
                                query = tool_call.arguments.get('query', '')
                                tool_usage["tavily_search"].append(query)
                                
                        elif tool_name == "tavily_extract":
                            if hasattr(tool_call, 'arguments'):
                                url = tool_call.arguments.get('url', '')
                                if url:
                                    tool_usage["tavily_extract"].append(url)
                                    tool_usage["all_visited_urls"].add(url.lower())
    
    return tool_usage


def check_url_verified(evidence_url: str, visited_urls: Set[str]) -> bool:
    """Check if an evidence URL was actually visited by tavily_extract."""
    
    if not evidence_url:
        return False
    
    # Normalize URL for comparison
    normalized_url = evidence_url.lower().strip()
    
    # Check exact match
    if normalized_url in visited_urls:
        return True
    
    # Check if any visited URL contains the domain of the evidence URL
    try:
        evidence_domain = urlparse(evidence_url).netloc.lower()
        for visited in visited_urls:
            visited_domain = urlparse(visited).netloc.lower()
            if evidence_domain and visited_domain and evidence_domain == visited_domain:
                return True
    except:
        pass
    
    return False


# Judge prompt template
JUDGE_PROMPT_TEMPLATE = """
You're evaluating personalized first lines for {company} prospects.

VERIFICATION STATUS FROM SYSTEM:
{verification_report}

Scoring Criteria:
1. {pain_recognition} (35%) - Does it hit a real pain point?
2. Prospect-Specific Insight (30%) - Verifiable, non-obvious details
3. {company} Fit (25%) - Natural connection to value prop
4. Reply Test (10%) - Would they actually reply?

IMPORTANT: 
- If a URL was NOT verified (model didn't use tavily_extract), heavily penalize the insight score
- Only give high scores to claims backed by VERIFIED evidence

Evaluate ALL 3 prospects below:

{prospects_details}

Output JSON only with scores for all 3 prospects:
{{
  "prospects": [
    {{
      "name": "{prospect1_name}",
      "pain_score": 0-10,
      "insight_score": 0-10,
      "fit_score": 0-10,
      "reply_score": 0-10,
      "total": 0-40,
      "rationale": "Brief explanation"
    }},
    {{
      "name": "{prospect2_name}",
      "pain_score": 0-10,
      "insight_score": 0-10,
      "fit_score": 0-10,
      "reply_score": 0-10,
      "total": 0-40,
      "rationale": "Brief explanation"
    }},
    {{
      "name": "{prospect3_name}",
      "pain_score": 0-10,
      "insight_score": 0-10,
      "fit_score": 0-10,
      "reply_score": 0-10,
      "total": 0-40,
      "rationale": "Brief explanation"
    }}
  ]
}}
"""


@scorer(metrics=[accuracy(), stderr()])
def multi_judge_scorer_batch_verified(
    judge_models: List[str] = None,
    company_context: Dict[str, str] = None
):
    """Multi-judge scoring with verification tracking from tool usage"""
    
    if judge_models is None:
        judge_models = [
            "openrouter/google/gemini-2.5-pro",
            "openrouter/moonshotai/kimi-k2",
            "openrouter/openai/gpt-5-mini",
            "openrouter/anthropic/claude-opus-4.1"
        ]
    
    if company_context is None:
        company_context = {
            "company": "Unknown",
            "pain_focus": "Pain Recognition"
        }
    
    async def score(state: TaskState, target: Any) -> Score:
        """Score the model's response with real verification tracking."""
        
        # Extract actual tool usage from state
        tool_usage = extract_tool_usage_from_state(state)
        visited_urls = tool_usage["all_visited_urls"]
        
        # Parse model response
        response_text = ""
        if hasattr(state, 'output') and hasattr(state.output, 'completion'):
            response_text = state.output.completion
        else:
            response_text = str(state.messages[-1].content if state.messages else "")
        
        # Use robust JSON extraction
        response = extract_json(response_text)
        
        # If extraction failed, check if model used tools
        if response is None:
            if len(tool_usage.get("tavily_search", [])) > 0 or len(tool_usage.get("tavily_extract", [])) > 0:
                response = create_empty_response()
                print(f"Warning: Model used tools but produced invalid JSON. Using empty response.")
            else:
                return Score(
                    value=0.0,
                    answer="",
                    explanation=f"Invalid JSON output and no tool usage detected"
                )
        
        # Verify structure
        if "prospects" not in response or not isinstance(response["prospects"], list):
            return Score(
                value=0.0,
                answer="",
                explanation="Response missing 'prospects' array"
            )
        
        # Check verification for each prospect
        verification_results = []
        verification_report_lines = []
        
        for i, prospect_response in enumerate(response.get("prospects", [])):
            evidence_url = prospect_response.get("evidence_url", "")
            prospect_name = prospect_response.get("name", f"Prospect {i+1}")
            
            # Check if this URL was actually visited
            was_verified = check_url_verified(evidence_url, visited_urls)
            
            verification_result = {
                "prospect": prospect_name,
                "evidence_url": evidence_url,
                "verified": was_verified,
                "visited_urls": list(visited_urls)
            }
            verification_results.append(verification_result)
            
            # Build report for judges
            if was_verified:
                verification_report_lines.append(
                    f"✅ {prospect_name}: URL VERIFIED (model used tavily_extract on {evidence_url})"
                )
            else:
                verification_report_lines.append(
                    f"❌ {prospect_name}: NOT VERIFIED (model did NOT use tavily_extract on {evidence_url})"
                )
        
        verification_report = "\n".join(verification_report_lines)
        
        # Add tool usage summary
        verification_report += f"\n\nTool Usage Summary:"
        verification_report += f"\n- Tavily searches: {len(tool_usage['tavily_search'])}"
        verification_report += f"\n- Tavily extracts: {len(tool_usage['tavily_extract'])}"
        all_url_verifications = tool_usage['tavily_extract']
        if all_url_verifications:
            verification_report += f"\n- URLs verified: {', '.join(all_url_verifications[:3])}..."
        else:
            verification_report += "\n- No URLs verified!"
        
        # Prepare prospects details for judges
        prospects_details = ""
        prospect_names = []
        all_expected_names = ["Matthew Christy", "Isaac Reback", "Tiffany Porter"]
        
        for i in range(3):  # Always iterate through 3 prospects
            if i < len(response.get("prospects", [])):
                prospect_response = response.get("prospects", [])[i]
                prospect_name = prospect_response.get("name", all_expected_names[i])
                first_line = prospect_response.get("first_line", "")
                evidence_url = prospect_response.get("evidence_url", "")
                
                # Check verification status
                verification_status = "❌ NOT VERIFIED"
                if i < len(verification_results):
                    verification_status = verification_results[i]['verified'] and '✅ VERIFIED' or '❌ NOT VERIFIED'
            else:
                prospect_name = all_expected_names[i] if i < len(all_expected_names) else f"Prospect {i+1}"
                first_line = "[NO RESPONSE PROVIDED]"
                evidence_url = ""
                verification_status = "❌ MISSING"
            
            prospect_names.append(prospect_name)
            prospects_details += f"""
Prospect {i+1}: {prospect_name}
First Line: {first_line}
Evidence URL: {evidence_url}
VERIFICATION: {verification_status}

"""
        
        # Collect judge scores
        all_judge_scores = []
        
        for judge_model in judge_models:
            try:
                model = get_model(judge_model)
                
                # Format judge prompt with verification status
                judge_prompt = JUDGE_PROMPT_TEMPLATE.format(
                    company=company_context.get("company", "the company"),
                    pain_recognition=company_context.get("pain_focus", "Pain Recognition"),
                    verification_report=verification_report,
                    prospects_details=prospects_details,
                    prospect1_name=prospect_names[0],
                    prospect2_name=prospect_names[1],
                    prospect3_name=prospect_names[2]
                )
                
                # Generate judge response
                judge_response = await model.generate(
                    [ChatMessageUser(content=judge_prompt)]
                )
                
                # Parse judge scores
                judge_score_text = judge_response.completion
                
                # Handle JSON in markdown blocks
                json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', judge_score_text, re.DOTALL)
                if json_match:
                    judge_scores = json.loads(json_match.group(1))
                else:
                    judge_scores = json.loads(judge_score_text)
                
                # Apply penalty for unverified claims
                for i, prospect_score in enumerate(judge_scores.get("prospects", [])):
                    if i < len(verification_results) and not verification_results[i]["verified"]:
                        # Penalize insight score if not verified
                        prospect_score["insight_score"] = min(2, prospect_score.get("insight_score", 0))
                        # Recalculate total
                        prospect_score["total"] = sum([
                            prospect_score.get("pain_score", 0),
                            prospect_score.get("insight_score", 0),
                            prospect_score.get("fit_score", 0),
                            prospect_score.get("reply_score", 0)
                        ])
                
                all_judge_scores.append({
                    "model": judge_model,
                    "scores": judge_scores
                })
                
            except Exception as e:
                print(f"Judge {judge_model} failed: {str(e)}")
                all_judge_scores.append({
                    "model": judge_model,
                    "error": str(e)
                })
        
        # Calculate median scores for each prospect
        prospect_scores = []
        for i in range(len(prospect_names)):
            scores_for_prospect = []
            for judge_result in all_judge_scores:
                if "scores" in judge_result and "prospects" in judge_result["scores"]:
                    if i < len(judge_result["scores"]["prospects"]):
                        scores_for_prospect.append(
                            judge_result["scores"]["prospects"][i].get("total", 0)
                        )
            
            if scores_for_prospect:
                sorted_scores = sorted(scores_for_prospect)
                median_idx = len(sorted_scores) // 2
                if len(sorted_scores) % 2 == 0:
                    median_score = (sorted_scores[median_idx-1] + sorted_scores[median_idx]) / 2
                else:
                    median_score = sorted_scores[median_idx]
            else:
                median_score = 0
            
            # Check verification
            verified = False
            if i < len(verification_results):
                verified = verification_results[i]["verified"]
            
            prospect_scores.append({
                "name": prospect_names[i],
                "median_score": median_score,
                "normalized": median_score / 40.0,
                "verified": verified
            })
        
        # Calculate overall score
        task_average = sum(p["normalized"] for p in prospect_scores) / len(prospect_scores) if prospect_scores else 0
        verification_rate = sum(1 for p in prospect_scores if p["verified"]) / len(prospect_scores) if prospect_scores else 0
        
        return Score(
            value=task_average,
            answer=json.dumps(response.get("prospects", []), indent=2),
            explanation=f"Score: {task_average:.3f}, Verification: {verification_rate:.1%} ({sum(1 for v in verification_results if v['verified'])}/3 verified)",
            metadata={
                "prospect_scores": prospect_scores,
                "judge_responses": all_judge_scores,
                "verification_results": verification_results,
                "tool_usage": {
                    "tavily_searches": len(tool_usage["tavily_search"]),
                    "tavily_extracts": len(tool_usage["tavily_extract"]),
                    "urls_verified": list(tool_usage["tavily_extract"])
                },
                "task_average": task_average,
                "verification_rate": verification_rate
            }
        )
    
    return score


class MultiJudgeScorer:
    """Wrapper class for multi-judge scoring"""
    
    def __init__(self, judge_models: List[str] = None):
        self.judge_models = judge_models or [
            "openrouter/google/gemini-2.5-pro",
            "openrouter/moonshotai/kimi-k2",
            "openrouter/openai/gpt-5-mini",
            "openrouter/anthropic/claude-opus-4.1"
        ]
    
    def score(self, result: Any, verbose: bool = False) -> Dict[str, Any]:
        """Score a result using the multi-judge panel"""
        # This would integrate with the scorer function above
        # Placeholder for actual implementation
        return {
            "final_score": 0.0,
            "cost": 0.0,
            "breakdown": {
                "Engineering Pain": 0.0,
                "Prospect Insight": 0.0,
                "Product Fit": 0.0,
                "Reply Probability": 0.0
            }
        }