from typing import TypedDict
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from .. import models

_EARTH_RADIUS = 6371  # примерный радиус Земли в км


class FindATMFilter(TypedDict):
    latitude: float
    longitude: float
    initial_latitude: float | None
    initial_longitude: float | None
    zoom: float
    all_day: bool | None
    avg_rating: int | None
    wheelchair: bool | None
    blind: bool | None
    nfc_support: bool | None
    qr_support: bool | None
    withdraw_currencies: list[str] | None
    deposit_currencies: list[str] | None


def get_atms_filtered(db: Session, filter_data: FindATMFilter):
    # TODO Добавить withdraw_currencies, deposit_currencies, ограничение числа точек в завис. от координат
    stmt = select(
        models.ATM,
        (func.acos(
            func.sin(func.radians(models.ATM.latitude)) * func.sin(func.radians(filter_data["latitude"])) +
            func.cos(func.radians(models.ATM.latitude)) * func.cos(func.radians(filter_data["latitude"])) *
            func.cos(func.radians(models.ATM.longitude) - func.radians(filter_data["longitude"]))
        ) * _EARTH_RADIUS).label("distance")
    ).where(
        models.ATM.avg_rating.is_not(None) if filter_data["avg_rating"] else True,
        models.ATM.avg_rating >= filter_data["avg_rating"] if filter_data["avg_rating"] else True,
        models.Week.all_time == filter_data["all_day"] if filter_data["all_day"] else True,
        models.ATMServices.wheelchair == filter_data["wheelchair"] if filter_data["wheelchair"] else True,
        models.ATMServices.blind == filter_data["blind"] if filter_data["blind"] else True,
        models.ATMServices.nfc == filter_data["nfc_support"] if filter_data["nfc_support"] else True,
        models.ATMServices.qr_code == filter_data["qr_support"] if filter_data["qr_support"] else True,
    ).join(
        models.Week, models.ATM.week_info_id == models.Week.id
    ).join(
        models.ATMServices, models.ATM.service_info_id == models.ATMServices.id
    )
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


def get_atm_reviews(db: Session, atm_id: int):
    stmt = select(models.ATMReviews).filter(models.ATMReviews.atm_id == atm_id)
    return db.execute(stmt).scalars()


def get_office_reviews(db: Session, office_id: int):
    stmt = select(models.OfficeReviews).filter(models.OfficeReviews.office_id == office_id)
    return db.execute(stmt).scalars()
