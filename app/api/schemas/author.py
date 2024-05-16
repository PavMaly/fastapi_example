from pydantic import BaseModel, field_validator

from app.common.base_data_classes import TitledString
from app.common.common import check_supported_chars


class Author(BaseModel):
    last_name: TitledString
    first_name: TitledString

    @field_validator('*')
    @classmethod
    def author_supported_chars(cls, value: TitledString) -> TitledString:
        if not check_supported_chars(value):
            raise ValueError(
                'Author\'s last name and last name must contain only russian, english or german letters')
        return value


class AuthorResponse(BaseModel):
    author_id: int
    author: str
