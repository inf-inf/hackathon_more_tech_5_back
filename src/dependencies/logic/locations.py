from ...logic.locations import LocationsLogic


def get_locations_logic() -> LocationsLogic:
    """Инициализация логики для работы с отделениями и банкоматами"""
    return LocationsLogic()
