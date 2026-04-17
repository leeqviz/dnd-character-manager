from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.created_at import Created_At_Mixin
from .mixins.updated_at import Updated_At_Mixin
from .mixins.uuid_pk import UUID_PK_Mixin

if TYPE_CHECKING:
    pass


class Skill(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "skills"

    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    stat_code: Mapped[str] = mapped_column(String(3), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint(
            "stat_code in ('STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA')",
            name="ck_skills_stat_code",
        ),
    )
