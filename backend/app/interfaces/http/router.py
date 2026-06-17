from fastapi import APIRouter

from app.interfaces.http.routers import auth, catalog, dashboard, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboards", tags=["dashboards"])
api_router.include_router(catalog.router, prefix="/catalog", tags=["catalog"])
