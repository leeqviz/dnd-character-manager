from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db import init_db
from src.routers import api_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    print("server is starting...")
    await init_db()
    yield
    print("server is stopping...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,   # Allows cookies
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)