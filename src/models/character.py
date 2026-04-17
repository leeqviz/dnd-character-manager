from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .mixins import Created_At_Mixin, Updated_At_Mixin, UUID_PK_Mixin

if TYPE_CHECKING:
    from src.models.background import Background
    from src.models.character_ability import CharacterAbility
    from src.models.character_archetype import CharacterArchetype
    from src.models.character_item import CharacterItem
    from src.models.character_skill import CharacterSkill
    from src.models.character_spell import CharacterSpell
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

    alignment: Mapped[str | None] = mapped_column(Text)
    level: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, server_default="1"
    )
    experience: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    proficiency_bonus: Mapped[int] = mapped_column(
        Integer, nullable=False, default=2, server_default="2"
    )
    armor_class: Mapped[int | None] = mapped_column(Integer)
    initiative: Mapped[int | None] = mapped_column(Integer)
    speed: Mapped[int | None] = mapped_column(Integer)
    max_hp: Mapped[int | None] = mapped_column(Integer)
    current_hp: Mapped[int | None] = mapped_column(Integer)
    temp_hp: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    inspiration: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    notes: Mapped[str | None] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="characters")
    race: Mapped[Optional["Race"]] = relationship(back_populates="characters")
    background: Mapped[Optional["Background"]] = relationship(
        back_populates="characters"
    )
    character_stat: Mapped[Optional["CharacterStat"]] = relationship(
        back_populates="character",
        uselist=False,
        cascade="all, delete-orphan",
    )
    character_items: Mapped[list["CharacterItem"]] = relationship(
        back_populates="character",
        cascade="all, delete-orphan",
    )
    character_archetypes: Mapped[list["CharacterArchetype"]] = relationship(
        back_populates="character",
        cascade="all, delete-orphan",
    )
    character_skills: Mapped[list["CharacterSkill"]] = relationship(
        back_populates="character",
        cascade="all, delete-orphan",
    )
    character_abilities: Mapped[list["CharacterAbility"]] = relationship(
        back_populates="character",
        cascade="all, delete-orphan",
    )
    character_spells: Mapped[list["CharacterSpell"]] = relationship(
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
