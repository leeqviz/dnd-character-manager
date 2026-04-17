from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.created_at import Created_At_Mixin
from .mixins.updated_at import Updated_At_Mixin
from .mixins.uuid_pk import UUID_PK_Mixin

if TYPE_CHECKING:
    from .character_spell import CharacterSpell


class Spell(UUID_PK_Mixin, Created_At_Mixin, Updated_At_Mixin, Base):
    __tablename__ = "spells"

    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    school: Mapped[str | None] = mapped_column(Text)
    range: Mapped[str | None] = mapped_column(Text)
    duration_time: Mapped[str | None] = mapped_column(Text)
    casting_time: Mapped[str | None] = mapped_column(Text)
    ritual: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    concentration: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    description: Mapped[str | None] = mapped_column(Text)

    character_spells: Mapped[list["CharacterSpell"]] = relationship(
        back_populates="spell",
        passive_deletes=True,
    )

    __table_args__ = (CheckConstraint("level between 0 and 9", name="ck_spells_level"),)
