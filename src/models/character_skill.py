from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.created_at import Created_At_Mixin
from .mixins.updated_at import Updated_At_Mixin
from .mixins.uuid_pk import UUID_PK_Mixin

if TYPE_CHECKING:
    from src.models.character import Character
    from src.models.skill import Skill


class CharacterSkill(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "character_skills"

    character_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("characters.id", ondelete="CASCADE"),
        primary_key=True,
    )
    skill_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("skills.id", ondelete="CASCADE"),
        primary_key=True,
    )
    proficient: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    expertise: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    bonus: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )

    character: Mapped["Character"] = relationship(back_populates="character_skills")
    skill: Mapped["Skill"] = relationship(back_populates="character_skills")

    __table_args__ = (
        CheckConstraint(
            "not expertise or proficient",
            name="ck_character_skills_expertise_requires_proficiency",
        ),
    )
