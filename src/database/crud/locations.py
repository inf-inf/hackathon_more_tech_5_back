from typing import TypedDict
from sqlalchemy import Integer, select, func, asc
from sqlalchemy.orm import Session

from .. import models

_EARTH_RADIUS = 6371  # примерный радиус Земли в км


def _zoom_mapper(zoom: float) -> float:
    """TODO: временное решение, для оптимизации возвращаемых точек

    :param zoom: приближение на карте
    """
    if zoom < 10:
        radius = 999999.0
    elif zoom < 10.5:
        radius = 40.0
    elif zoom < 11:
        radius = 25.0
    elif zoom < 12:
        radius = 20.0
    elif zoom < 13:
        radius = 10.0
    elif zoom < 14:
        radius = 5.0
    elif zoom < 15:
        radius = 2.0
    elif zoom < 16:
        radius = 1.0
    else:
        radius = 0.5
    return radius


class BaseFilter(TypedDict):
    latitude: float
    longitude: float
    initial_latitude: float | None
    initial_longitude: float | None
    zoom: float
    avg_rating: int | None


class FindATMFilter(BaseFilter):
    all_day: bool | None
    wheelchair: bool | None
    blind: bool | None
    nfc_support: bool | None
    qr_support: bool | None
    withdraw_currencies: list[str] | None
    deposit_currencies: list[str] | None


class FindOfficesFilter(BaseFilter):
    avg_service_time: int | None
    count_clients_now: int | None
    with_ramp: bool | None
    prime: bool | None
    vip: bool | None
    rko: bool | None
    suo: bool | None
    kep: bool | None
    withdraw_currencies: list[str] | None
    deposit_currencies: list[str] | None


def get_atms_filtered(db: Session, filter_data: FindATMFilter):
    # TODO Добавить filter withdraw_currencies, deposit_currencies
    radius_search = _zoom_mapper(filter_data["zoom"])
    stmt = select(
        models.ATM,
        (func.acos(
            func.sin(func.radians(models.ATM.latitude)) * func.sin(func.radians(filter_data["initial_latitude"])) +
            func.cos(func.radians(models.ATM.latitude)) * func.cos(func.radians(filter_data["initial_latitude"])) *
            func.cos(func.radians(models.ATM.longitude) - func.radians(filter_data["initial_longitude"]))
        ) * _EARTH_RADIUS).label("distance"),
    ).where(
        (func.acos(
            func.sin(func.radians(models.ATM.latitude)) * func.sin(func.radians(filter_data["latitude"])) +
            func.cos(func.radians(models.ATM.latitude)) * func.cos(func.radians(filter_data["latitude"])) *
            func.cos(func.radians(models.ATM.longitude) - func.radians(filter_data["longitude"]))
        ) * _EARTH_RADIUS) <= radius_search,

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
    ).order_by(
        asc("distance")
    )
    return db.execute(stmt).all()


def get_offices_filtered(db: Session, filter_data: FindOfficesFilter):
    # TODO Добавить filter withdraw_currencies, deposit_currencies
    radius_search = _zoom_mapper(filter_data["zoom"])
    distance = (
        func.acos(
            func.sin(func.radians(models.Office.latitude)) * func.sin(func.radians(filter_data["initial_latitude"])) +
            func.cos(func.radians(models.Office.latitude)) * func.cos(func.radians(filter_data["initial_latitude"])) *
            func.cos(func.radians(models.Office.longitude) - func.radians(filter_data["initial_longitude"]))
        ) * _EARTH_RADIUS
    ).label("distance")

    stmt = select(
        models.Office,
        distance,
        (
            func.cast(distance + models.Office.avg_service_time * models.Office.count_clients_now, Integer)
        ).label("time_wait")
    ).where(
        (func.acos(
            func.sin(func.radians(models.Office.latitude)) * func.sin(func.radians(filter_data["latitude"])) +
            func.cos(func.radians(models.Office.latitude)) * func.cos(func.radians(filter_data["latitude"])) *
            func.cos(func.radians(models.Office.longitude) - func.radians(filter_data["longitude"]))
        ) * _EARTH_RADIUS) <= radius_search,
        models.Office.avg_rating.is_not(None) if filter_data["avg_rating"] else True,
        models.Office.avg_rating >= filter_data["avg_rating"] if filter_data["avg_rating"] else True,
        models.Office.avg_service_time <= filter_data["avg_service_time"] if filter_data["avg_service_time"] else True,
        models.Office.count_clients_now <= filter_data["count_clients_now"] if filter_data["count_clients_now"] else True,
        models.OfficeServices.with_ramp == filter_data["with_ramp"] if filter_data["with_ramp"] else True,
        models.OfficeServices.prime == filter_data["prime"] if filter_data["prime"] else True,
        models.OfficeServices.vip == filter_data["vip"] if filter_data["vip"] else True,
        models.OfficeServices.rko == filter_data["rko"] if filter_data["rko"] else True,
        models.OfficeServices.suo == filter_data["suo"] if filter_data["suo"] else True,
        models.OfficeServices.suo == filter_data["kep"] if filter_data["kep"] else True,
    ).join(
        models.OfficeServices, models.OfficeServices.id == models.Office.service_info_id
    ).order_by(
        asc("time_wait")
    )
    return db.execute(stmt).all()


def get_atm_reviews(db: Session, atm_id: int):
    stmt = select(models.ATMReviews).filter(models.ATMReviews.atm_id == atm_id)
    return db.execute(stmt).scalars()


def get_office_reviews(db: Session, office_id: int):
    stmt = select(models.OfficeReviews).filter(models.OfficeReviews.office_id == office_id)
    return db.execute(stmt).scalars()
