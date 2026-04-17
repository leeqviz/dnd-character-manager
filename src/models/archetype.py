from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.created_at import Created_At_Mixin
from .mixins.updated_at import Updated_At_Mixin
from .mixins.uuid_pk import UUID_PK_Mixin

if TYPE_CHECKING:
    from src.models.ability import Ability
    from src.models.character_archetype import CharacterArchetype
    from src.models.character_spell import CharacterSpell


class Archetype(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "archetypes"

    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    hit_die: Mapped[int] = mapped_column(Integer, nullable=False)
    spell_casting_ability: Mapped[str | None] = mapped_column(String(3))
    description: Mapped[str | None] = mapped_column(Text)

    character_archetypes: Mapped[list["CharacterArchetype"]] = relationship(
        back_populates="archetype",
        passive_deletes=True,
    )
    abilities: Mapped[list["Ability"]] = relationship(
        back_populates="archetype",
        passive_deletes=True,
        foreign_keys="Ability.archetype_id",
    )
    character_spells: Mapped[list["CharacterSpell"]] = relationship(
        back_populates="archetype",
        passive_deletes=True,
    )

    __table_args__ = (
        CheckConstraint("hit_die in (4, 6, 8, 10, 12)", name="ck_archetypes_hit_die"),
        CheckConstraint(
            "spell_casting_ability in ('INT', 'WIS', 'CHA') or spell_casting_ability is null",
            name="ck_archetypes_spell_casting_ability",
        ),
    )
