from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

def safe_commit(db: Session, operation_description: str = "Operasi"):
    """Helper for DB commit transaction with universal error handling"""
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logger.error(f"{operation_description} failed: duplicated/integrity: {e}")
        raise HTTPException(status_code=400, detail=f"{operation_description} failed: data already exist or invalid.")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"{operation_description} failed: {e}")
        raise HTTPException(status_code=500, detail=f"{operation_description} failed: server failure.")

def handle_not_found(obj, message="Data not found"):
    """Helper to raise 404 object doesn't exist"""
    if not obj:
        raise HTTPException(status_code=404, detail=message)
    return obj