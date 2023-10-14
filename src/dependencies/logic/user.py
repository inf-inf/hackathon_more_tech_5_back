from ...logic.user import UserLogic


def get_user_logic() -> UserLogic:
    """Инициализация логики для работы с пользователем"""
    return UserLogic()
