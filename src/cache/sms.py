from typing import Any


# Мок реализация вместо Redis. Ключ - код, значение - SentSmsInfo
SMS_CACHE: dict[str, Any] = {}
