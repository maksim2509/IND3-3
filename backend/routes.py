import random
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from models import Dish, Order, OrderCreate, ErrorResponse

router = APIRouter()

DISHES: list[Dish] = [
    Dish(id=1,  name="Борщ",                category="Супи",           price=75,  emoji="🍲"),
    Dish(id=2,  name="Солянка",             category="Супи",           price=80,  emoji="🥣"),
    Dish(id=3,  name="Вареники з картоплею",category="Головні страви", price=90,  emoji="🥟"),
    Dish(id=4,  name="Котлета по-київськи", category="Головні страви", price=120, emoji="🍗"),
    Dish(id=5,  name="Голубці",             category="Головні страви", price=95,  emoji="🥬"),
    Dish(id=6,  name="Греча з грибами",     category="Гарніри",        price=60,  emoji="🍄"),
    Dish(id=7,  name="Пюре картопляне",     category="Гарніри",        price=45,  emoji="🥔"),
    Dish(id=8,  name="Рис відварний",       category="Гарніри",        price=40,  emoji="🍚"),
    Dish(id=9,  name="Салат Цезар",         category="Салати",         price=95,  emoji="🥗"),
    Dish(id=10, name="Олів'є",              category="Салати",         price=70,  emoji="🥙"),
    Dish(id=11, name="Компот",              category="Напої",          price=25,  emoji="🍹"),
    Dish(id=12, name="Чай",                 category="Напої",          price=20,  emoji="🍵"),
]

_order_id_counter = 1
ORDERS: list[Order] = []


@router.get("/dishes", response_model=list[Dish], tags=["Страви"])
def get_dishes(category: str | None = Query(None)):
    if category:
        filtered = [d for d in DISHES if d.category == category]
        if not filtered:
            raise HTTPException(status_code=404, detail=f"Категорію '{category}' не знайдено")
        return filtered
    return DISHES


@router.get("/dishes/random", response_model=Dish, tags=["Страви"])
def get_random_dish():
    return random.choice(DISHES)


@router.get("/dishes/{dish_id}", response_model=Dish, tags=["Страви"])
def get_dish(dish_id: int):
    dish = next((d for d in DISHES if d.id == dish_id), None)
    if not dish:
        raise HTTPException(status_code=404, detail=f"Страву з ID {dish_id} не знайдено")
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
    global _order_id_counter
    ordered_dishes = []
    for dish_id in body.dish_ids:
        dish = next((d for d in DISHES if d.id == dish_id), None)
        if not dish:
            raise HTTPException(status_code=404, detail=f"Страву з ID {dish_id} не знайдено")
        ordered_dishes.append(dish)
    if not ordered_dishes:
        raise HTTPException(status_code=400, detail="Список страв не може бути порожнім")
    total = sum(d.price for d in ordered_dishes)
    new_order = Order(id=_order_id_counter, dishes=ordered_dishes, total=total, created_at=datetime.now())
    _order_id_counter += 1
    ORDERS.append(new_order)
    return new_order


@router.delete("/orders/{order_id}", tags=["Замовлення"])
def delete_order(order_id: int):
    global ORDERS
    order = next((o for o in ORDERS if o.id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail=f"Замовлення з ID {order_id} не знайдено")
    ORDERS = [o for o in ORDERS if o.id != order_id]
    return {"message": f"Замовлення #{order_id} видалено"}
