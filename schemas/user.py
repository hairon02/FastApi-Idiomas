from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    hashed_password: str = Field(..., min_length=6, max_length=100)
    fecha_registro:  datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(
        from_attributes=True
    )
    

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int 

