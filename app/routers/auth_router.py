from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user = auth_service.register(db, data)
    if not user:
        return {"error_message": "Email already exist"}
    return {"message": "User registered successfully"}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    token, query = auth_service.login(db, data)
    if not token:
        return {"error_message": "Invalid credentials"}
    return {"name": query.name, "email": query.email, "access_token": token, "token_type": "bearer"}
