from typing import Union

from mock_server.main import Book
from tests.config import cfg
from tests.helpers.api_request import APIClient, Response


class BaseClient:
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }


class Reader(BaseClient):
    # Domain Specific Language (Domain Driven Design) pattern:
    # https://www.selenium.dev/documentation/test_practices/encouraged/domain_specific_language/
    def __init__(self):
        super().__init__()

        self.base_url = cfg.api_host
        self.request = APIClient()

    async def add_book(self, book: Book) -> Response:
        return await self.request.post(
            url=f"{self.base_url}/addBook",
            payload=book.dict(),
            headers=self.headers,
        )

    async def delete_book(self, book_id: int) -> Response:
        return await self.request.delete(
            url=f"{self.base_url}/deleteBook",
            params={"id": book_id},
        )

    async def get_all_books(self) -> Response:
        return await self.request.get(url=f"{self.base_url}/books")

    async def get_book_by_id(self, book_id: int) -> Response:
        return await self.request.get(
            url=f"{self.base_url}/viewBookByID",
            params={"id": book_id},
        )
