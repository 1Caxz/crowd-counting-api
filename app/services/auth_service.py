from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.utils.jwt_helper import create_access_token
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register(db: Session, data: RegisterRequest):
    if db.query(User).filter(User.name == data.name).first():
        return None  # user already exists

    hashed_pw = pwd_context.hash(data.password)
    query = User(name=data.name, email=data.email)
    query.password = hashed_pw
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def login(db: Session, data: LoginRequest):
    query = db.query(User).filter(User.email == data.email).first()
    if not query or not pwd_context.verify(data.password, query.password):
        return None
    token = create_access_token(data={"user_id": query.id, "email": query.email})
    return token
