from pydantic import BaseModel
from typing import Optional

class PostCreate(BaseModel):
    user_id: int
    title: str
    image: str

class PostUpdate(BaseModel):
    title: Optional[str]

class PostDelete(BaseModel):
    id: int

class PostResponse(PostCreate):
    id: int
    
    class Config:
        orm_mode = True