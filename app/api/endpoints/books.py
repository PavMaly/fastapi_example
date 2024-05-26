
from fastapi import APIRouter, status, HTTPException

from app.common.common import CommonDeps, GetToken
from app.repositories.book import get_books, get_book_by_id, add_new_book, search_book_repo, book_id_exists, update_book
from app.api.schemas.book import BookCreate, BookResponse, BookSearchResponse, BookUpdate
from app.repositories.user import check_is_staff

books_route = APIRouter()


@books_route.get('/')
async def books(commons: CommonDeps) -> list[BookResponse]:
    """Show all library books."""
    return await get_books(commons.skip, commons.limit)


@books_route.get('/search')
async def search_book(commons: CommonDeps, book_title: str = '', author: str = '', ) -> BookSearchResponse:
    """Search book by partial match."""
    return await search_book_repo(book_title, author, commons.skip, commons.limit)


@books_route.post('/add', status_code=status.HTTP_201_CREATED)
async def add_book(book: BookCreate, token: str = GetToken) -> BookResponse:
    """Add a new book in library collection and return its data presentation."""
    await check_is_staff(token)
    return await add_new_book(book)


@books_route.get('/{book_id}')
async def get_book(book_id: int) -> BookResponse:
    """Find book by id."""
    if not isinstance(book_id, int):
        raise HTTPException(status_code=400, detail='book_id must be integer')
    return await get_book_by_id(book_id)


@books_route.put('/update_book')
async def update_book_info(book: BookUpdate, token: str = GetToken):
    """Update existing book info."""
    await check_is_staff(token)
    await book_id_exists(book.id)
    await update_book(book)
