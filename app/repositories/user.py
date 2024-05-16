import hashlib

from fastapi import HTTPException, Depends

from app.api.schemas.user import LoginUser, BaseUser, UserCreate, CreateUserResponse
from app.common.common import oauth2_scheme, get_user_from_token
from app.common.logger import log
from app.db.database import database, SALT
from app.db.db_executor import db_executor


@log
async def get_user_id(username: str) -> int:
    query = 'SELECT user_id FROM users ' \
            'WHERE username = :username;'
    values = {'username': username}
    result = await db_executor.fetch_one(query, values)
    if result:
        return result['user_id']
    raise HTTPException(status_code=401, detail='Unauthorized')


@log
async def get_user_password(user_id: int) -> str:
    query = 'SELECT password FROM users ' \
            'WHERE user_id = :user_id;'
    values = {'user_id': user_id}
    result = await db_executor.fetch_one(query, values)
    return result['password']


@log
async def check_user_password(user: LoginUser) -> bool:
    user_id = await get_user_id(user.username)
    saved_hash = await get_user_password(user_id)
    hash_to_check = hashlib.sha512((user.password + SALT).encode()).hexdigest()
    return saved_hash == hash_to_check


@log
async def check_user_exists(user: BaseUser):
    query = 'SELECT FROM users ' \
            'WHERE username = :username;'
    values = {'username': user.username}
    result = await db_executor.fetch_all(query, values)
    if result:
        raise HTTPException(status_code=409, detail=f'User with username {user.username} already exists.')


@log
async def check_email_is_used(reader: UserCreate):
    query = 'SELECT FROM users_data ' \
            'WHERE email = :email;'
    values = {'email': reader.email}
    result = await db_executor.fetch_all(query, values)
    if result:
        raise HTTPException(status_code=409, detail=f'Email address {reader.email} is already used.')


@log
async def create_user(user: UserCreate) -> int:
    password = hashlib.sha512((user.password + SALT).encode()).hexdigest()
    query = 'INSERT INTO users (username, is_admin, is_librarian, password) ' \
            'VALUES (:username, :is_admin, :is_librarian, :password) ' \
            'RETURNING user_id;'
    values = {'username': user.username, 'is_admin': user.is_admin, 'is_librarian': user.is_librarian,
              'password': password}
    return await db_executor.execute(query, values)


@log
async def add_user_info(user: UserCreate, user_id: int) -> None:
    query = 'INSERT INTO users_data (user_id, full_name, email, phone, address) ' \
            'VALUES (:user_id, :full_name, :email, :phone, :address) ;'
    address = ''.join(user.address.dict().values())
    full_name = f'{user.full_name.last_name} {user.full_name.first_name}'
    values = {'user_id': user_id, 'full_name': full_name, 'email': user.email, 'phone': user.phone,
              'address': address}
    return await db_executor.execute(query, values)


@log
async def add_new_user(user: UserCreate) -> CreateUserResponse:
    await check_user_exists(user)
    await check_email_is_used(user)
    async with database.transaction():
        new_user_id = await create_user(user)
        await add_user_info(user, new_user_id)
    return CreateUserResponse(user_id=new_user_id, username=user.username)


@log
async def check_role(username: str, role: str):
    query = f'SELECT {role} FROM users ' \
            f'WHERE username = :username;'
    values = {'username': username}
    result = await db_executor.fetch_one(query, values)
    if not result:
        raise HTTPException(status_code=404, detail=f'User with username <{username}> not found')
    return getattr(result, role)


@log
async def _is_worker(username: str) -> bool:
    worker_roles = ['is_admin', 'is_librarian']
    user_roles = [role for role in worker_roles if await check_role(username, role)]
    return any(user_roles)


@log
async def user_is_worker(token):
    user = await get_user_from_token(token)
    return await _is_worker(user)


@log
async def check_is_worker(token):
    if not await user_is_worker(token):
        raise HTTPException(status_code=403, detail='Only privileged users allowed')