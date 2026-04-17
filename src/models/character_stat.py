from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base
from .mixins import Created_At_Mixin, Updated_At_Mixin

if TYPE_CHECKING:
    from src.models.character import Character


class CharacterStat(Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "character_stats"

    strength: Mapped[int] = mapped_column(Integer, nullable=False)
    dexterity: Mapped[int] = mapped_column(Integer, nullable=False)
    constitution: Mapped[int] = mapped_column(Integer, nullable=False)
    intelligence: Mapped[int] = mapped_column(Integer, nullable=False)
    wisdom: Mapped[int] = mapped_column(Integer, nullable=False)
    charisma: Mapped[int] = mapped_column(Integer, nullable=False)

    character_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("characters.id", ondelete="CASCADE"),
        primary_key=True,
        unique=True,
    )

    character: Mapped["Character"] = relationship(back_populates="stat")

    __table_args__ = (
        CheckConstraint(
            "strength between 1 and 30", name="ck_character_stats_strength"
        ),
        CheckConstraint(
            "dexterity between 1 and 30", name="ck_character_stats_dexterity"
        ),
        CheckConstraint(
            "constitution between 1 and 30", name="ck_character_stats_constitution"
        ),
        CheckConstraint(
            "intelligence between 1 and 30", name="ck_character_stats_intelligence"
        ),
        CheckConstraint("wisdom between 1 and 30", name="ck_character_stats_wisdom"),
        CheckConstraint(
            "charisma between 1 and 30", name="ck_character_stats_charisma"
        ),
    )
