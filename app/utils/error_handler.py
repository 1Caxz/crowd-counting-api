from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

def safe_commit(db: Session, operation_description: str = "Operasi"):
    """Helper untuk commit transaksi DB dengan error handling universal"""
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logger.error(f"{operation_description} gagal karena duplikasi/integritas: {e}")
        raise HTTPException(status_code=400, detail=f"{operation_description} gagal: data sudah ada atau tidak valid.")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"{operation_description} gagal: {e}")
        raise HTTPException(status_code=500, detail=f"{operation_description} gagal karena kesalahan server.")

def handle_not_found(obj, message="Data tidak ditemukan"):
    """Helper untuk raise 404 jika objek tidak ada"""
    if not obj:
        raise HTTPException(status_code=404, detail=message)
    return obj