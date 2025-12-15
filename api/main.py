"""
API REST para el descargador de YouTube.

Ejecutar con: uvicorn api.main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes.downloads import router as downloads_router

# Crear aplicación FastAPI
app = FastAPI(
    title="YouTube Downloader API",
    description="API REST para descargar audio y video desde YouTube",
    version="0.3.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(downloads_router)


@app.get("/", tags=["root"])
async def root():
    """Endpoint raíz de la API."""
    return {
        "message": "YouTube Downloader API",
        "version": "0.3.0",
        "docs": "/docs",
        "endpoints": {
            "download": "POST /download",
            "status": "GET /download/status/{task_id}"
        }
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
