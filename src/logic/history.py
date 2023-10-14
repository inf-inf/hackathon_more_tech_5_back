from sqlalchemy.orm import Session

from ..database.crud.history import get_office_history


class HistoryLogic:
    """Логика работы с историей отделений и/или банкоматов"""

    def __init__(self, db: Session):
        self._db = db

    def find_office_history(self, office_id: int):
        return get_office_history(self._db, office_id)
