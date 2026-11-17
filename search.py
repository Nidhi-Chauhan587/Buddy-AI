
from ddgs import DDGS


def search_web(query):
    try:
        search_results = DDGS().text(
            query,
            max_results=5
        )

        results = []

        for item in search_results:
            results.append({
                "title": item.get("title", ""),
                "body": item.get("body", ""),
                "url": item.get("href", "")
            })

        return results

    except Exception as e:
        print("Search error:", e)
        return []
