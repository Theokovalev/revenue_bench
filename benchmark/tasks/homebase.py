"""
Homebase Task - Evaluate AI models on B2B cold outreach personalization
"""

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message, use_tools
import json
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from tools.tavily_search import tavily_search
from tools.tavily_extract import tavily_extract
from judges.multi_judge_scorer import multi_judge_scorer_batch_verified


class HomebaseTask:
    """Homebase personalization task for evaluating AI models on B2B outreach"""
    
    def __init__(self):
        self.prompt_path = Path(__file__).parent / "prompts" / "homebase_prompt.md"
        self.load_prompt()
    
    def load_prompt(self):
        """Load task prompt from file"""
        with open(self.prompt_path, 'r') as f:
            self.prompt = f.read()
    
    def evaluate(self, model: str, verbose: bool = False):
        """Run evaluation on specified model"""
        
        # Expected response format (for reference)
        expected_response = json.dumps({
            "prospects": [
                {
                    "name": "Matthew Christy",
                    "first_line": "<personalized message>",
                    "evidence_url": "https://<source>",
                    "evidence_quote": "<optional snippet>"
                },
                {
                    "name": "Isaac Reback",
                    "first_line": "<personalized message>",
                    "evidence_url": "https://<source>",
                    "evidence_quote": "<optional snippet>"
                },
                {
                    "name": "Tiffany Porter",
                    "first_line": "<personalized message>",
                    "evidence_url": "https://<source>",
                    "evidence_quote": "<optional snippet>"
                }
            ]
        })
        
        # Create dataset with single sample (all 3 prospects)
        dataset = [
            Sample(
                input=self.prompt,
                target=expected_response
            )
        ]
        
        # Create and run task
        task = Task(
            dataset=dataset,
            solver=[
                system_message("You are an expert SDR specializing in multi-location SMB outreach."),
                use_tools([
                    tavily_search(), 
                    tavily_extract()
                ]),
                generate(max_tokens=3000)  # Sufficient for 3 responses
            ],
            scorer=multi_judge_scorer_batch_verified(
                company_context={
                    "company": "Homebase",
                    "pain_focus": "Ops/Labor Pain Recognition"
                }
            )
        )
        
        # Run evaluation (implementation depends on Inspect AI setup)
        # This would typically use inspect_ai.eval() or similar
        return self.run_task(task, model, verbose)
    
    def run_task(self, task, model, verbose):
        """Execute the task with given model"""
        # This would integrate with Inspect AI's evaluation framework
        # Placeholder for actual implementation
        try:
            from inspect_ai import eval
            result = eval(
                task,
                model=model,
                log_dir="logs/",
                log_samples=verbose
            )
            return result
        except ImportError:
            print("Note: Full Inspect AI integration required for actual evaluation")
            return None


@task
def homebase_personalization_optimized():
    """Homebase personalization task - all prospects in one call
    
    This is the original task function for direct use with Inspect AI CLI.
    """
    task_instance = HomebaseTask()
    
    dataset = [
        Sample(
            input=task_instance.prompt,
            target=json.dumps({
                "prospects": [
                    {
                        "name": "Matthew Christy",
                        "first_line": "<personalized message>",
                        "evidence_url": "https://<source>",
                        "evidence_quote": "<optional snippet>"
                    },
                    {
                        "name": "Isaac Reback",
                        "first_line": "<personalized message>",
                        "evidence_url": "https://<source>",
                        "evidence_quote": "<optional snippet>"
                    },
                    {
                        "name": "Tiffany Porter",
                        "first_line": "<personalized message>",
                        "evidence_url": "https://<source>",
                        "evidence_quote": "<optional snippet>"
                    }
                ]
            })
        )
    ]
    
    return Task(
        dataset=dataset,
        solver=[
            system_message("You are an expert SDR specializing in multi-location SMB outreach."),
            use_tools([
                tavily_search(), 
                tavily_extract()
            ]),
            generate(max_tokens=3000)
        ],
        scorer=multi_judge_scorer_batch_verified(
            company_context={
                "company": "Homebase",
                "pain_focus": "Ops/Labor Pain Recognition"
            }
        )
    )