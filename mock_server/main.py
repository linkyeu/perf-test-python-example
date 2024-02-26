from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Dict, Union, Optional

from pydantic import BaseModel

app = FastAPI()

# In-memory storage for books, using dictionary for simplicity
# Structure: {book_id: {"title": title, "author": author, ...}}
_books_storage = {}


class Book(BaseModel):
    id: str
    title: str
    author: str
    description: Optional[str] = None


def get_books_storage() -> Dict[str, Book]:
    global _books_storage
    return _books_storage


def books_storage() -> Dict[str, Book]:
    return get_books_storage()


@app.post('/addBook')
async def add_book(book: Book, books: Dict[str, Book] = Depends(books_storage)):
    if book.id in books:
        raise HTTPException(status_code=400, detail="Book already exists")
    books[book.id] = book
    return {"message": "Book added successfully", "book": book}


@app.delete('/deleteBook')
async def delete_book(
    books: Dict[str, Book] = Depends(books_storage),
    book_id: str = Query(..., alias='id')
):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    del books[book_id]
    return {"message": "Book deleted successfully"}


@app.get('/books', response_model=Union[List, List[Book]])
async def get_books(books: Dict[str, Book] = Depends(books_storage)):
    return list(books.values())


@app.get('/viewBookByID', response_model=Book)
async def view_book_by_id(
    books: Dict[str, Book] = Depends(books_storage),
    book_id: str = Query(..., alias='id')
):
    book = books.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
