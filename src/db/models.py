import uuid
from datetime import datetime, timezone

from pydantic import BaseModel
from sqlalchemy import DateTime, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

timestamp_with_tz = datetime.now(timezone.utc)

class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=timestamp_with_tz, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=timestamp_with_tz, onupdate=timestamp_with_tz, server_default=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"
    
class UserOut(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    
    class Config:
        from_attributes = True
        
class UserIn(BaseModel):
    name: str
    email: str
    password: str