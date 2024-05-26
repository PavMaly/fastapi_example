from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def check_supported_chars(input_string):
    valid_alphabets = set(
        '- АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜäöüß.')
    return all(char in valid_alphabets for char in input_string)


class CommonQueryParams:
    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = skip
        self.limit = limit


CommonDeps = Annotated[CommonQueryParams, Depends()]

GetToken = Depends(oauth2_scheme)

ALGORITHM = "HS256"
SECRET = '6b7619c4d533b948eb384a40b34e47fc18133146f9b116c51f4cebc749ac4ccd'


async def create_jwt_token(data: dict):
    expires = datetime.utcnow() + timedelta(seconds=1800)
    data.update({'exp': expires})
    return jwt.encode(data, SECRET, algorithm=ALGORITHM)


async def get_user_from_token(token: str = GetToken) -> str:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Expired token')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')
