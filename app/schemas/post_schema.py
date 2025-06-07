from pydantic import BaseModel
from typing import Optional

class PostUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]

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