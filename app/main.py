from fastapi import FastAPI
from app.routers import post_router, user_router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Crowd Counting API")
app.include_router(post_router.router)
app.include_router(user_router.router)