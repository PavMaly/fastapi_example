import re
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, field_validator, EmailStr

from app.common.base_data_classes import TitledString, StrippedString
from app.common.common import check_supported_chars

COUNTRY_PHONE_CODES = ['+7', '8']

LoginUser = Annotated[OAuth2PasswordRequestForm, Depends()]


class CurrentUser(BaseModel):
    current_user: str


class FullName(BaseModel):
    last_name: TitledString
    first_name: TitledString

    @field_validator('*')
    @classmethod
    def full_name_supported_chars(cls, value: str) -> str:
        if not check_supported_chars(value):
            raise ValueError(
                'Author\'s last name and last name must contain only russian, english or german letters')
        return value


class BaseUser(BaseModel):
    username: StrippedString
    password: StrippedString

    @field_validator('username')
    @classmethod
    def validate_username(cls, value: StrippedString) -> StrippedString:
        pattern = r'^[a-zA-Z0-9_-]+$'
        if re.match(pattern, value) is None:
            raise ValueError('Unsupported chars. Only latin letters, numbers and _ - signs are permited.')
        return value


class Address(BaseModel):
    zip_code: StrippedString
    city: TitledString
    street: StrippedString
    building: StrippedString
    apartment: StrippedString | None = None


    @field_validator('zip_code')
    @classmethod
    def check_zip_code(cls, value: StrippedString) -> StrippedString:
        value = value.strip()
        if not value.isdigit():
            raise ValueError(f'Unsupported zip code format: {value}')
        return value


class UserCreate(BaseUser):
    full_name: FullName
    email: EmailStr
    is_admin: bool
    is_librarian: bool
    phone: str | None = None
    address: Address | None = None

    @field_validator('email')
    @classmethod
    def strip_value(cls, value: str) -> str:
        return value.strip()

    @field_validator('phone')
    @classmethod
    def check_phone_number(cls, value: str) -> str:
        value = value.strip()
        supported_chars = '0123456789+'
        err = ValueError(f'Unsupported phone number format: {value}')
        if not all(char in supported_chars for char in value):
            raise err
        if '+' in value[1:]:
            raise err
        return value


class ReaderCreate(UserCreate):
    is_admin: bool = False
    is_librarian: bool = False
    phone: str
    address: Address

    @field_validator('is_librarian', 'is_admin')
    @classmethod
    def have_no_privileges(cls, value: str) -> str:
        if value:
            raise ValueError('Creating reader with admin or librarian privileges forbidden')
        return value


class CreateUserResponse(BaseModel):
    user_id: int
    username: str
