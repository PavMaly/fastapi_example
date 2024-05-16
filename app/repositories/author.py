
from app.api.schemas.author import Author, AuthorResponse
from app.common.logger import log
from app.db.db_executor import db_executor


@log
async def find_author(author: Author) -> AuthorResponse | None:
    author_full_name = f'{author.last_name} {author.first_name}'
    query = 'SELECT author_id, author FROM authors ' \
            'WHERE author = :author ;'
    values = {'author': author_full_name}
    author = await db_executor.fetch_one(query, values)
    if author:
        return AuthorResponse(**author)


@log
async def create_author(author: Author) -> int:
    author_full_name = f'{author.last_name} {author.first_name}'
    query = 'INSERT INTO authors(author) VALUES (:author) RETURNING author_id;'
    values = {'author': author_full_name}
    return await db_executor.execute(query, values)


@log
async def new_book_authors(authors: list[Author]) -> list[int]:
    book_authors_id = []
    for author in authors:
        author_id = await find_author(author)
        if not author_id:
            new_author = await create_author(author)
            book_authors_id.append(new_author)
        if author_id:
            book_authors_id.append(author_id)
    return book_authors_id

