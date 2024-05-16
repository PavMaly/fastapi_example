
from fastapi import APIRouter, HTTPException

from app.api.schemas.user import CreateUserResponse, ReaderCreate, UserCreate
from app.common.common import GetToken
from app.repositories.user import add_new_user, check_is_worker

registration_route = APIRouter()


@registration_route.post('')
async def register_reader(reader: ReaderCreate):
    """Registrate new reader in library."""
    return await add_new_user(reader)


@registration_route.post('/worker')
async def register_worker(worker: UserCreate, token: str = GetToken) -> CreateUserResponse:
    """Registrate new worker in library."""
    await check_is_worker(token)
    if worker.is_admin or worker.is_librarian:
        return await add_new_user(worker)
    raise HTTPException(status_code=422, detail='No privileges passed. New worker MUST have one or more privileges')
