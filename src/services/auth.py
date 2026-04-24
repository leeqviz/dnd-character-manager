from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users import UsersRepository
from src.schemas.auth import LoginSchema


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UsersRepository(self.session)

    async def get_user_credentials(self, name: str, email: str):
        user = await self.repo.get_by_name_and_email(name, email)
        return LoginSchema.model_validate(user)
