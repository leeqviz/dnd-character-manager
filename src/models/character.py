from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .mixins import Created_At_Mixin, Updated_At_Mixin, UUID_PK_Mixin

if TYPE_CHECKING:
    from src.models.background import Background
    from src.models.character_item import CharacterItem
    from src.models.character_stat import CharacterStat
    from src.models.race import Race
    from src.models.user import User


class Character(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "characters"

    user_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    race_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("races.id", ondelete="SET NULL"),
    )
    background_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("backgrounds.id", ondelete="SET NULL"),
    )

    user: Mapped["User"] = relationship(back_populates="characters")
    race: Mapped[Optional["Race"]] = relationship(back_populates="characters")
    background: Mapped[Optional["Background"]] = relationship(
        back_populates="characters"
    )
    stat: Mapped[Optional["CharacterStat"]] = relationship(
        back_populates="character",
        uselist=False,
        cascade="all, delete-orphan",
    )
    character_items: Mapped[list["CharacterItem"]] = relationship(
        back_populates="character",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint("level >= 1", name="ck_characters_level"),
        CheckConstraint("experience >= 0", name="ck_characters_experience"),
        CheckConstraint(
            "proficiency_bonus >= 2", name="ck_characters_proficiency_bonus"
        ),
        CheckConstraint("max_hp is null or max_hp >= 0", name="ck_characters_max_hp"),
        CheckConstraint(
            "current_hp is null or current_hp >= 0", name="ck_characters_current_hp"
        ),
        CheckConstraint("temp_hp >= 0", name="ck_characters_temp_hp"),
        CheckConstraint("speed is null or speed > 0", name="ck_characters_speed"),
        CheckConstraint(
            "armor_class is null or armor_class >= 0", name="ck_characters_ac"
        ),
    )
