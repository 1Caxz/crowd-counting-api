from pydantic import BaseModel
from typing import Optional

class PostCreate(BaseModel):
    user_id: int
    title: str
    image: str

class PostUpdate(BaseModel):
    title: Optional[str]

class PostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    image: str
    heatmap: str
    count: float
    
    class Config:
        from_attributes = True