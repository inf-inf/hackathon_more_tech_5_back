from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models


def get_atms_filtered(db: Session):
    stmt = select(models.ATM)
    return db.execute(stmt).scalars()


def get_offices_filtered(db: Session):
    stmt = select(models.Office)
    return db.execute(stmt).scalars()


def get_atm_reviews(db: Session, atm_id: int):
    stmt = select(models.ATMReviews).filter(models.ATMReviews.atm_id == atm_id)
    return db.execute(stmt).scalars()


def get_office_reviews(db: Session, office_id: int):
    stmt = select(models.OfficeReviews).filter(models.OfficeReviews.office_id == office_id)
    return db.execute(stmt).scalars()
