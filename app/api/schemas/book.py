from datetime import datetime

from pydantic import BaseModel, field_validator, model_validator

from app.api.schemas.author import Author
from app.common.base_data_classes import StrippedString


class BookCreate(BaseModel):
    title: StrippedString
    publisher: StrippedString
    year: int
    authors: list[Author]
    no_authority: bool = False

    @model_validator(mode='after')
    def check_authority_skip(self):
        if not self.no_authority and self.authors == []:
            raise ValueError('Authors not defined. To create book with no authority set \'no_authority\': true.')
        if self.no_authority and self.authors:
            raise ValueError('Conflict: \'no_authority\' set true and \'authors\' field is not empty.')
        return self


    @field_validator('year')
    @classmethod
    def validate_year(cls, value: int) -> int:
        current_year = datetime.now().year
        if value < 2000:
            raise ValueError('Books published before 1980 are not accepted into the library\'s collection.')
        if value > current_year:
            raise ValueError(f'Year {value} has not yet arrived')
        return value


class BookResponse(BaseModel):
    title: str
    publisher: str
    year: int
    authors: str


class BookSearchMeta(BaseModel):
    found: int = 0


class BookSearchResponse(BaseModel):
    meta: BookSearchMeta | None = None
    books: list[BookResponse] | None = None


class BookUpdate(BaseModel):
    id: int
    title: StrippedString | None = None
    publisher: StrippedString | None = None
    year: int | None = None
    authors: list[Author] | None = None
    no_authority: bool = False

    @field_validator('year')
    @classmethod
    def validate_year(cls, value: int) -> int:
        if value is not None:
            current_year = datetime.now().year
            if value < 2000:
                raise ValueError('Books published before 1980 are not accepted into the library\'s collection.')
            if value > current_year:
                raise ValueError(f'Year {value} has not yet arrived')
            return value

    @model_validator(mode='after')
    def check_authority_skip(self):
        if self.no_authority and self.authors:
            raise ValueError('Conflict: \'no_authority\' set true and \'authors\' field is not empty.')
        return self
