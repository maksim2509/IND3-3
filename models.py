from pydantic import BaseModel, Field
from datetime import datetime

class Dish(BaseModel):
    id: int
    name: str
    category: str
    price: int
    emoji: str

class OrderCreate(BaseModel):
    dish_ids: list[int]

class Order(BaseModel):
    id: int
    dishes: list[Dish]
    total: int
    created_at: datetime
