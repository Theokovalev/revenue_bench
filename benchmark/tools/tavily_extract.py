"""
Tavily Extract Tool - Extract and verify content from URLs
"""

from inspect_ai.tool import tool
import os
import httpx
from typing import Dict, Any


@tool
def tavily_extract():
    """
    Extract content from URLs using Tavily Extract API.
    
    This tool allows models to verify claims by extracting actual content
    from web pages. It's essential for fact-checking and ensuring accurate
    personalization in outreach messages.
    
    Args:
        url: URL to extract content from
        
    Returns:
        Dictionary with extracted content and metadata
    """
    
    async def execute(url: str) -> Dict[str, Any]:
        """
        Extract content from a URL for verification.
        
        Args:
            url: The URL to extract content from
        """
        
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return {"error": "TAVILY_API_KEY not found in environment"}
        
        # Validate URL
        if not url or not url.startswith(('http://', 'https://')):
            return {"error": f"Invalid URL: {url}"}
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "api_key": api_key,
            "urls": [url],  # Extract API accepts multiple URLs
            "include_images": False,
            "include_favicon": False,
            "extract_depth": "basic",  # Use basic for cost savings
            "format": "text"  # Plain text for easier claim verification
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.tavily.com/extract",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check if extraction was successful
                    if "results" in data and len(data["results"]) > 0:
                        result = data["results"][0]
                        
                        # Check for failed extractions
                        if "failed_results" in data and url in data.get("failed_results", []):
                            return {
                                "url": url,
                                "success": False,
                                "error": "Failed to extract content from URL"
                            }
                        
                        # Return extracted content
                        content = result.get("raw_content", "")
                        return {
                            "url": url,
                            "success": True,
                            "content": content,
                            "text": content,
                            "metadata": {
                                "response_time": data.get("response_time", 0)
                            }
                        }
                    else:
                        return {
                            "url": url,
                            "success": False,
                            "error": "No content extracted"
                        }
                        
                elif response.status_code == 401:
                    return {"error": "Invalid Tavily API key"}
                elif response.status_code == 429:
                    return {"error": "Rate limit exceeded"}
                elif response.status_code == 432:
                    return {"error": "Plan limit exceeded"}
                else:
                    return {"error": f"Extract failed: {response.status_code}"}
                    
        except httpx.TimeoutException:
            return {"error": "Extract request timed out"}
        except Exception as e:
            return {"error": f"Extract error: {str(e)}"}
    
    return execute