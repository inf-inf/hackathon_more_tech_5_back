from fastapi import Depends
from sqlalchemy.orm import Session
from ...logic.locations import LocationsLogic
from ..database.connection import get_db


def get_locations_logic(db: Session = Depends(get_db)) -> LocationsLogic:
    """Инициализация логики для работы с отделениями и банкоматами"""
    return LocationsLogic(db)
