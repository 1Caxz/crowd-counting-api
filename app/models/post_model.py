from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from app.core.database import Base

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255))
    image = Column(String(255))

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    
    user = func.relationship("User")