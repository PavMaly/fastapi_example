import typing

from databases import Database
from databases.interfaces import Record
from fastapi import HTTPException

from app.common.logger import log_error_with_traceback
from app.db.database import database


class DataBaseExecuteException(Exception):
    pass


class DBExecutor:

    def __init__(self, db: Database):
        self.db = db

    async def fetch_one(self, query: str, values: dict | None = None) -> typing.Optional[Record]:
        try:
            return await self.db.fetch_one(query=query, values=values)
        except DataBaseExecuteException as e:
            log_error_with_traceback(e)
            raise HTTPException(status_code=500)

    async def fetch_all(self, query: str, values: dict | None = None) -> typing.List[Record]:
        try:
            return await self.db.fetch_all(query=query, values=values)
        except DataBaseExecuteException as e:
            log_error_with_traceback(e)
            raise HTTPException(status_code=500)

    async def execute(self, query: str, values: dict | None = None) -> typing.Any:
        try:
            return await self.db.execute(query=query, values=values)
        except DataBaseExecuteException as e:
            log_error_with_traceback(e)
            raise HTTPException(status_code=500)


db_executor = DBExecutor(database)
