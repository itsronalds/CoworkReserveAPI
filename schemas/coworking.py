from pydantic import BaseModel
from typing import Optional


class CoworkingBase(BaseModel):
    name: str
    ubication: str
    price_by_hour: Optional[float]
    capacity: int
    is_available: int


class Coworking(CoworkingBase):
    id: int
