import logging

from fastapi import APIRouter, HTTPException, Depends

from app.api.schemas.user import CurrentUser, LoginUser
from app.common.common import create_jwt_token, get_user_from_token
from app.repositories.user import check_user_password

login_route = APIRouter()


@login_route.post('')
async def log_in(user: LoginUser):
    if await check_user_password(user):
        data = {'sub': user.username}
        logging.info(f'User {user.username} successfully logged in')
        return {'access_token': await create_jwt_token(data), 'token_type': 'bearer'}
    raise HTTPException(status_code=401, detail='Unauthorized')


@login_route.get("/about_me")
async def about_me(current_user: str = Depends(get_user_from_token)) -> CurrentUser:
    return CurrentUser(current_user=current_user)
