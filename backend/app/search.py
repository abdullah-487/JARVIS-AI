from tavily import TavilyClient
from app.config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)


def search_web(query: str, max_results: int = 5):
    try:
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results
        )

        results = []

        for item in response.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", "")
            })

        return results

    except Exception as e:
        print(f"Tavily search error: {e}")
        return []
