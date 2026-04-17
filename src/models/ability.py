from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.created_at import Created_At_Mixin
from .mixins.updated_at import Updated_At_Mixin
from .mixins.uuid_pk import UUID_PK_Mixin

if TYPE_CHECKING:
    from .archetype import Archetype
    from .character_ability import CharacterAbility
    from .race import Race


class Ability(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "abilities"

    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    archetype_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("archetypes.id", ondelete="SET NULL"),
    )
    race_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        ForeignKey("races.id", ondelete="SET NULL"),
    )

    archetype: Mapped[Optional["Archetype"]] = relationship(
        back_populates="abilities",
        foreign_keys=[archetype_id],
    )
    race: Mapped[Optional["Race"]] = relationship(
        back_populates="abilities",
        foreign_keys=[race_id],
    )
    character_abilities: Mapped[list["CharacterAbility"]] = relationship(
        back_populates="ability",
        passive_deletes=True,
    )

    __table_args__ = (
        CheckConstraint(
            "type in ('feat', 'trait', 'feature', 'racial', 'class')",
            name="ck_abilities_type",
        ),
    )
