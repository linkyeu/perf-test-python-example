from typing import List

import pytest
import requests

from mock_server.main import Book
from tests.config import endpoint
from tests.helpers.reader import Reader


@pytest.fixture()
def test_book() -> Book:
    return Book(
        id="1",
        title="War and Piece",
        author="Tolstoy",
        description=None
    )


@pytest.fixture()
def test_books() -> List[Book]:
    Book(
        id="1",
        title="War and Piece",
        author="Tolstoy",
        description=None
    )

    return


@pytest.fixture()
def test_storage() -> dict:
    return dict()


@pytest.fixture()
def test_book_in_storage(test_book) -> dict[str, Book]:
    return {test_book.id: test_book}


def remove_all_books() -> None:
    """Hardcoded to delete book with ID=1"""
    response = requests.get(endpoint.GET_BOOKS)
    assert response.status_code == 200
    books = response.json()

    for book in books:
        response = requests.delete(endpoint.DELETE, params={"id": book["id"]})
        assert response.status_code in [404, 200]


@pytest.fixture()
def given_clean_storage() -> None:
    remove_all_books()
    yield
    remove_all_books()


@pytest.fixture()
def given_storage_with_book(test_book, given_clean_storage) -> None:
    remove_all_books()
    response = requests.post(endpoint.ADD, json=test_book.dict())
    assert response.status_code == 200
    yield
    remove_all_books()


@pytest.fixture
def reader():
    yield Reader()
