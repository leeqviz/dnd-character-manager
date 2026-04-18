import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.db import psql_conn
from src.main import app
from src.models import Base

TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/test_db"

engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
async_session_maker_test = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)

    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session():
    async with async_session_maker_test() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[psql_conn.get_session] = override_get_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
