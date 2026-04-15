import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_async_session
from src.models.user import User
from src.schemas.user import UserIn, UserOut

users_router = APIRouter()

@users_router.get("/", response_model=list[UserOut])
async def get_users(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(User)) 
    items = result.scalars().all()        
    return items

@users_router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_async_session)):
    user = await db.get(User, user_id)
    return user

@users_router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn, db: AsyncSession = Depends(get_async_session)):
    new_user = User(id=uuid.uuid4(), name=user.name, email=user.email, hashed_password=user.password)
    db.add(new_user)
    await db.commit()
    return new_user

@users_router.patch("/{user_id}", response_model=UserOut)
async def update_user(user_id: uuid.UUID, user: UserIn, db: AsyncSession = Depends(get_async_session)):
    db_user = await db.get(User, user_id)
    db_user.name = user.name if user.name is not None else db_user.name
    db_user.email = user.email if user.email is not None else db_user.email
    db_user.hashed_password = user.password is not None if user.password else db_user.hashed_password
    await db.commit()
    return db_user

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_async_session)):
    db_user = await db.get(User, user_id)
    await db.delete(db_user)
    await db.commit()