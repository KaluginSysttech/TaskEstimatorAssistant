"""Main entrypoint for Statistics API.

This is a separate entrypoint from the main bot application.
It runs a FastAPI server that provides statistics data for the frontend dashboard.

Run with:
    uvicorn src.api_main:app --host 0.0.0.0 --port 8001 --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.stats_api import router

# Create FastAPI application
app = FastAPI(
    title="TEA Statistics API",
    description="""
    Mock API для дашборда статистики проекта TEA.
    
    Предоставляет статистику по диалогам Telegram-бота:
    - Ключевые метрики (диалоги, пользователи, длина, рост)
    - Графики активности
    - Последние диалоги
    - Топ пользователей
    
    **Текущая версия:** Mock реализация с тестовыми данными.
    
    **Sprint F5:** Будет заменена на реальную реализацию с подключением к БД.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.get("/", tags=["health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "TEA Statistics API",
        "version": "1.0.0",
        "implementation": "mock",
        "docs": "/docs"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "service": "TEA Statistics API",
        "version": "1.0.0",
        "implementation": "mock",
        "endpoints": {
            "stats": "/api/v1/stats?period={day|week|month}",
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api_main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )

