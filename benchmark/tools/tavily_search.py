"""
Tavily Search Tool - Web search for prospect research
"""

from inspect_ai.tool import tool
import os
import httpx
from typing import Dict, Any, List, Optional


@tool
def tavily_search():
    """
    Search the web using Tavily API for prospect research.
    
    Tavily provides high-quality web search results optimized for AI agents.
    It returns structured data with answers and relevant content snippets.
    
    Args:
        query: Search query string
        include_domains: Optional list of domains to restrict search to
        search_depth: "basic" (1 credit) or "advanced" (2 credits)
        
    Returns:
        Dictionary containing search results and answer
    """
    
    async def execute(
        query: str,
        include_domains: Optional[List[str]] = None,
        search_depth: str = "basic"
    ) -> Dict[str, Any]:
        """Execute Tavily search with proper authentication.
        
        Args:
            query: Search query string
            include_domains: Optional list of domains to restrict search to
            search_depth: "basic" (1 credit) or "advanced" (2 credits)
        """
        
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return {"error": "TAVILY_API_KEY not found in environment"}
        
        # Validate search_depth parameter
        if search_depth not in ["basic", "advanced"]:
            search_depth = "basic"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "api_key": api_key,  # API key goes in payload
            "query": query,
            "search_depth": search_depth,
            "max_results": 5,
            "include_answer": True,
            "include_raw_content": True,
            "topic": "general"
        }
        
        if include_domains:
            payload["include_domains"] = include_domains
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Format results for model consumption
                    results = []
                    for result in data.get("results", []):
                        results.append({
                            "url": result.get("url", ""),
                            "title": result.get("title", ""),
                            "content": result.get("content", "")[:500],  # Truncate for readability
                            "score": result.get("score", 0)
                        })
                    
                    return {
                        "answer": data.get("answer", ""),
                        "results": results,
                        "query": query
                    }
                elif response.status_code == 401:
                    return {"error": "Invalid API key - check TAVILY_API_KEY"}
                elif response.status_code == 429:
                    return {"error": "Rate limit exceeded"}
                elif response.status_code == 432:
                    return {"error": "Plan limit exceeded"}
                else:
                    return {"error": f"Search failed: {response.status_code}"}
                    
        except httpx.TimeoutException:
            return {"error": "Search request timed out"}
        except Exception as e:
            return {"error": f"Search error: {str(e)}"}
    
    return execute