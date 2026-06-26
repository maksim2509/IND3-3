import random
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from models import Dish, Order, OrderCreate

router = APIRouter()

DISHES = [
    Dish(id=1,  name="Борщ",                category="Супи",           price=75,  emoji="🍲"),
    Dish(id=2,  name="Солянка",             category="Супи",           price=80,  emoji="🥣"),
    Dish(id=3,  name="Вареники з картоплею",category="Головні страви", price=90,  emoji="🥟"),
    Dish(id=4,  name="Котлета по-київськи", category="Головні страви", price=120, emoji="🍗"),
    Dish(id=5,  name="Голубці",             category="Головні страви", price=95,  emoji="🥬"),
    Dish(id=6,  name="Греча з грибами",     category="Гарніри",        price=60,  emoji="🍄"),
    Dish(id=7,  name="Пюре картопляне",     category="Гарніри",        price=45,  emoji="🥔"),
    Dish(id=8,  name="Салат Цезар",         category="Салати",         price=95,  emoji="🥗"),
    Dish(id=9,  name="Компот",              category="Напої",          price=25,  emoji="🍹"),
    Dish(id=10, name="Чай",                 category="Напої",          price=20,  emoji="🍵"),
]

_counter = 1
ORDERS = []

@router.get("/dishes", response_model=list[Dish], tags=["Страви"])
def get_dishes(category: str | None = Query(None)):
    if category:
        filtered = [d for d in DISHES if d.category == category]
        if not filtered:
            raise HTTPException(404, f"Категорію '{category}' не знайдено")
        return filtered
    return DISHES

@router.get("/dishes/random", response_model=Dish, tags=["Страви"])
def get_random():
    return random.choice(DISHES)

@router.get("/dishes/{dish_id}", response_model=Dish, tags=["Страви"])
def get_dish(dish_id: int):
    dish = next((d for d in DISHES if d.id == dish_id), None)
    if not dish:
        raise HTTPException(404, f"Страву з ID {dish_id} не знайдено")
    return dish

@router.get("/categories", response_model=list[str], tags=["Страви"])
def get_categories():
    seen = []
    for d in DISHES:
        if d.category not in seen:
            seen.append(d.category)
    return seen

@router.get("/orders", response_model=list[Order], tags=["Замовлення"])
def get_orders():
    return ORDERS

@router.post("/orders", response_model=Order, status_code=201, tags=["Замовлення"])
def create_order(body: OrderCreate):
    global _counter
    dishes = [next((d for d in DISHES if d.id == i), None) for i in body.dish_ids]
    dishes = [d for d in dishes if d]
    if not dishes:
        raise HTTPException(400, "Страви не знайдено")
    order = Order(id=_counter, dishes=dishes, total=sum(d.price for d in dishes), created_at=datetime.now())
    _counter += 1
    ORDERS.append(order)
    return order

@router.delete("/orders/{order_id}", tags=["Замовлення"])
def delete_order(order_id: int):
    global ORDERS
    if not any(o.id == order_id for o in ORDERS):
        raise HTTPException(404, f"Замовлення {order_id} не знайдено")
    ORDERS = [o for o in ORDERS if o.id != order_id]
    return {"message": "Видалено"}
