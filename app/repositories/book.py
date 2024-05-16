from collections import namedtuple

from fastapi import HTTPException, Depends

from app.api.schemas.authority import Authority, ID_NO_AUTHOR
from app.common.common import GetToken
from app.common.logger import log
from app.db.db_executor import db_executor
from app.repositories.author import new_book_authors
from app.api.schemas.book import BookResponse, BookCreate, BookSearchResponse, BookSearchMeta, BookUpdate
from app.db.database import database
from app.repositories.authority import create_authority, delete_authority_by_book_id


@log
async def get_books(skip: int, limit: int) -> list[BookResponse]:
    query = 'SELECT books.book_id, title, publisher, year, STRING_AGG(author, \', \') as authors FROM books ' \
            'JOIN authority ON books.book_id = authority.book_id ' \
            'JOIN authors ON authority.author_id = authors.author_id ' \
            'GROUP BY books.book_id ORDER BY books.book_id ' \
            'LIMIT :limit OFFSET :offset ;'
    values = {'offset': skip, 'limit': limit}
    result = await db_executor.fetch_all(query, values)
    books = [BookResponse(**book) for book in result]
    return books


@log
async def get_book_by_id(book_id: int) -> BookResponse:
    query = 'SELECT books.book_id, title, publisher, year, STRING_AGG(author, \', \') as authors FROM books ' \
            'JOIN authority ON books.book_id = authority.book_id ' \
            'JOIN authors ON authority.author_id = authors.author_id ' \
            'WHERE books.book_id = :book_id ' \
            'GROUP BY books.book_id ORDER BY books.book_id;'
    values = {'book_id': book_id}
    result = await db_executor.fetch_one(query, values)
    if result:
        return BookResponse(**result)
    raise HTTPException(status_code=404, detail=f'Book with id={book_id} not found')


@log
async def book_id_exists(book_id: int) -> bool:
    query = 'SELECT book_id FROM books WHERE book_id = :book_id;'
    values = {'book_id': book_id}
    result = await db_executor.fetch_one(query, values)
    if result:
        return True
    raise HTTPException(status_code=404, detail=f'Book with id={book_id} not found')


@log
async def is_dublicate_book(book: BookCreate) -> int:
    query = 'SELECT book_id from books ' \
            'WHERE title = :title and publisher = :publisher and year = :year'
    values = {'title': book.title, 'publisher': book.publisher, 'year': book.year}
    result = await db_executor.fetch_one(query, values)
    if result:
        return result['book_id']
    return 0


@log
async def create_book(book: BookCreate) -> int:
    query = 'INSERT INTO books (title, publisher, year) ' \
            'VALUES (:title, :publisher, :year) ' \
            'RETURNING book_id;'
    values = {'title': book.title, 'publisher': book.publisher, 'year': book.year}
    result = await db_executor.execute(query, values)
    return result


@log
async def add_new_book(book: BookCreate) -> BookResponse:
    # https://www.encode.io/databases/connections_and_transactions/
    dublicate = await is_dublicate_book(book)
    if dublicate:
        dublicate_info = book.model_dump(exclude={'authors', 'no_authority'})
        raise HTTPException(status_code=409, detail=f'Book <{dublicate_info}> already exists. ID: {dublicate}.')
    async with database.transaction():
        book_authors_id = await new_book_authors(book.authors)
        new_book_id = await create_book(book)
        if book.no_authority:
            new_authority = Authority(book_id=new_book_id, author_id=ID_NO_AUTHOR)
            await create_authority(new_authority)
        else:
            for author_id in book_authors_id:
                new_authority = Authority(book_id=new_book_id, author_id=author_id)
                await create_authority(new_authority)
        new_book = await get_book_by_id(new_book_id)
    return new_book


@log
async def search_book_repo(title: str, author: str, skip: int, limit: int) -> BookSearchResponse:
    if not title and not author:
        raise HTTPException(
            status_code=400,
            detail='No search details were given. Must specify partial book title and/or partial author name.')
    query = 'SELECT books.book_id  FROM books ' \
            'JOIN authority ON books.book_id = authority.book_id ' \
            'JOIN authors ON authority.author_id = authors.author_id ' \
            'WHERE author ilike :author and title ilike :title ' \
            'GROUP BY books.book_id ORDER BY books.book_id ' \
            'LIMIT :limit OFFSET :offset ;'
    values = {'author': f'%{author}%', 'title': f'%{title}%', 'limit': limit, 'offset': skip}
    result = await db_executor.fetch_all(query, values)
    if result:
        found_books = []
        for item in result:
            book = await get_book_by_id(item.book_id)
            found_books.append(book)
        response = BookSearchResponse()
        response.meta = BookSearchMeta(found=len(found_books))
        response.books = found_books
        return response
    raise HTTPException(status_code=404, detail='No books found.')


@log
async def _update_book_title(book_id: int, title: str):
    query = ' UPDATE books SET title = :title WHERE book_id = :id ;'
    values = {'title': title, 'id': book_id}
    await db_executor.execute(query, values)


BookValue = namedtuple('BookValue', ['value_name', 'value_rate'])


@log
async def _update_book_value(book_id: int, new_value: BookValue):
    query = f' UPDATE books SET {new_value.value_name} = :value WHERE book_id = :id ;'
    values = {'value': new_value.value_rate, 'id': book_id}
    await db_executor.execute(query, values)


@log
async def update_book(book: BookUpdate):
    async with database.transaction():
        if book.title:
            book_new_title = BookValue('title', book.title)
            await _update_book_value(book.id, book_new_title)
        if book.publisher:
            book_new_publisher = BookValue('publisher', book.publisher)
            await _update_book_value(book.id, book_new_publisher)
        if book.year:
            book_new_year = BookValue('year')
            await _update_book_value(book.id, book_new_year)
        if book.authors:
            book_authors_id = await new_book_authors(book.authors)
            await delete_authority_by_book_id(book.id)
            for author_id in book_authors_id:
                new_authority = Authority(book_id=book.id, author_id=author_id)
                await create_authority(new_authority)
        if book.no_authority:
            await delete_authority_by_book_id(book.id)
            no_author_authority = Authority(book_id=book.id, author_id=ID_NO_AUTHOR)
            await create_authority(no_author_authority)



