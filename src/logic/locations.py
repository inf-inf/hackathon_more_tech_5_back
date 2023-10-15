from typing import Literal
from sqlalchemy.orm import Session
from ..database.crud import locations as locations_crud


class LocationsLogic:
    """Логика работы с отделениями и банкоматами"""
    def __init__(self, db: Session):
        self._db = db

    def find_atms(self, filter_data: locations_crud.FindATMFilter):
        return locations_crud.get_atms_filtered(self._db, filter_data)

    def find_offices(self, filter_data: locations_crud.FindOfficesFilter):
        return locations_crud.get_offices_filtered(self._db, filter_data)

    def get_location_reviews(self, location_type: Literal['atm', 'office'], location_id: int):
        location_types_mapping = {
            'atm': locations_crud.get_atm_reviews,
            'office': locations_crud.get_office_reviews
        }
        get_reviews = location_types_mapping[location_type]
        return get_reviews(self._db, location_id)

    def post_office_review(self, _phone: str, _office_id: int, _review: str) -> bool:
        return True

    def request_office_visit(self, _office_id: int) -> dict[str, bool]:
        return {'9:00': False, '9:15': True, '9:30': False}

    def register_office_visit(self, phone: str, _office_id: int, _selected_time: str) -> dict[str, str]:
        return {
            'address': '141506, Московская область, г. Солнечногорск, ул. Красная, д. 60',
            'code': 'ЭО-123',
            'phone': phone,
            'datetime': '10:45'
        }
