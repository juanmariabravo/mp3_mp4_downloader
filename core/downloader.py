"""
Servicio de descarga de contenido desde YouTube.
"""
import subprocess
import sys
import os
from typing import Optional, Tuple
from static_ffmpeg import run

from .config import Config, FormatType, VideoQuality


class DownloadResult:
    """Resultado de una operación de descarga."""
    
    def __init__(self, success: bool, message: str = "", output: str = "", error: str = ""):
        self.success = success
        self.message = message
        self.output = output
        self.error = error
    
    def __repr__(self):
        status = "SUCCESS" if self.success else "FAILED"
        return f"DownloadResult({status}, message='{self.message}')"


class DownloaderService:
    """
    Servicio para descargar y convertir contenido desde YouTube.
    
    Soporta descarga de audio (MP3) y video (MP4) con diferentes calidades.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Inicializa el servicio de descarga.
        
        Args:
            config: Configuración del descargador. Si no se proporciona, usa la configuración por defecto.
        """
        self.config = config or Config.get_default()
        self._ffmpeg_path, self._ffprobe_path = self._initialize_ffmpeg()
    
    def _initialize_ffmpeg(self) -> Tuple[str, str]:
        """
        Inicializa y obtiene las rutas de ffmpeg y ffprobe.
        
        Returns:
            Tuple con las rutas de ffmpeg y ffprobe.
        """
        try:
            ffmpeg_path, ffprobe_path = run.get_or_fetch_platform_executables_else_raise()
            return ffmpeg_path, ffprobe_path
        except Exception as e:
            raise RuntimeError(f"Error al inicializar ffmpeg: {e}")
    
    def download_audio(self, url: str, output_path: Optional[str] = None) -> DownloadResult:
        """
        Descarga solo el audio de un video en formato MP3.
        
        Args:
            url: URL del video de YouTube.
            output_path: Ruta opcional para guardar el archivo.
        
        Returns:
            DownloadResult con el resultado de la operación.
        """
        return self._download(url, FormatType.MP3, output_path=output_path)
    
    def download_video(
        self, 
        url: str, 
        quality: VideoQuality = VideoQuality.HD,
        output_path: Optional[str] = None
    ) -> DownloadResult:
        """
        Descarga video con audio en formato MP4.
        
        Args:
            url: URL del video de YouTube.
            quality: Calidad del video (VideoQuality enum).
            output_path: Ruta opcional para guardar el archivo.
        
        Returns:
            DownloadResult con el resultado de la operación.
        """
        return self._download(url, FormatType.MP4, quality, output_path)
    
    def _download(
        self,
        url: str,
        format_type: FormatType,
        quality: Optional[VideoQuality] = None,
        output_path: Optional[str] = None
    ) -> DownloadResult:
        """
        Ejecuta la descarga según el formato especificado.
        
        Args:
            url: URL del video.
            format_type: Tipo de formato (MP3 o MP4).
            quality: Calidad del video (solo para MP4).
            output_path: Ruta de salida personalizada.
        
        Returns:
            DownloadResult con el resultado de la operación.
        """
        # Construir comando base
        command = [
            sys.executable,
            '-m', 'yt_dlp',
            '--no-playlist' if self.config.NO_PLAYLIST else '--yes-playlist',
            '--ffmpeg-location', os.path.dirname(self._ffmpeg_path),
            '--output', output_path or self.config.OUTPUT_TEMPLATE,
            url
        ]
        
        # Configurar según el formato
        if format_type == FormatType.MP3:
            command.extend([
                '-x',  # Extraer solo audio
                '--audio-format', 'mp3',
                '--audio-quality', self.config.AUDIO_QUALITY,
            ])
            format_desc = f"MP3 | Calidad: Máxima (VBR {self.config.AUDIO_QUALITY})"
        
        elif format_type == FormatType.MP4:
            quality = quality or VideoQuality.HD
            
            # Construir string de formato para yt-dlp
            if quality == VideoQuality.BEST:
                format_string = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'
            else:
                format_string = (
                    f'bestvideo[ext=mp4][height<={quality.value}]+bestaudio[ext=m4a]/'
                    f'bestvideo[height<={quality.value}]+bestaudio/'
                    f'best[height<={quality.value}]'
                )
            
            command.extend([
                '-f', format_string,
                '--merge-output-format', 'mp4',
                '--postprocessor-args', 'ffmpeg:-c:v copy -c:a aac',
            ])
            
            quality_desc = next(
                (v['description'] for v in self.config.VIDEO_QUALITIES.values() 
                 if v['resolution'] == quality.value),
                quality.value
            )
            format_desc = f"MP4 | Calidad: {quality_desc}"
        
        else:
            return DownloadResult(
                success=False,
                message=f"Formato no soportado: {format_type}",
                error="Invalid format type"
            )
        
        # Ejecutar descarga
        try:
            process = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            return DownloadResult(
                success=True,
                message=f"Descarga completada exitosamente ({format_desc})",
                output=process.stdout
            )
        
        except subprocess.CalledProcessError as e:
            return DownloadResult(
                success=False,
                message=f"Error durante la descarga (código {e.returncode})",
                error=e.stderr or str(e)
            )
        
        except FileNotFoundError as e:
            return DownloadResult(
                success=False,
                message="No se pudo ejecutar yt-dlp. Verifica que esté instalado.",
                error=str(e)
            )
        
        except Exception as e:
            return DownloadResult(
                success=False,
                message=f"Error inesperado: {type(e).__name__}",
                error=str(e)
            )
