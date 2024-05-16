from app.api.schemas.authority import Authority
from app.common.logger import log
from app.db.db_executor import db_executor


@log
async def create_authority(authority: Authority) -> None:
    query = 'INSERT INTO authority(book_id, author_id) VALUES (:book_id, :author_id);'
    values = {'book_id': authority.book_id, 'author_id': authority.author_id}
    await db_executor.execute(query, values)


@log
async def delete_authority_by_book_id(book_id: int) -> None:
    query = 'DELETE FROM authority WHERE book_id = :book_id ;'
    values = {'book_id': book_id}
    await db_executor.execute(query, values)
