from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Text,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.created_at import Created_At_Mixin
from .mixins.updated_at import Updated_At_Mixin
from .mixins.uuid_pk import UUID_PK_Mixin

if TYPE_CHECKING:
    from src.models.ability import Ability
    from src.models.character import Character


class CharacterAbility(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "character_abilities"

    character_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("characters.id", ondelete="CASCADE"),
        primary_key=True,
    )
    ability_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("abilities.id", ondelete="CASCADE"),
        primary_key=True,
    )
    acquired_at_level: Mapped[int | None] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(Text)

    character: Mapped["Character"] = relationship(back_populates="character_abilities")
    ability: Mapped["Ability"] = relationship(back_populates="character_abilities")

    __table_args__ = (
        CheckConstraint(
            "acquired_at_level is null or acquired_at_level >= 1",
            name="ck_character_abilities_acquired_at_level",
        ),
    )
