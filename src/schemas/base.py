from pydantic import BaseModel, ConfigDict


class BaseCamelModel(BaseModel):
    """Базовая модель для Response, использующих alias CamelCase"""
    model_config = ConfigDict(populate_by_name=True)


class BaseOrmModel(BaseCamelModel):
    """Базовая модель для поддержки ORM"""
    model_config = ConfigDict(from_attributes=True)
