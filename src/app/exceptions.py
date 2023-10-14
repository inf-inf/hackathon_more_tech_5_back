from fastapi import Request
from fastapi.responses import JSONResponse


class BaseApiException(Exception):
    """Базовый класс для исключений, которые должны возвращать ответ из API с кодом 4xx"""
    def __init__(self, msg: str, status_code: int = 400):
        self.msg = msg
        self.status_code = status_code


async def base_api_exception_handler(_request: Request, exc: BaseApiException) -> JSONResponse:
    """Обработчик ошибок BaseApiException"""
    return JSONResponse(
        content={'msg': exc.msg}, status_code=exc.status_code
    )


exception_handlers = {
    BaseApiException: base_api_exception_handler,
}
