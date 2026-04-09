from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.db.connection import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting...")
    await init_db()
    yield
    
    print("server is stopping...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}
