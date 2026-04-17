from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import (
    Boolean,
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
    from src.models.archetype import Archetype
    from src.models.character import Character
    from src.models.spell import Spell


class CharacterSpell(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "character_spells"

    character_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("characters.id", ondelete="CASCADE"),
        primary_key=True,
    )
    spell_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("spells.id", ondelete="CASCADE"),
        primary_key=True,
    )
    archetype_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("archetypes.id", ondelete="SET NULL"),
    )
    is_known: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    is_prepared: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    spell_slot_level: Mapped[int | None] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(Text)

    character: Mapped["Character"] = relationship(back_populates="character_spells")
    spell: Mapped["Spell"] = relationship(back_populates="character_spells")
    archetype: Mapped[Optional["Archetype"]] = relationship(
        back_populates="character_archetypes"
    )

    __table_args__ = (
        CheckConstraint(
            "spell_slot_level is null or spell_slot_level between 0 and 9",
            name="ck_character_spells_slot_level",
        ),
    )
