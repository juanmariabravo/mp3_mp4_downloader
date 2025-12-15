import subprocess
import os
import sys
from static_ffmpeg import run

# --- Configuración ---
# Descargar y obtener las rutas de ffmpeg y ffprobe usando static-ffmpeg
ffmpeg_path, ffprobe_path = run.get_or_fetch_platform_executables_else_raise()

def download_audio_as_mp3(url_video):
    """
    Ejecuta yt-dlp para descargar y convertir un vídeo a MP3.
    """
    print(f"--- Iniciando descarga y conversión para: {url_video} ---")

    # Comando para ejecutar yt-dlp:
    # 1. -t mp3: Usa el preset para extraer audio en formato MP3.
    # 2. --audio-quality 0: Configura la calidad más alta para la conversión MP3 (VBR 0).
    # 3. --ffmpeg-location: Le dice a yt-dlp dónde está el ejecutable de ffmpeg.
    # 4. --output: Define el formato de nombre de archivo (ej. 'Título del vídeo.mp3').
    
    # Usar Python con módulo yt-dlp para evitar problemas con rutas con caracteres especiales
    command = [
        sys.executable,  # python.exe
        '-m', 'yt_dlp',
        '-t', 'mp3',
        '--audio-quality', '0',
        '--no-playlist',  # Solo descarga el video individual, no la lista completa
        '--ffmpeg-location', os.path.dirname(ffmpeg_path),
        '--output', '%(title)s.%(ext)s', # Nombra el archivo con el título del vídeo
        url_video
    ]

    try:
        # Ejecuta el comando en el sistema operativo
        # 'check=True' asegura que si hay un error, se lance una excepción
        process = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        print("\n--- PROCESO COMPLETADO EXITOSAMENTE ---")
        print(process.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"\n!!! ERROR DURANTE LA DESCARGA/CONVERSIÓN !!!")
        print(f"Código de retorno: {e.returncode}")
        print(f"Salida de error: {e.stderr}")
    except FileNotFoundError as e:
        print(f"\n!!! ERROR: No se pudo ejecutar el comando. Asegúrate de que los requisitos estén instalados. !!!")


if __name__ == '__main__':
    # --- PRUEBA DEL CÓDIGO ---
    # Reemplaza 'URL_DEL_VIDEO' con una URL de YouTube real (ej. un video de dominio público o de tu propia autoría para pruebas legales)
    test_url = input("Pega la URL del vídeo/audio a descargar: ")
    if test_url:
        download_audio_as_mp3(test_url)
    else:
        print("URL no proporcionada. Saliendo.")