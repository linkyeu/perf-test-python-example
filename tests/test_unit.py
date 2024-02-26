import pytest

from assertpy import assert_that
from fastapi import HTTPException
from mock_server.main import add_book, view_book_by_id, get_books, delete_book


@pytest.mark.unit
@pytest.mark.asyncio
async def test_add_new_book(test_book, test_storage):
    response = await add_book(test_book, test_storage)

    assert_that(test_storage[test_book.id]).is_equal_to(test_book)
    assert_that(response).contains_entry(
        {"message": "Book added successfully"},
        {"book": test_book}
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_add_existing_book(test_book, test_storage):
    test_storage[test_book.id] = test_book

    with pytest.raises(HTTPException) as exc_info:
        await add_book(test_book, test_storage)

        assert_that(exc_info.value.status_code).is_equal_to(404)
        assert_that(exc_info.value.detail).is_equal_to("Book already exists")


@pytest.mark.unit
@pytest.mark.asyncio
async def test_delete_existing_book(test_storage, test_book):
    test_storage[test_book.id] = test_book

    response = await delete_book(books=test_storage, book_id="1")

    assert_that(response).is_equal_to({"message": "Book deleted successfully"})
    assert_that(test_book.id).is_not_in(test_storage)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_delete_not_existing_book(test_storage, test_book):
    with pytest.raises(HTTPException) as exc_info:
        await delete_book(test_storage, book_id="not-existing-id")

        assert_that(exc_info.value.status_code).is_equal_to(404)
        assert_that(exc_info.value.detail).is_equal_to("Book not found")


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_books(test_storage, test_book):
    response = await get_books(test_storage)
    assert_that(response).is_instance_of(list).is_length(0)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_view_book_by_existing_id(test_book_in_storage, test_book):
    response = await view_book_by_id(test_book_in_storage, book_id="1")
    assert_that(response).is_equal_to(test_book)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_view_book_by_not_existing_id(test_book_in_storage):
    with pytest.raises(HTTPException) as exc_info:
        await view_book_by_id(test_book_in_storage, book_id="not-existing-id")

        assert_that(exc_info.value.status_code).is_equal_to(404)
        assert_that(exc_info.value.detail).is_equal_to("Book not found")
