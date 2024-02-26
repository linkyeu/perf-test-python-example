"""
Note:
    WHy I don't test that for example a book is really deleted from a storage ?
    Because in API we're mostly testing communication via REST-API.
    Functionally related to adding, delete items from stage are testing in
    unit tests.
    That is also a reason why I rely on fixtures which used API calls.
"""

import httpx
import pytest
from assertpy import assert_that

from tests.config import endpoint
from mock_server.main import app


@pytest.mark.api
@pytest.mark.asyncio
async def test_add_new_book(given_clean_storage, test_book):
    async with httpx.AsyncClient() as client:
        test_book = test_book.dict()
        response = await client.post(endpoint.ADD, json=test_book)

        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()).contains_entry(
            {"message": "Book added successfully"},
            {"book": test_book},
        )


@pytest.mark.api
@pytest.mark.asyncio
async def test_add_existing_book(given_storage_with_book, test_book):
    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint.ADD, json=test_book.dict())

        assert_that(response.status_code).is_equal_to(400)
        assert_that(response.json()).is_equal_to({"detail": "Book already exists"})


@pytest.mark.api
@pytest.mark.asyncio
async def test_delete_existing_book(given_storage_with_book):
    async with httpx.AsyncClient() as client:
        response = await client.delete(endpoint.DELETE, params={"id": "1"})

        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()).is_equal_to(
            {"message": "Book deleted successfully"})


@pytest.mark.api
@pytest.mark.asyncio
async def test_delete_not_existing_book(given_clean_storage):
    async with httpx.AsyncClient() as client:
        response = await client.delete(endpoint.DELETE, params={"id": "1"})

    assert_that(response.status_code).is_equal_to(404)
    assert_that(response.json()).is_equal_to({"detail": "Book not found"})


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_books(given_storage_with_book, test_book):
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint.GET_BOOKS)

        data = response.json()
        assert_that(response.status_code).is_equal_to(200)
        assert_that(data).is_instance_of(list).is_length(1)
        assert_that(data[0]).is_equal_to(test_book.dict())


@pytest.mark.api
@pytest.mark.asyncio
async def test_view_book_not_existing_id(given_clean_storage):
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint.VIEW_BY_ID, params={"id": "1"})

        assert_that(response.status_code).is_equal_to(404)
        assert_that(response.json()).is_equal_to({"detail": "Book not found"})


@pytest.mark.api
@pytest.mark.asyncio
async def test_view_book_existing_id(given_storage_with_book, test_book):
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint.VIEW_BY_ID, params={"id": "1"})

        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()).is_equal_to(test_book.dict())


@pytest.mark.asyncio
async def test_add_and_delete_book():
    async with httpx.AsyncClient(
        app=app, base_url="http://localhost:8000"
    ) as ac:
        # Add a book
        book_data = {
            "id": "book1",
            "title": "Test Book",
            "author": "Test Author",
        }
        add_response = await ac.post("/addBook", json=book_data)
        assert_that(add_response.status_code).is_equal_to(200)
        assert_that(add_response.json()).contains_entry(
            {"message": "Book added successfully"}
        )

        # Verify book added
        get_book_response = await ac.get(f"/viewBookByID?id={book_data['id']}")
        assert_that(get_book_response.status_code).is_equal_to(200)
        assert_that(get_book_response.json()["id"]).is_equal_to(book_data["id"])

        # Delete the book
        delete_response = await ac.delete(f"/deleteBook?id={book_data['id']}")
        assert_that(delete_response.status_code).is_equal_to(200)
        assert_that(delete_response.json()).contains_entry(
            {"message": "Book deleted successfully"}
        )

        # Verify book deleted
        get_deleted_book_response = await ac.get(f"/viewBookByID?id={book_data['id']}")
        assert_that(get_deleted_book_response.status_code).is_equal_to(404)
