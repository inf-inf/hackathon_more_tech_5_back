import random


class SMS:
    def send(self, phone: str, text: str) -> None:
        ...

    @staticmethod
    def generate_code() -> str:
        return str(random.randint(1000, 9999))
