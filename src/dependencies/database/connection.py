from sqlalchemy.orm import Session
from ...database.base import SessionLocal


def get_db() -> Session:
    """Открыть соединение с бд"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
