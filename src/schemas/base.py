from pydantic import BaseModel, ConfigDict


class BaseOrmModel(BaseModel):
    """Базовая модель для поддержки ORM"""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
