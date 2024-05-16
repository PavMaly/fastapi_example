from pydantic import BaseModel

ID_NO_AUTHOR = 1


class Authority(BaseModel):
    book_id: int
    author_id: int
