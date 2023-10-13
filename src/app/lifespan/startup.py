import json

from src.database.base import Base, engine


class StartupEvent:
    """startup события для приложения FastAPI"""

    def run(self):
        """Запуск startup события"""
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        self._insert_atms()
        self._insert_offices()
        self._insert_working_weeks_offices()
        self._generate_reviews_for_atms()
        self._generate_reviews_for_offices()

    def _insert_atms(self):
        """Создает записи про банкоматы в БД (atms)"""

    def _insert_offices(self):
        """Создает записи про офисы в БД (offices)"""

    def _insert_working_weeks_offices(self):
        """Создает записи в БД (week)"""

    def _generate_reviews_for_atms(self):
        """Генерирует отзывы для банкоматов (atm_reviews)"""

    def _generate_reviews_for_offices(self):
        """Генерирует отзывы для банкоматов (office_reviews)"""

    @staticmethod
    def _read_input_json():
        """Чтение входных данных (актуально только для Хакатона)"""
        with open("data/atms.json") as atms_file:
            atms_json = json.loads(atms_file.read())

        with open("data/offices.json") as offices_file:
            offices_json = json.loads(offices_file.read())

        return atms_json, offices_json
