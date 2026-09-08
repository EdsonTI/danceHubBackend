from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.tenant.auth import router as auth_router
from app.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Plataforma Híbrida: SaaS para Escuelas y Marketplace de Baile."
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["System"])
    def health_check():
        return {"status": "ok", "service": settings.PROJECT_NAME}

    app.include_router(auth_router, prefix="/api/tenant/auth")
    
    return app

app = create_app()