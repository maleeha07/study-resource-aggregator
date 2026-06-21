import unittest
from unittest.mock import Mock, patch

import books_service


class TestBooksService(unittest.TestCase):
    @patch("books_service.requests.get")
    def test_get_books_returns_parsed_book_list(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "docs": [
                {
                    "title": "Python Programming",
                    "author_name": ["Jane Doe"],
                    "key": "/works/OL12345W"
                },
                {
                    "title": "Learn Testing",
                    "author_name": ["John Smith"],
                    "key": "/works/OL67890W"
                }
            ]
        }
        mock_get.return_value = mock_response

        books = books_service.get_books("Python", max_results=2)

        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]["title"], "Python Programming")
        self.assertEqual(books[0]["author"], "Jane Doe")
        self.assertEqual(books[0]["link"], "https://openlibrary.org/works/OL12345W")
        self.assertEqual(books[1]["title"], "Learn Testing")
        self.assertEqual(books[1]["author"], "John Smith")

    @patch("books_service.requests.get")
    def test_get_books_returns_empty_list_when_docs_missing(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"error": "invalid request"}
        mock_get.return_value = mock_response

        books = books_service.get_books("Python", max_results=2)

        self.assertEqual(books, [])


if __name__ == "__main__":
    unittest.main()
