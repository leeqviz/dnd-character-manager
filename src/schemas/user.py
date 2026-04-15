import uuid

from pydantic import BaseModel, ConfigDict


class UserOut(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    password: str
    
    model_config = ConfigDict(from_attributes=True)
        
class UserIn(BaseModel):
    name: str
    email: str
    password: str