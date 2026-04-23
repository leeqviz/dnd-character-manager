import os

# Set ENV_STATE to "test" to use test database with .env.test
os.environ["ENV_STATE"] = "test"


from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs import settings
from src.db import get_psql_session, psql_conn
from src.main import app

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", settings.postgres.url)
    command.upgrade(config, "head")
    yield  # tests run
    command.downgrade(config, "base")


@pytest_asyncio.fixture(name="db_session")
async def get_psql_session_test() -> AsyncGenerator[AsyncSession]:
    async with psql_conn.session_maker() as session:
        yield session
        await session.rollback()
        # await session.close()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient]:
    async def override_get_psql_session() -> AsyncGenerator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_psql_session] = override_get_psql_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
