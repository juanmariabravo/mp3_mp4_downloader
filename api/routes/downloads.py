"""
Rutas para las operaciones de descarga.
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from api.models import (
    DownloadRequest,
    DownloadResponse,
    TaskStatusResponse,
    ErrorResponse,
    TaskStatus
)
from api.task_manager import task_manager

router = APIRouter(prefix="/download", tags=["downloads"])


@router.post(
    "",
    response_model=DownloadResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Iniciar descarga",
    description="Inicia una descarga de YouTube y retorna un task_id para seguimiento"
)
async def create_download(request: DownloadRequest):
    """
    Inicia una nueva descarga de YouTube.
    
    - **url**: URL del video de YouTube
    - **format**: mp3 (audio) o mp4 (video)
    - **quality**: Calidad del video (solo para MP4): 360, 480, 720, 1080, best
    
    Retorna un task_id que puedes usar para consultar el estado de la descarga.
    """
    try:
        # Validar que si es MP4, se proporcione calidad
        quality = None
        if request.format == "mp4":
            quality = request.quality.value if request.quality else "720"
        
        # Crear tarea
        task_id = task_manager.create_task(
            url=request.url,
            format_type=request.format.value,
            quality=quality
        )
        
        return DownloadResponse(
            task_id=task_id,
            status=TaskStatus.PENDING,
            message=f"Descarga de {request.format.upper()} iniciada",
            created_at=datetime.now()
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al iniciar la descarga: {str(e)}"
        )


@router.get(
    "/status/{task_id}",
    response_model=TaskStatusResponse,
    summary="Consultar estado",
    description="Consulta el estado de una descarga por su task_id"
)
async def get_download_status(task_id: str):
    """
    Consulta el estado de una descarga.
    
    - **task_id**: ID de la tarea retornado por el endpoint de descarga
    
    Retorna el estado actual, progreso y detalles de la descarga.
    """
    task = task_manager.get_task(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea {task_id} no encontrada"
        )
    
    return task.to_response()
