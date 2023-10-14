from sqlalchemy.orm import Session
from ..database.crud import locations as locations_crud


class LocationsLogic:
    """Логика работы с отделениями и банкоматами"""
    def __init__(self, db: Session):
        self._db = db

    def find_atms(self, filter_data):
        return locations_crud.get_atms_filtered(self._db)

    def find_offices(self, filter_data):
        return locations_crud.get_offices_filtered(self._db)

    def get_atm_reviews(self, atm_id: int):
        return locations_crud.get_atm_reviews(self._db, atm_id)

    def get_office_reviews(self, office_id: int):
        return locations_crud.get_office_reviews(self._db, office_id)

    def request_office_visit(self, _office_id: int) -> dict[str, bool]:
        return {'9:00': False, '9:15': True, '9:30': False}

    def register_office_visit(self, phone: str) -> dict[str, str]:
        return {
            'address': '141506, Московская область, г. Солнечногорск, ул. Красная, д. 60',
            'code': 'ЭО-123',
            'phone': phone,
            'datetime': '...'
        }
