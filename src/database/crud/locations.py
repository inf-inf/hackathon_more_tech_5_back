from sqlalchemy.orm import Session

from .. import models

def get_atms_filtered(db: Session):
    return db.query(
        models.ATM
    ).all()
