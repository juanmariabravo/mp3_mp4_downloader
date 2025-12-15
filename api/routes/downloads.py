"""
Rutas para las operaciones de descarga.
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from datetime import datetime
import os

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
        if request.format.value == "mp4":
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


@router.get(
    "/file/{task_id}",
    summary="Descargar archivo",
    description="Descarga el archivo resultante de una tarea completada"
)
async def download_file(task_id: str):
    """
    Descarga el archivo de una tarea completada.
    
    - **task_id**: ID de la tarea completada
    
    Retorna el archivo descargado para que el usuario lo pueda guardar.
    """
    task = task_manager.get_task(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea {task_id} no encontrada"
        )
    
    if task.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La tarea aún no ha sido completada. Estado actual: {task.status}"
        )
    
    if not task.file_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archivo no encontrado para esta tarea"
        )
    
    file_path = task.file_path
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El archivo no existe en el servidor"
        )
    
    # Obtener el nombre del archivo sin el task_id
    # Formato: task_id_nombre_real.ext -> nombre_real.ext
    filename = task.file_name or os.path.basename(file_path)
    
    # Remover el task_id del nombre para dar el archivo con su nombre original
    if filename.startswith(task_id):
        # Formato: {task_id}_título.ext -> título.ext
        filename = filename[len(task_id)+1:]  # +1 para el guion bajo
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )
