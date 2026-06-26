from datetime import datetime
from pydantic import BaseModel

class Dish(BaseModel):
    id: int
    name: str
    category: str
    price: float
    emoji: str

class OrderCreate(BaseModel):
    dish_ids: list[int]

class Order(BaseModel):
    id: int
    dishes: list[Dish]
    total: float
    created_at: datetime

class ErrorResponse(BaseModel):
    detail: str
