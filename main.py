from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

app = FastAPI(
    title="🍽️ Обідній Вибір API",
    description="API для сайту вибору обіду.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "🍽️ API працює!", "docs": "/docs"}
