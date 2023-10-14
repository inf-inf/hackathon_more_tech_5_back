from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import OfficeHistory


def get_office_history(db: Session, office_id: int):
    stmt = select(OfficeHistory).where(OfficeHistory.office_id == office_id)
    return db.execute(stmt).scalars()
