"""
Note:
    WHy I don't test that for example a book is really deleted from a storage ?
    Because in API we're mostly testing communication via REST-API.
    Functionally related to adding, delete items from stage are testing in
    unit tests.
    That is also a reason why I rely on fixtures which are used API calls.

    Here I used Domain Specific Language (Domain Driven Design) so tests are
    more readable and from user point of view instead of poor Python code
    with e.g. requests.<>.
"""
import pytest

from assertpy import assert_that
from mock_server.main import Book


@pytest.mark.api
@pytest.mark.asyncio
async def test_add_not_existing_book(given_clean_storage, reader, test_book):
    response = await reader.add_book(book=test_book)

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.as_dict).contains_entry(
            {"message": "Book added successfully"},
            {"book": test_book.dict()},
        )


@pytest.mark.api
@pytest.mark.asyncio
async def test_add_existing_book(given_storage_with_book, reader, test_book):
    response = await reader.add_book(book=test_book)

    assert_that(response.status_code).is_equal_to(400)
    assert_that(response.as_dict).is_equal_to({"detail": "Book already exists"})


@pytest.mark.api
@pytest.mark.asyncio
async def test_delete_existing_book(given_storage_with_book, reader):
    response = await reader.delete_book(book_id=1)

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.as_dict).is_equal_to(
        {"message": "Book deleted successfully"}
    )


@pytest.mark.api
@pytest.mark.asyncio
async def test_delete_not_existing_book(given_clean_storage, reader):
    response = await reader.delete_book(book_id=1)

    assert_that(response.status_code).is_equal_to(404)
    assert_that(response.as_dict).is_equal_to({"detail": "Book not found"})


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_all_books(given_storage_with_book, reader, test_book):
    response = await reader.get_all_books()

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.as_dict).is_instance_of(list).is_length(1)
    assert_that(response.as_dict[0]).is_equal_to(test_book.dict())


@pytest.mark.api
@pytest.mark.asyncio
async def test_view_not_existing_book(given_clean_storage, reader):
    response = await reader.get_book_by_id(book_id=1)

    assert_that(response.status_code).is_equal_to(404)
    assert_that(response.as_dict).is_equal_to({"detail": "Book not found"})


@pytest.mark.api
@pytest.mark.asyncio
async def test_view_existing_book(given_storage_with_book, reader, test_book):
    response = await reader.get_book_by_id(book_id=1)

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.as_dict).is_equal_to(test_book.dict())


@pytest.mark.api
@pytest.mark.asyncio
async def test_add_and_delete_book(given_clean_storage, reader):
    book_data = Book(
        id="book1",
        title="Test Book",
        author="Test Author",
    )

    response = await reader.add_book(book=book_data)
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.as_dict).contains_entry(
        {"message": "Book added successfully"}
    )

    response = await reader.get_book_by_id(book_id=book_data.id)
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.as_dict).is_equal_to(book_data.dict())

    response = await reader.delete_book(book_id=book_data.id)
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.as_dict).contains_entry(
        {"message": "Book deleted successfully"}
    )

    response = await reader.get_book_by_id(book_id=book_data.id)
    assert_that(response.status_code).is_equal_to(404)
