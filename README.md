# 🍽️ Обідній Вибір

Сайт для вибору страв на обід.

**Live demo:** https://YOUR_USERNAME.github.io/lunch-site  
**Backend API:** https://YOUR-APP.onrender.com/docs

## Фічі
- 📋 Меню з фільтром за категорією
- 🛒 Кошик з підрахунком суми
- 🎲 Рулетка випадкового вибору
- 🛎️ Оформлення замовлення
- 🗑️ Видалення замовлення
- ⚠️ Обробка помилок

## API
| Метод | Ендпоінт | Опис |
|-------|----------|------|
| GET | `/dishes` | Всі страви |
| GET | `/dishes/random` | Випадкова страва |
| GET | `/dishes/{id}` | Страва за ID |
| GET | `/categories` | Категорії |
| GET | `/orders` | Замовлення |
| POST | `/orders` | Створити замовлення |
| DELETE | `/orders/{id}` | Видалити замовлення |

## Як запустити локально
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
