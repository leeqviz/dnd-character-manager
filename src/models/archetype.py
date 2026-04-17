from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.created_at import Created_At_Mixin
from .mixins.updated_at import Updated_At_Mixin
from .mixins.uuid_pk import UUID_PK_Mixin

if TYPE_CHECKING:
    pass


class Archetype(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "archetypes"

    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    hit_die: Mapped[int] = mapped_column(Integer, nullable=False)
    spell_casting_ability: Mapped[str | None] = mapped_column(String(3))
    description: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint("hit_die in (4, 6, 8, 10, 12)", name="ck_classes_hit_die"),
        CheckConstraint(
            "spell_casting_ability in ('INT', 'WIS', 'CHA') or spell_casting_ability is null",
            name="ck_classes_spell_casting_ability",
        ),
    )
