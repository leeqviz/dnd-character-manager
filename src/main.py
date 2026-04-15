import uuid
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.connection import get_async_session, init_db
from src.db.models import User, UserIn, UserOut


@asynccontextmanager
async def lifespan(_: FastAPI):
    print("server is starting...")
    await init_db()
    yield
    print("server is stopping...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allows all origins
    allow_methods=["*"],      # Allows all methods
    allow_headers=["*"],      # Allows all headers
    allow_credentials=True,   # Allows cookies
)

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/users", response_model=list[UserOut])
async def get_users(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(User)) 
    items = result.scalars().all()        
    return items

@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_async_session)):
    user = await db.get(User, user_id)
    return user

@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn, db: AsyncSession = Depends(get_async_session)):
    new_user = User(id=uuid.uuid4(), name=user.name, email=user.email, hashed_password=user.password)
    db.add(new_user)
    await db.commit()
    return new_user

@router.patch("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: uuid.UUID, user: UserIn, db: AsyncSession = Depends(get_async_session)):
    db_user = await db.get(User, user_id)
    db_user.name = user.name if user.name is not None else db_user.name
    db_user.email = user.email if user.email is not None else db_user.email
    db_user.hashed_password = user.password is not None if user.password else db_user.hashed_password
    await db.commit()
    return db_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_async_session)):
    db_user = await db.get(User, user_id)
    await db.delete(db_user)
    await db.commit()


app.include_router(router, prefix="/api", tags=["api"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)