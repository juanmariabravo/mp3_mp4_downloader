"""
Interfaz de línea de comandos para el descargador de YouTube.
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import DownloaderService, Config, VideoQuality
from core.config import FormatType


def show_menu():
    """Muestra el menú interactivo y retorna las opciones seleccionadas."""
    print("\n" + "="*50)
    print("DESCARGADOR DE YOUTUBE - MP3 & MP4")
    print("="*50)
    
    # Selección de formato
    print("\nSelecciona el formato de descarga:")
    print("  1. MP3 (Solo audio)")
    print("  2. MP4 (Video con audio)")
    
    format_choice = input("\nElige una opción (1 o 2): ").strip()
    
    video_quality = None
    
    if format_choice == '1':
        format_type = FormatType.MP3
    elif format_choice == '2':
        format_type = FormatType.MP4
        
        # Selección de calidad de video
        config = Config.get_default()
        print("\nSelecciona la calidad del video:")
        for key, value in config.VIDEO_QUALITIES.items():
            print(f"  {key}. {value['description']}")
        
        quality_choice = input("\nElige una opción (1-5) [Por defecto: 3]: ").strip()
        quality_choice = quality_choice if quality_choice in config.VIDEO_QUALITIES else '3'
        
        # Convertir a enum VideoQuality
        resolution = config.VIDEO_QUALITIES[quality_choice]['resolution']
        video_quality = VideoQuality(resolution)
    else:
        print("Opción inválida. Usando MP3 por defecto.")
        format_type = FormatType.MP3
    
    # Solicitar URL
    print("\nPega la URL del vídeo a descargar:")
    url = input("URL: ").strip()
    
    return url, format_type, video_quality


def main():
    """Función principal del CLI."""
    try:
        # Mostrar menú y obtener opciones
        url, format_type, video_quality = show_menu()
        
        if not url:
            print("URL no proporcionada. Saliendo.")
            return
        
        # Inicializar el servicio de descarga
        print("\nInicializando descargador...")
        downloader = DownloaderService()
        
        # Ejecutar descarga según el formato
        print(f"\n--- Iniciando descarga {format_type.value.upper()} para: {url} ---\n")
        
        if format_type == FormatType.MP3:
            result = downloader.download_audio(url)
        else:
            result = downloader.download_video(url, quality=video_quality)
        
        # Mostrar resultado
        if result.success:
            print(f"\n--- {result.message.upper()} ---")
            if result.output:
                print(result.output)
        else:
            print(f"\n!!! {result.message.upper()} !!!")
            if result.error:
                print(f"Detalles del error:\n{result.error}")
    
    except KeyboardInterrupt:
        print("\n\nDescarga cancelada por el usuario.")
        sys.exit(0)
    
    except Exception as e:
        print(f"\nError inesperado: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
