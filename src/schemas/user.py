import uuid

from pydantic import BaseModel


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