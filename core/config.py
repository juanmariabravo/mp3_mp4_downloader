"""
Configuración y constantes del proyecto.
"""
from enum import Enum
from dataclasses import dataclass
from typing import Dict


class VideoQuality(Enum):
    """Calidades de video disponibles."""
    LOW = '360'
    MEDIUM = '480'
    HD = '720'
    FULL_HD = '1080'
    BEST = 'best'


class FormatType(Enum):
    """Tipos de formato de descarga."""
    MP3 = 'mp3'
    MP4 = 'mp4'


@dataclass
class Config:
    """Configuración global del descargador."""
    
    # Calidades de video con descripciones
    VIDEO_QUALITIES: Dict[str, Dict[str, str]] = None
    
    # Configuración de audio
    AUDIO_QUALITY: str = '0'  # VBR 0 (máxima calidad)
    
    # Configuración de descarga
    NO_PLAYLIST: bool = True  # Solo descargar videos individuales
    
    # Formato de nombre de archivo
    OUTPUT_TEMPLATE: str = '%(title)s.%(ext)s'
    
    def __post_init__(self):
        """Inicializa las calidades de video si no están definidas."""
        if self.VIDEO_QUALITIES is None:
            self.VIDEO_QUALITIES = {
                '1': {'resolution': VideoQuality.LOW.value, 'description': '360p (Baja calidad)'},
                '2': {'resolution': VideoQuality.MEDIUM.value, 'description': '480p (Calidad media)'},
                '3': {'resolution': VideoQuality.HD.value, 'description': '720p HD (Recomendado)'},
                '4': {'resolution': VideoQuality.FULL_HD.value, 'description': '1080p Full HD'},
                '5': {'resolution': VideoQuality.BEST.value, 'description': 'Mejor calidad disponible'}
            }
    
    @staticmethod
    def get_default():
        """Retorna una configuración por defecto."""
        return Config()
