from fastapi import Depends
from sqlalchemy.orm import Session
from ...logic.history import HistoryLogic
from ..database.connection import get_db


def get_history_logic(db: Session = Depends(get_db)) -> HistoryLogic:
    """Инициализация логики для работы с отделениями и банкоматами"""
    return HistoryLogic(db)
