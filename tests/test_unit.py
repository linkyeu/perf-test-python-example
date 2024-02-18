import pytest
from fastapi import HTTPException

from mock_server.main import add_book, view_book_by_id, get_books, delete_book


@pytest.mark.unit
@pytest.mark.asyncio
async def test_add_new_book(test_book, test_storage):
    response = await add_book(test_book, test_storage)

    assert test_storage[test_book.id] == test_book
    assert response == {"message": "Book added successfully", "book": test_book}


@pytest.mark.unit
@pytest.mark.asyncio
async def test_add_existing_book(test_book, test_storage):
    test_storage[test_book.id] = test_book

    with pytest.raises(HTTPException) as exc_info:
        await add_book(test_book, test_storage)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Book already exists"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_delete_existing_book(test_storage, test_book):
    test_storage[test_book.id] = test_book

    response = await delete_book(books=test_storage, book_id="1")

    assert response == {"message": "Book deleted successfully"}
    assert test_book.id not in test_storage


@pytest.mark.unit
@pytest.mark.asyncio
async def test_delete_not_existing_book(test_storage, test_book):
    with pytest.raises(HTTPException) as exc_info:
        await delete_book(test_storage, book_id="not-existing-id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Book not found"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_books(test_storage, test_book):
    response = await get_books(test_storage)

    assert isinstance(response, list)
    assert len(response) == 0


@pytest.mark.unit
@pytest.mark.asyncio
async def test_view_book_by_existing_id(test_book_in_storage, test_book):
    response = await view_book_by_id(test_book_in_storage, book_id="1")
    assert response == test_book


@pytest.mark.unit
@pytest.mark.asyncio
async def test_view_book_by_not_existing_id(test_book_in_storage):
    with pytest.raises(HTTPException) as exc_info:
        await view_book_by_id(test_book_in_storage, book_id="not-existing-id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Book not found"
