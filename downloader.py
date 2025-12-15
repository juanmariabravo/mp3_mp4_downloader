import subprocess
import os
import sys
from static_ffmpeg import run

# --- Configuración ---
# Descargar y obtener las rutas de ffmpeg y ffprobe usando static-ffmpeg
ffmpeg_path, ffprobe_path = run.get_or_fetch_platform_executables_else_raise()

# Calidades de video disponibles
VIDEO_QUALITIES = {
    '1': {'resolution': '360', 'description': '360p (Baja calidad)'},
    '2': {'resolution': '480', 'description': '480p (Calidad media)'},
    '3': {'resolution': '720', 'description': '720p HD (Recomendado)'},
    '4': {'resolution': '1080', 'description': '1080p Full HD'},
    '5': {'resolution': 'best', 'description': 'Mejor calidad disponible'}
}

def download_media(url, format_type='mp3', video_quality='720'):
    """
    Descarga y convierte un vídeo de YouTube a MP3 o MP4.
    
    Args:
        url (str): URL del vídeo de YouTube
        format_type (str): 'mp3' para audio o 'mp4' para video
        video_quality (str): Resolución del video (solo aplica para MP4)
    """
    print(f"\n--- Iniciando descarga {format_type.upper()} para: {url} ---")

    # Configuración base del comando
    command = [
        sys.executable,
        '-m', 'yt_dlp',
        '--no-playlist',  # Solo descarga el video individual
        '--ffmpeg-location', os.path.dirname(ffmpeg_path),
        '--output', '%(title)s.%(ext)s',
        url
    ]

    # Configuración específica según el formato
    if format_type == 'mp3':
        # Para MP3: extraer solo audio
        command.extend([
            '-x',  # Extraer audio
            '--audio-format', 'mp3',
            '--audio-quality', '0',  # Mejor calidad de audio
        ])
        print("Formato: MP3 | Calidad: Máxima (VBR 0)")
    
    elif format_type == 'mp4':
        # Para MP4: descargar video con audio
        if video_quality == 'best':
            format_string = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'
        else:
            format_string = f'bestvideo[ext=mp4][height<={video_quality}]+bestaudio[ext=m4a]/bestvideo[height<={video_quality}]+bestaudio/best[height<={video_quality}]'
        
        command.extend([
            '-f', format_string,
            '--merge-output-format', 'mp4',
            '--postprocessor-args', 'ffmpeg:-c:v copy -c:a aac',  # Asegurar que el audio se copie correctamente
        ])
        quality_desc = VIDEO_QUALITIES.get(next((k for k, v in VIDEO_QUALITIES.items() if v['resolution'] == video_quality), '3'))['description']
        print(f"Formato: MP4 | Calidad: {quality_desc}")

    try:
        # Ejecutar el comando
        process = subprocess.run(
            command, 
            check=True, 
            capture_output=True, 
            text=True, 
            encoding='utf-8', 
            errors='replace'
        )
        
        print("\n --- DESCARGA COMPLETADA EXITOSAMENTE ---")
        print(process.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"\n!!! ERROR DURANTE LA DESCARGA/CONVERSIÓN !!!")
        print(f"Código de retorno: {e.returncode}")
        print(f"Salida de error: {e.stderr}")
    except FileNotFoundError as e:
        print(f"\n!!! ERROR: No se pudo ejecutar el comando. Asegúrate de que los requisitos estén instalados. !!!")

def show_menu():
    """Muestra el menú interactivo para seleccionar formato y calidad."""
    print("\n" + "="*50)
    print("DESCARGADOR DE YOUTUBE - MP3 & MP4")
    print("="*50)
    
    # Selección de formato
    print("\nSelecciona el formato de descarga:")
    print("  1. MP3 (Solo audio)")
    print("  2. MP4 (Video con audio)")
    
    format_choice = input("\nElige una opción (1 o 2): ").strip()
    
    if format_choice == '1':
        format_type = 'mp3'
        video_quality = None
    elif format_choice == '2':
        format_type = 'mp4'
        
        # Selección de calidad de video
        print("\nSelecciona la calidad del video:")
        for key, value in VIDEO_QUALITIES.items():
            print(f"  {key}. {value['description']}")
        
        quality_choice = input("\nElige una opción (1-5) [Por defecto: 3]: ").strip()
        quality_choice = quality_choice if quality_choice in VIDEO_QUALITIES else '3'
        video_quality = VIDEO_QUALITIES[quality_choice]['resolution']
    else:
        print("Opción inválida. Usando MP3 por defecto.")
        format_type = 'mp3'
        video_quality = None
    
    # Solicitar URL
    print("\nPega la URL del vídeo a descargar:")
    url = input("URL: ").strip()
    
    return url, format_type, video_quality


if __name__ == '__main__':
    """Punto de entrada principal del programa."""
    try:
        url, format_type, video_quality = show_menu()
        
        if url:
            if format_type == 'mp3':
                download_media(url, format_type='mp3')
            else:
                download_media(url, format_type='mp4', video_quality=video_quality)
        else:
            print("URL no proporcionada. Saliendo.")
    
    except KeyboardInterrupt:
        print("\n\nDescarga cancelada por el usuario.")
    except Exception as e:
        print(f"\nError inesperado: {e}")
