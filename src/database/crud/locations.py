from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models


def get_atms_filtered(db: Session):
    stmt = select(models.ATM)
    return db.execute(stmt).scalars()


def get_offices_filtered(db: Session):
    stmt = select(models.Office)
    return db.execute(stmt).scalars()
