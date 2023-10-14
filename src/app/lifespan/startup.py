from __future__ import annotations

import json
import random
from statistics import mean
from typing import TYPE_CHECKING, Any

from src.database.models import ATM, Office, ATMReviews, OfficeReviews, Week
from src.database.base import Base, engine

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


# TODO: нужно лишь для Хакатона, чтобы заполнить БД данными
_demo_reviews = [
    "Мне понравилось, неплохо",
    "Господи, что это?",
    "Дизлайк, если б мог - я бы поставил",
    "Это лучшее, что я видел",
    "Я заблудился, как это возможно?",
    "Это было страшное место",
    "Обслуживали, обслуживали да не дообслуживали",
    "Приду еще раз, но как нибудь никогда",
    "Хорошо, мне нравится, но можно лучше",
    "Людное место, не понял что это, но мне понравилось",
    "Надо было взять с собой что нибудь поесть",
    "фывл лдфытво лджфыив, ой, что это я",
    None,
    None
]


class StartupEvent:
    """startup события для приложения FastAPI"""
    def __init__(self, session: Session):
        self._session = session

    def run(self):
        """Запуск startup события"""
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        atms_json, offices_json = self.__read_input_json()

        self._insert_atms(atms_json)
        self._insert_offices(offices_json)

    def _insert_atms(self, atms_json: list[dict[str, Any]]):
        """Создает записи про банкоматы в БД (atms)"""
        for atm_json in atms_json:
            reviews = self.__generate_reviews_for_atms()
            avg_rating = int(mean(review.rating for review in reviews)) if reviews else None
            atm = ATM(
                address=atm_json["address"],
                latitude=atm_json["latitude"],
                longitude=atm_json["longitude"],
                avg_rating=avg_rating,
                reviews=reviews
            )
            self._session.add(atm)

    def _insert_offices(self, offices_json: list[dict[str, Any]]):
        """Создает записи про офисы в БД (offices)"""
        for office_json in offices_json:
            reviews = self.__generate_reviews_for_offices()
            avg_rating = int(mean(review.rating for review in reviews)) if reviews else None
            office = Office(
                address=office_json["address"],
                latitude=office_json["latitude"],
                longitude=office_json["longitude"],
                with_ramp=office_json["hasRamp"] == "Y" if office_json["hasRamp"] else False,
                avg_rating=avg_rating,
                reviews=reviews,
                week_info_fiz=self.__parse_working_days_office(office_json["openHoursIndividual"]),
                week_info_yur=self.__parse_working_days_office(office_json["openHours"]),
                service_info=OfficeServices(
                    rko=office_json["rko"] == "есть РКО" if office_json["rko"] else False,
                    suo=office_json["suoAvailability"] == "Y",
                    kep=office_json["kep"] or False,
                    currency_input=Currency(
                        rub=True,
                        usd=True,
                        eur=True
                    ),
                    currency_output=Currency(
                        rub=True,
                        usd=True,
                        eur=True
                    )
                )
            )
            self._session.add(office)

    @staticmethod
    def __parse_working_days_office(days: list[dict[str, str]]) -> Week:
        """Парсятся рабочие дни в конкретном офисе для записи в БД (week)"""
        week = Week()
        for day_info in days:
            if day_info["days"] == "пн":
                week.monday = day_info["hours"] if day_info["hours"] != "выходной" else None
            elif day_info["days"] == "вт":
                week.tuesday = day_info["hours"] if day_info["hours"] != "выходной" else None
            elif day_info["days"] == "ср":
                week.wednesday = day_info["hours"] if day_info["hours"] != "выходной" else None
            elif day_info["days"] == "чт":
                week.thursday = day_info["hours"] if day_info["hours"] != "выходной" else None
            elif day_info["days"] == "пт":
                week.friday = day_info["hours"] if day_info["hours"] != "выходной" else None
            elif day_info["days"] == "сб":
                week.saturday = day_info["hours"] if day_info["hours"] != "выходной" else None
            else:
                week.sunday = day_info["hours"] if day_info["hours"] != "выходной" else None
        return week

    @staticmethod
    def __generate_reviews_for_atms() -> list[ATMReviews]:
        """Генерирует отзывы для банкоматов (atm_reviews)"""
        return [ATMReviews(rating=random.randint(10, 50), content=random.choice(_demo_reviews))
                for _ in range(random.randint(0, 10))]

    @staticmethod
    def __generate_reviews_for_offices():
        """Генерирует отзывы для банкоматов (office_reviews)"""
        return [OfficeReviews(rating=random.randint(10, 50), content=random.choice(_demo_reviews))
                for _ in range(random.randint(0, 10))]

    @staticmethod
    def __read_input_json():
        """Чтение входных данных (актуально только для Хакатона)"""
        with open("data/atms.json", encoding="utf-8") as atms_file:
            atms_json = json.loads(atms_file.read())

        with open("data/offices.json", encoding="utf-8") as offices_file:
            offices_json = json.loads(offices_file.read())

        return atms_json, offices_json
