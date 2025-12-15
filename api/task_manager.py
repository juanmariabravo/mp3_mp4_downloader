"""
Gestor de tareas de descarga en memoria.
"""
import uuid
from datetime import datetime
from typing import Dict, Optional
from threading import Thread
import sys
import os
import glob
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core import DownloaderService, VideoQuality
from core.config import FormatType as CoreFormatType
from api.models.schemas import TaskStatus, TaskStatusResponse


class Task:
    """Representa una tarea de descarga."""
    
    def __init__(self, task_id: str, url: str, format_type: str, quality: Optional[str] = None):
        self.task_id = task_id
        self.url = url
        self.format_type = format_type
        self.quality = quality
        self.status = TaskStatus.PENDING
        self.progress = 0.0
        self.message = "Tarea creada"
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None
        self.file_path: Optional[str] = None
        self.file_name: Optional[str] = None
        self.error: Optional[str] = None
    
    def to_response(self) -> TaskStatusResponse:
        """Convierte la tarea a un TaskStatusResponse."""
        return TaskStatusResponse(
            task_id=self.task_id,
            status=self.status,
            progress=self.progress,
            message=self.message,
            created_at=self.created_at,
            completed_at=self.completed_at,
            file_path=self.file_path,
            file_name=self.file_name,
            error=self.error
        )


class TaskManager:
    """
    Gestor de tareas de descarga en memoria.
    En producción, esto debería usar una base de datos y Celery.
    """
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.downloader = DownloaderService()
    
    def create_task(self, url: str, format_type: str, quality: Optional[str] = None) -> str:
        """
        Crea una nueva tarea de descarga.
        
        Args:
            url: URL del video
            format_type: Formato (mp3 o mp4)
            quality: Calidad del video (opcional)
        
        Returns:
            ID de la tarea creada
        """
        task_id = str(uuid.uuid4())
        task = Task(task_id, url, format_type, quality)
        self.tasks[task_id] = task
        
        # Iniciar descarga en un hilo separado
        thread = Thread(target=self._execute_download, args=(task_id,))
        thread.daemon = True
        thread.start()
        
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Obtiene una tarea por su ID."""
        return self.tasks.get(task_id)
    
    def _execute_download(self, task_id: str):
        """
        Ejecuta la descarga en segundo plano.
        
        Args:
            task_id: ID de la tarea a ejecutar
        """
        task = self.tasks.get(task_id)
        if not task:
            return
        
        try:
            # Actualizar estado a descargando
            task.status = TaskStatus.DOWNLOADING
            task.message = "Descargando..."
            task.progress = 10.0
            
            # Crear directorio downloads si no existe
            downloads_dir = Path("downloads")
            downloads_dir.mkdir(exist_ok=True)
            
            # Usar template de yt-dlp para incluir el título del video
            # Formato: {task_id}_%(title)s.ext
            file_extension = "mp3" if task.format_type == "mp3" else "mp4"
            output_template = str(downloads_dir / f"{task_id}_%(title)s.{file_extension}")
            
            # Ejecutar descarga según el formato
            if task.format_type == "mp3":
                result = self.downloader.download_audio(task.url, output_path=output_template)
            else:
                # Convertir quality string a VideoQuality enum
                quality_map = {
                    "360": VideoQuality.LOW,
                    "480": VideoQuality.MEDIUM,
                    "720": VideoQuality.HD,
                    "1080": VideoQuality.FULL_HD,
                    "best": VideoQuality.BEST
                }
                quality_enum = quality_map.get(task.quality, VideoQuality.HD)
                result = self.downloader.download_video(task.url, quality=quality_enum, output_path=output_template)
            
            # Actualizar progreso
            task.progress = 90.0
            task.status = TaskStatus.PROCESSING
            task.message = "Procesando..."
            
            # Verificar resultado
            if result.success:
                task.status = TaskStatus.COMPLETED
                task.progress = 100.0
                task.message = result.message
                task.completed_at = datetime.now()
                
                # Buscar el archivo descargado que comienza con el task_id
                pattern = str(downloads_dir / f"{task_id}_*.{file_extension}")
                files = glob.glob(pattern)
                
                if files:
                    # Debería haber solo un archivo
                    file_path = files[0]
                    task.file_path = os.path.abspath(file_path)
                    # Extraer solo el nombre del archivo (sin la ruta)
                    task.file_name = os.path.basename(file_path)
                else:
                    task.file_path = None
                    task.file_name = None
            else:
                task.status = TaskStatus.FAILED
                task.message = result.message
                task.error = result.error
                task.completed_at = datetime.now()
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.message = "Error inesperado durante la descarga"
            task.error = str(e)
            task.completed_at = datetime.now()


# Instancia global del gestor de tareas
task_manager = TaskManager()
