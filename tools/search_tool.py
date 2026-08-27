import os
from serpapi import GoogleSearch

def search_web_for_travel(query: str) -> str:
    """
    Searches the web for live information about travel destinations.
    """
    params = {
      "q": query,
      "api_key": os.getenv("SERPAPI_KEY")
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    snippets = [res.get("snippet", "") for res in results.get("organic_results", [])[:3]]
    return " ".join(snippets)