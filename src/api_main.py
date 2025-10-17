"""Main entrypoint for Statistics API.

This is a separate entrypoint from the main bot application.
It runs a FastAPI server that provides statistics data for the frontend dashboard.

Run with:
    uvicorn src.api_main:app --host 0.0.0.0 --port 8001 --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.chat_api import router as chat_router
from src.api.stats_api import router as stats_router
from src.config.settings import Settings
from src.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database connection on startup."""
    # Startup
    settings = Settings()
    init_db(settings.database_url)
    print(f"[OK] Database initialized: {settings.database_url.split('@')[0]}@***")
    yield
    # Cleanup
    print("[OK] Application shutdown")

# Create FastAPI application
app = FastAPI(
    title="TEA API",
    description="""
    API для дашборда статистики и чата проекта TEA.
    
    **Функционал:**
    - Статистика по диалогам Telegram-бота
    - Веб-интерфейс чата с двумя режимами:
      - Normal: Общение с LLM-ассистентом
      - Admin: Вопросы по статистике диалогов
    
    **Endpoints:**
    - `/api/v1/stats` - Получение статистики
    - `/api/v1/chat/message` - Отправка сообщения в чат
    
    **Текущая версия:** Sprint F4
    
    **Sprint F5:** Переход с Mock на реальное подключение к БД.
    """,
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
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
app.include_router(stats_router)
app.include_router(chat_router)


@app.get("/", tags=["health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "TEA API",
        "version": "1.1.0",
        "sprint": "F4",
        "docs": "/docs"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "service": "TEA API",
        "version": "1.1.0",
        "sprint": "F4",
        "endpoints": {
            "stats": "/api/v1/stats?period={day|week|month}",
            "chat": "/api/v1/chat/message",
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

