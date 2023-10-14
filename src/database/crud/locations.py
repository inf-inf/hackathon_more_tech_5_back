from sqlalchemy import select, func
from sqlalchemy.orm import Session

from .. import models

_EARTH_RADIUS = 6371  # примерный радиус Земли в км


def get_atms_filtered(db: Session, filter_data):
    if filter_data["latitude"] and filter_data["longitude"]:
        stmt = select(
            models.ATM,
            (func.acos(
                func.sin(func.radians(models.ATM.latitude)) * func.sin(func.radians(filter_data["latitude"])) +
                func.cos(func.radians(models.ATM.latitude)) * func.cos(func.radians(filter_data["latitude"])) *
                func.cos(func.radians(models.ATM.longitude) - func.radians(filter_data["longitude"]))
            ) * _EARTH_RADIUS).label("distance")
        )
    else:
        stmt = select(models.ATM)
    return db.execute(stmt).all()


def get_offices_filtered(db: Session, filter_data):
    if filter_data["latitude"] and filter_data["longitude"]:
        stmt = select(
            models.Office,
            (func.acos(
                func.sin(func.radians(models.Office.latitude)) * func.sin(func.radians(filter_data["latitude"])) +
                func.cos(func.radians(models.Office.latitude)) * func.cos(func.radians(filter_data["latitude"])) *
                func.cos(func.radians(models.Office.longitude) - func.radians(filter_data["longitude"]))
            ) * _EARTH_RADIUS).label("distance")
        )
    else:
        stmt = select(models.Office)
    return db.execute(stmt).all()
