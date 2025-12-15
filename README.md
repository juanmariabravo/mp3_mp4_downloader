# Descargador de YouTube - MP3 & MP4

Descarga y convierte videos de YouTube a MP3 o MP4 con alta calidad. 
Incluye interfaz de línea de comandos (CLI), API REST con FastAPI y frontend web interactivo.

## Características

- **Descarga de audio (MP3)** - Extrae solo el audio en máxima calidad
- **Descarga de video (MP4)** - Video con audio en diferentes resoluciones
- **Selector de calidad** - Elige entre 360p, 480p, 720p, 1080p o la mejor disponible
- **3 formas de usar:**
  - **CLI interactiva** - Menú en terminal
  - **API REST** - Endpoints HTTP con FastAPI
  - **Frontend web** - Interfaz gráfica en el navegador
- **Solo videos individuales** - Evita descargas masivas de playlists
- **Nombres automáticos** - Archivos nombrados con el título del video
- **Progreso en tiempo real** - Seguimiento de descargas (API/Frontend)
- **Manejo de errores** - Mensajes claros de estado y errores

## Requisitos Previos

- Python 3.7 o superior
- Conexión a Internet

## Instalación

1. **Clona o descarga este repositorio**
   ```powershell
   git clone https://github.com/juanmariabravo/mp3_mp4_downloader.git
   cd mp3_mp4_downloader
   ```

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
   - `static-ffmpeg`: Incluye ffmpeg y ffprobe para conversión

## Uso

### Opción 1: Interfaz de Línea de Comandos (CLI)

1. **Ejecuta el script:**
   ```powershell
   python downloader.py
   ```

2. **Selecciona el formato** (MP3 o MP4)

3. **Si elegiste MP4, selecciona la calidad:**
   - 360p (Baja calidad)
   - 480p (Calidad media)
   - 720p HD (Recomendado)
   - 1080p Full HD
   - Mejor calidad disponible

4. **Pega la URL del video de YouTube**

5. **El archivo se guardará en la carpeta `downloads/`** con el nombre del video

### Opción 2: API REST

1. **Inicia el servidor API:**
   ```powershell
   uvicorn api.main:app --reload
   ```

2. **Accede a la documentación interactiva:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Endpoints disponibles:**
   - `POST /download` - Inicia una descarga
   - `GET /download/status/{task_id}` - Consulta el estado
   - `GET /health` - Health check

Ver [api/README.md](api/README.md) para ejemplos de uso.

### Opción 3: Frontend Web

1. **Inicia el servidor API** (si no está corriendo):
   ```powershell
   uvicorn api.main:app --reload
   ```

2. **Abre el frontend** en tu navegador:
   ```powershell
   Start-Process frontend\index.html
   ```
   O simplemente abre `frontend/index.html` haciendo doble clic.

3. **Usa la interfaz web:**
   - Pega la URL del video de YouTube
   - Selecciona MP3 o MP4
   - Si elegiste MP4, selecciona la calidad
   - Haz clic en "Descargar" y observa el progreso en tiempo real
   - Los archivos se guardan en `downloads/`

Ver [frontend/README.md](frontend/README.md) para más detalles.

## Ejemplo de Uso

```
==================================================
DESCARGADOR DE YOUTUBE - MP3 & MP4
==================================================

Selecciona el formato de descarga:
  1. MP3 (Solo audio)
  2. MP4 (Video con audio)

Elige una opción (1 o 2): 2

Selecciona la calidad del video:
  1. 360p (Baja calidad)
  2. 480p (Calidad media)
  3. 720p HD (Recomendado)
  4. 1080p Full HD
  5. Mejor calidad disponible

Elige una opción (1-5) [Por defecto: 3]: 3

Pega la URL del vídeo a descargar:
URL: https://youtu.be/ejemplo

--- Iniciando descarga MP4 para: https://youtu.be/ejemplo ---
Formato: MP4 | Calidad: 720p HD (Recomendado)

--- DESCARGA COMPLETADA EXITOSAMENTE ---
```

## Notas Importantes

- La primera vez que ejecutes el script, `static-ffmpeg` descargará automáticamente los binarios de ffmpeg necesarios (~50 MB)
- Los archivos descargados se guardan en la misma carpeta del script con el formato: `Título del vídeo.mp3` o `.mp4`
- **MP3:** Calidad de audio configurada al máximo (VBR 0)
- **MP4:** El video incluye audio correctamente sincronizado
- URLs con parámetros de playlist solo descargan el video individual (gracias a `--no-playlist`)

## Formatos Soportados

| Formato | Extensión | Calidades Disponibles | Descripción |
|---------|-----------|----------------------|-------------|
| Audio | `.mp3` | Máxima (VBR 0) | Solo audio, sin video |
| Video | `.mp4` | 360p, 480p, 720p, 1080p, Best | Video + Audio |

## 🔧 Solución de Problemas

### Error: "Module not found"
```powershell
# Asegúrate de activar el entorno virtual
.\venv\Scripts\Activate.ps1

# Reinstala las dependencias
pip install -r requirements.txt
```

### Error: "ffmpeg not found"
El script descarga ffmpeg automáticamente. Si falla:
```powershell
pip uninstall static-ffmpeg
pip install static-ffmpeg
```

### Video sin audio
Asegúrate de usar la última versión del código. El problema ha sido corregido.

## Próximas Funcionalidades

- ~~API REST con FastAPI~~ ✅ Completado (v0.3.0)
- ~~Frontend web interactivo~~ ✅ Completado (v0.3.0)
- Sistema de colas persistente con Celery
- WebSockets para progreso en tiempo real
- Descarga de playlists completas
- Autenticación y autorización
- Contenedores Docker para deployment

Ver [ROADMAP.md](ROADMAP.md) para más detalles.

## Licencia

Este proyecto es para uso educativo. Respeta los derechos de autor al descargar contenido.
