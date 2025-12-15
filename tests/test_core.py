"""
Tests unitarios para el módulo core.
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import DownloaderService, Config, VideoQuality
from core.config import FormatType


class TestConfig(unittest.TestCase):
    """Tests para la clase Config."""
    
    def test_default_config(self):
        """Verifica que la configuración por defecto se inicialice correctamente."""
        config = Config.get_default()
        
        self.assertEqual(config.AUDIO_QUALITY, '0')
        self.assertTrue(config.NO_PLAYLIST)
        self.assertEqual(config.OUTPUT_TEMPLATE, '%(title)s.%(ext)s')
        self.assertIsNotNone(config.VIDEO_QUALITIES)
        self.assertEqual(len(config.VIDEO_QUALITIES), 5)
    
    def test_video_qualities(self):
        """Verifica que las calidades de video estén definidas correctamente."""
        config = Config.get_default()
        
        self.assertIn('1', config.VIDEO_QUALITIES)
        self.assertEqual(config.VIDEO_QUALITIES['1']['resolution'], '360')
        self.assertIn('description', config.VIDEO_QUALITIES['1'])


class TestDownloaderService(unittest.TestCase):
    """Tests para la clase DownloaderService."""
    
    @patch('core.downloader.run.get_or_fetch_platform_executables_else_raise')
    def setUp(self, mock_ffmpeg):
        """Configura el entorno de pruebas."""
        # Mockear la inicialización de ffmpeg
        mock_ffmpeg.return_value = ('/path/to/ffmpeg', '/path/to/ffprobe')
        self.service = DownloaderService()
    
    def test_initialization(self):
        """Verifica que el servicio se inicialice correctamente."""
        self.assertIsNotNone(self.service.config)
        self.assertIsInstance(self.service.config, Config)
    
    @patch('core.downloader.subprocess.run')
    def test_download_audio_success(self, mock_run):
        """Test de descarga exitosa de audio."""
        # Configurar el mock para simular éxito
        mock_process = MagicMock()
        mock_process.stdout = "Download completed"
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        
        result = self.service.download_audio("https://www.youtube.com/watch?v=gEHK00H_PxQ&list=RDgEHK00H_PxQ&start_radio=1")
        
        self.assertTrue(result.success)
        self.assertIn("exitosa", result.message.lower())
        mock_run.assert_called_once()
    
    @patch('core.downloader.subprocess.run')
    def test_download_video_success(self, mock_run):
        """Test de descarga exitosa de video."""
        # Configurar el mock para simular éxito
        mock_process = MagicMock()
        mock_process.stdout = "Download completed"
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        
        result = self.service.download_video(
            "https://www.youtube.com/watch?v=gEHK00H_PxQ&list=RDgEHK00H_PxQ&start_radio=1",
            quality=VideoQuality.HD
        )
        
        self.assertTrue(result.success)
        self.assertIn("exitosa", result.message.lower())
        mock_run.assert_called_once()
    
    def test_video_quality_enum(self):
        """Verifica que el enum VideoQuality funcione correctamente."""
        self.assertEqual(VideoQuality.LOW.value, '360')
        self.assertEqual(VideoQuality.HD.value, '720')
        self.assertEqual(VideoQuality.FULL_HD.value, '1080')
        self.assertEqual(VideoQuality.BEST.value, 'best')


class TestDownloadResult(unittest.TestCase):
    """Tests para la clase DownloadResult."""
    
    def test_success_result(self):
        """Verifica la creación de un resultado exitoso."""
        from core.downloader import DownloadResult
        
        result = DownloadResult(success=True, message="Test success")
        
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Test success")
        self.assertIn("SUCCESS", repr(result))
    
    def test_failure_result(self):
        """Verifica la creación de un resultado fallido."""
        from core.downloader import DownloadResult
        
        result = DownloadResult(
            success=False,
            message="Test failed",
            error="Error details"
        )
        
        self.assertFalse(result.success)
        self.assertEqual(result.message, "Test failed")
        self.assertEqual(result.error, "Error details")
        self.assertIn("FAILED", repr(result))


if __name__ == '__main__':
    unittest.main()
