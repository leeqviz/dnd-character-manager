from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
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


class CharacterArchetype(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "character_archetypes"

    character_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("characters.id", ondelete="CASCADE"),
        primary_key=True,
    )
    archetype_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("archetypes.id", ondelete="RESTRICT"),
        primary_key=True,
    )
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    is_primary: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    spell_casting_dc: Mapped[int | None] = mapped_column(Integer)
    spell_attack_bonus: Mapped[int | None] = mapped_column(Integer)

    character: Mapped["Character"] = relationship(back_populates="character_archetypes")
    archetype: Mapped["Archetype"] = relationship(back_populates="character_archetypes")

    __table_args__ = (
        ForeignKeyConstraint(
            ["archetype_id"],
            ["archetypes.id"],
            ondelete="SET NULL",
            name="fk_characters_classes_subclass_class",
        ),
        CheckConstraint("class_level >= 1", name="ck_characters_classes_level"),
    )
