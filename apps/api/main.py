from fastapi import FastAPI
from sqlalchemy import text

from apps.api.config import get_settings
from apps.api.db.session import engine
from apps.api.routers.organization import router as organization_router


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Adaptive multi-agent logistics coordination platform.",
)

app.include_router(organization_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    database_status = "ok"

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        database_status = "error"

    return {
        "status": "ok" if database_status == "ok" else "degraded",
        "service": settings.app_name,
        "environment": settings.app_env,
        "version": settings.app_version,
        "database": database_status,
    }