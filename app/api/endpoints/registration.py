
from fastapi import APIRouter, HTTPException

from app.api.schemas.user import CreateUserResponse, ReaderCreate, UserCreate
from app.common.common import GetToken
from app.repositories.user import add_new_user, check_is_staff

registration_route = APIRouter()


@registration_route.post('')
async def register_reader(reader: ReaderCreate):
    """Registrate new reader in library."""
    return await add_new_user(reader)


@registration_route.post('/staff')
async def register_worker(staff: UserCreate, token: str = GetToken) -> CreateUserResponse:
    """Registrate new staff in library."""
    await check_is_staff(token)
    if staff.is_admin or staff.is_librarian:
        return await add_new_user(staff)
    raise HTTPException(status_code=422, detail='No privileges passed. New staff MUST have one or more privileges')
