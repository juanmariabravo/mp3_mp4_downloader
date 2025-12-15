"""
Esquemas Pydantic para la API.
"""
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum
from typing import Optional
from datetime import datetime


class FormatType(str, Enum):
    """Tipos de formato de descarga."""
    MP3 = "mp3"
    MP4 = "mp4"


class VideoQualityChoice(str, Enum):
    """Calidades de video disponibles."""
    LOW = "360"
    MEDIUM = "480"
    HD = "720"
    FULL_HD = "1080"
    BEST = "best"


class TaskStatus(str, Enum):
    """Estados posibles de una tarea de descarga."""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DownloadRequest(BaseModel):
    """Request para iniciar una descarga."""
    url: str = Field(..., description="URL del video de YouTube")
    format: FormatType = Field(default=FormatType.MP3, description="Formato de descarga (mp3 o mp4)")
    quality: Optional[VideoQualityChoice] = Field(default=None, description="Calidad del video (solo para MP4)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    "format": "mp3"
                },
                {
                    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    "format": "mp4",
                    "quality": "720"
                }
            ]
        }
    }


class DownloadResponse(BaseModel):
    """Response después de iniciar una descarga."""
    task_id: str = Field(..., description="ID único de la tarea")
    status: TaskStatus = Field(..., description="Estado actual de la tarea")
    message: str = Field(..., description="Mensaje descriptivo")
    created_at: datetime = Field(..., description="Fecha y hora de creación")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": "550e8400-e29b-41d4-a716-446655440000",
                    "status": "pending",
                    "message": "Descarga iniciada",
                    "created_at": "2025-12-15T10:30:00"
                }
            ]
        }
    }


class TaskStatusResponse(BaseModel):
    """Response con el estado de una tarea."""
    task_id: str = Field(..., description="ID de la tarea")
    status: TaskStatus = Field(..., description="Estado actual")
    progress: Optional[float] = Field(default=None, description="Progreso en porcentaje (0-100)")
    message: str = Field(..., description="Mensaje del estado actual")
    created_at: datetime = Field(..., description="Fecha de creación")
    completed_at: Optional[datetime] = Field(default=None, description="Fecha de finalización")
    file_path: Optional[str] = Field(default=None, description="Ruta del archivo descargado")
    error: Optional[str] = Field(default=None, description="Mensaje de error si falló")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "task_id": "550e8400-e29b-41d4-a716-446655440000",
                    "status": "completed",
                    "progress": 100.0,
                    "message": "Descarga completada exitosamente",
                    "created_at": "2025-12-15T10:30:00",
                    "completed_at": "2025-12-15T10:32:15",
                    "file_path": "downloads/video_title.mp3",
                    "error": None
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Response de error."""
    error: str = Field(..., description="Tipo de error")
    message: str = Field(..., description="Mensaje descriptivo del error")
    details: Optional[str] = Field(default=None, description="Detalles adicionales del error")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "ValidationError",
                    "message": "URL inválida",
                    "details": "La URL proporcionada no es una URL válida de YouTube"
                }
            ]
        }
    }
