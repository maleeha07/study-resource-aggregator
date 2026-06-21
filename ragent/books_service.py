import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")


def fetch_top_books(topic: str, max_results: int = 5):
    """
    Fetch up to 5 relevant books for a user topic.
    """

    url = "https://www.googleapis.com/books/v1/volumes"

    params = {
        "q": topic,
        "maxResults": min(max_results, 5),
        "orderBy": "relevance"
    }

    if GOOGLE_BOOKS_API_KEY:
        params["key"] = GOOGLE_BOOKS_API_KEY

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return []

        data = response.json()

        books = []

        for item in data.get("items", [])[:5]:
            volume = item.get("volumeInfo", {})

            title = volume.get("title", "Unknown Book")
            authors = ", ".join(
                volume.get("authors", ["Unknown Author"])
            )

            books.append({
                "title": title,
                "author": authors,
                "link": volume.get(
                    "previewLink",
                    "https://books.google.com"
                )
            })

        return books

    except Exception as e:
        print(f"[Books Service Error]: {e}")
        return []