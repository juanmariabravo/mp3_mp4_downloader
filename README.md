# Descargador de Audio MP3 desde YouTube

Descarga y convierte videos de YouTube a MP3 o MP4 con alta calidad. 
Incluye interfaz de línea de comandos, y próximamente API REST con Celery y frontend web.

## Características

- Descarga audio de videos de YouTube
- Conversión automática a formato MP3
- Calidad de audio máxima (VBR 0)
- Nombre de archivo basado en el título del video
- Manejo de rutas con caracteres especiales

## Requisitos Previos

- Python 3.7 o superior
- Conexión a Internet

## Instalación

1. **Clona o descarga este repositorio**

2. **Crea un entorno virtual (recomendado)**
   ```powershell
   python -m venv venv
   ```

3. **Activa el entorno virtual**
   ```powershell
   .\venv\Scripts\Activate
   ```

4. **Instala las dependencias**
   ```powershell
   pip install -r requirements.txt
   ```

   Esto instalará:
   - `yt-dlp`: Para descargar videos de YouTube
   - `static-ffmpeg`: Incluye ffmpeg y ffprobe para la conversión de audio

## Uso

1. Ejecuta el script:
   ```powershell
   python downloader.py
   ```

2. Pega la URL del video de YouTube cuando se te solicite

3. El archivo MP3 se guardará en la misma carpeta con el nombre del video

## Ejemplo

```
Pega la URL del vídeo/audio a descargar: https://youtu.be/ejemplo
--- Iniciando descarga y conversión para: https://youtu.be/ejemplo ---
--- PROCESO COMPLETADO EXITOSAMENTE ---
```

## Notas

- La primera vez que ejecutes el script, `static-ffmpeg` descargará automáticamente los binarios de ffmpeg necesarios
- Los archivos descargados se guardan con el formato: `Título del vídeo.mp3`
- La calidad de audio está configurada al máximo (VBR 0)

## Solución de Problemas

Si encuentras errores:
- Asegúrate de tener activado el entorno virtual
- Verifica que todas las dependencias estén instaladas: `pip list`
- Comprueba tu conexión a Internet

## Licencia

Este proyecto es para uso educativo. Respeta los derechos de autor al descargar contenido.
