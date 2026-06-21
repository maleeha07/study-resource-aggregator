import requests

def get_books(topic, max_results=5):
    """
    Fetches books related to a topic from Open Library.
    Returns a list of dicts with title, author, and link.
    """
    url = "https://openlibrary.org/search.json"
    params = {
        "q": topic,
        "limit": max_results
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "docs" not in data:
        print("Open Library API error:", data)
        return []

    books = []
    for doc in data["docs"]:
        title = doc.get("title", "Unknown title")
        authors = doc.get("author_name", ["Unknown author"])
        author = authors[0] if authors else "Unknown author"
        book_key = doc.get("key", "")
        link = f"https://openlibrary.org{book_key}"

        books.append({
            "title": title,
            "author": author,
            "link": link
        })

    return books


# Test it directly
if __name__ == "__main__":
    results = get_books("React")
    for b in results:
        print(b)