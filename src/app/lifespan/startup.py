from __future__ import annotations

from datetime import datetime
import json
import random
from statistics import mean
from typing import TYPE_CHECKING, Any

from src.database.models import (
    ATM, ATMReviews, ATMServices, Currency, Office, OfficeHistory, OfficeReviews, OfficeServices, Week
)
from src.database.base import Base, engine

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


# # # TODO: нужно лишь для Хакатона, чтобы заполнить БД данными # # #
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
_atm_week_info = {
    "start": ["06:00", "07:00", "08:00", "08:30", "09:00", "10:00"],
    "end": ["21:00", "21:30", "21:45", "22:00", "23:00", "00:00", "01:00", "02:00"]
}
_atm_services_mapper = {
    "AVAILABLE": True,
    "UNAVAILABLE": False,
    "UNKNOWN": False
}
_office_history_time = [
    "12:00:00", "13:00:00", "14:00:00", "15:00:00", "16:00:00", "17:00:00", "18:00:00", "19:00:00", "20:00:00"
]
_office_history_date = [
    "2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04", "2023-10-05", "2023-10-06", "2023-10-07", "2023-10-08",
    "2023-10-09", "2023-10-10", "2023-10-11", "2023-10-12", "2023-10-13", "2023-10-14"
]
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class StartupEvent:
    """startup события для приложения FastAPI"""
    def __init__(self, session: Session):
        self._session = session

    def run(self):
        """Запуск startup события"""
        Base.metadata.drop_all(engine)  # drop all tables
        Base.metadata.create_all(engine)  # create all tables

        atms_json, offices_json = self.__read_input_json()

        self._insert_atms(atms_json)
        self._insert_offices(offices_json)

    def _insert_atms(self, atms_json: list[dict[str, Any]]):
        """Создает записи про банкоматы в БД (atms)"""
        for atm_json in atms_json:
            reviews = self.__generate_reviews_for_atms()
            review_count = len(reviews)
            avg_rating = int(mean(review.rating for review in reviews)) if reviews else None
            if atm_json["allDay"]:
                week_info = Week(all_time=True)
            else:
                week_info = Week(
                    monday=self.__generate_week_info_for_atms(),
                    tuesday=self.__generate_week_info_for_atms(),
                    wednesday=self.__generate_week_info_for_atms(),
                    thursday=self.__generate_week_info_for_atms(),
                    friday=self.__generate_week_info_for_atms(),
                    saturday=self.__generate_week_info_for_atms(),
                    sunday=self.__generate_week_info_for_atms()
                )
            atm = ATM(
                address=atm_json["address"],
                latitude=atm_json["latitude"],
                longitude=atm_json["longitude"],
                avg_rating=avg_rating,
                reviews=reviews,
                review_count=review_count,
                service_info=ATMServices(
                    wheelchair=_atm_services_mapper[atm_json["services"]["wheelchair"]["serviceActivity"]],
                    blind=_atm_services_mapper[atm_json["services"]["blind"]["serviceActivity"]],
                    nfc=_atm_services_mapper[atm_json["services"]["nfcForBankCards"]["serviceActivity"]],
                    qr_code=_atm_services_mapper[atm_json["services"]["qrRead"]["serviceActivity"]],
                    currency_input=Currency(
                        rub=_atm_services_mapper[atm_json["services"]["supportsRub"]["serviceActivity"]],
                        usd=_atm_services_mapper[atm_json["services"]["supportsUsd"]["serviceActivity"]],
                        eur=_atm_services_mapper[atm_json["services"]["supportsEur"]["serviceActivity"]]
                    ),
                    currency_output=Currency(
                        rub=_atm_services_mapper[atm_json["services"]["supportsChargeRub"]["serviceActivity"]],
                        usd=False,
                        eur=False
                    )
                ),
                week_info=week_info
            )
            self._session.add(atm)

    def _insert_offices(self, offices_json: list[dict[str, Any]]):
        """Создает записи про офисы в БД (offices)"""
        for office_json in offices_json:
            reviews = self.__generate_reviews_for_offices()
            review_count = len(reviews)
            avg_rating = int(mean(review.rating for review in reviews)) if reviews else None
            week_info_fiz = self.__parse_working_days_office(office_json["openHoursIndividual"])
            week_info_yur = self.__parse_working_days_office(
                office_json["openHours"],
                # проверка, чтобы не было ситуации, когда офис не работает ни для физ. лиц, ни для юр. лиц
                need_random=week_info_fiz is not None
            )
            office = Office(
                address=office_json["address"],
                latitude=office_json["latitude"],
                longitude=office_json["longitude"],
                avg_rating=avg_rating,
                reviews=reviews,
                review_count=review_count,
                avg_service_time=random.randint(3, 15),
                count_clients_now=random.randint(0, 10),
                week_info_fiz=week_info_fiz,
                week_info_yur=week_info_yur,
                service_info=OfficeServices(
                    with_ramp=office_json["hasRamp"] == "Y" if office_json["hasRamp"] else False,
                    prime=random.choice([True, True, True, False]),
                    vip=random.choice([True, False, False, False]),
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
                ),
                history=self.__generate_history_for_office()
            )
            self._session.add(office)

    @staticmethod
    def __parse_working_days_office(days: list[dict[str, str]], *, need_random: bool = True) -> Week | None:
        """Парсятся рабочие дни в конкретном офисе для записи в БД (week)

        :param days: информация о днях недели из json
        :param need_random: использовать ли random или нет (True - использовать)
        """
        choice = random.choice([True, False])
        if not choice and need_random:
            return None

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
    def __generate_week_info_for_atms() -> str | None:
        """Генерирует время работы банкомата на неделе"""
        work_time = f'{random.choice(_atm_week_info["start"])}-{random.choice(_atm_week_info["end"])}'
        return random.choice([work_time, work_time, work_time, None])

    @staticmethod
    def __generate_reviews_for_offices():
        """Генерирует отзывы для банкоматов (office_reviews)"""
        return [OfficeReviews(rating=random.randint(10, 50), content=random.choice(_demo_reviews))
                for _ in range(random.randint(0, 10))]

    @staticmethod
    def __generate_history_for_office():
        """Генерирует историю посещения (событий) офиса"""
        return [
            OfficeHistory(
                dt=datetime.fromisoformat(
                    f"{random.choice(_office_history_date)} {random.choice(_office_history_time)}"
                ),
                count_clients=random.randint(0, 12)
            )
            for _ in range(100)
        ]

    @staticmethod
    def __read_input_json():
        """Чтение входных данных (актуально только для Хакатона)"""
        with open("data/atms.json", encoding="utf-8") as atms_file:
            atms_json = json.loads(atms_file.read())

        with open("data/offices.json", encoding="utf-8") as offices_file:
            offices_json = json.loads(offices_file.read())

        return atms_json, offices_json
