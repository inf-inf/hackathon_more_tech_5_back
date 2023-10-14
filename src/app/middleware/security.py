from fastapi import Request


async def add_response_token_header(request: Request, call_next):
    """Middleware добавляет в ответ X-Token Header если он был выставлен в request.state.new_token

    Некоторые методы могут проверять токен и выставлять новый, для следующего запроса от фронта
    с помощью `dependencies.security.user.check_user_token`
    """
    request.state.new_token = None

    response = await call_next(request)

    if request.state.new_token:
        response.headers['X-Token'] = request.state.new_token

    return response
