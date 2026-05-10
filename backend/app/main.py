from fastapi import FastAPI

from backend.app.core.config import settings
from backend.app.routes.health import router as health_router
from backend.app.routes.products import router as products_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

app.include_router(health_router)
app.include_router(products_router)
