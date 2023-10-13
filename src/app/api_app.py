from fastapi import FastAPI


class ApiApp(FastAPI):
    def __int__(self):
        super().__init__(
            title="MORE Tech 5.0",
            description="Сервис для подбора оптимального отделения банка, учитывая потребности клиента и доступность "
                        "услуг"
        )
