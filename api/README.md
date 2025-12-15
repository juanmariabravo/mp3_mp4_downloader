# API REST - YouTube Downloader

API REST para descargar audio (MP3) y video (MP4) desde YouTube.

## Inicio Rápido

### 1. Iniciar el servidor

```powershell
# Desde el directorio raíz del proyecto
python -m uvicorn api.main:app --reload --port 8000
```

### 2. Acceder a la documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### POST /download
Inicia una descarga de YouTube.

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "format": "mp3",
  "quality": null
}
```

**Response (202 Accepted):**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Descarga de MP3 iniciada",
  "created_at": "2025-12-15T10:30:00"
}
```

### GET /download/status/{task_id}
Consulta el estado de una descarga.

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100.0,
  "message": "Descarga completada exitosamente",
  "created_at": "2025-12-15T10:30:00",
  "completed_at": "2025-12-15T10:32:15",
  "file_path": "downloads/video_title.mp3",
  "error": null
}
```

## Ejemplos de Uso

### Con cURL

**Descargar MP3:**
```bash
curl -X POST "http://localhost:8000/download" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "format": "mp3"
  }'
```

**Descargar MP4 en 720p:**
```bash
curl -X POST "http://localhost:8000/download" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "format": "mp4",
    "quality": "720"
  }'
```

**Consultar estado:**
```bash
curl "http://localhost:8000/download/status/{task_id}"
```

### Con Python (requests)

```python
import requests
import time

# Iniciar descarga
response = requests.post(
    "http://localhost:8000/download",
    json={
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "format": "mp3"
    }
)

task_id = response.json()["task_id"]
print(f"Task ID: {task_id}")

# Consultar estado cada 2 segundos
while True:
    status_response = requests.get(
        f"http://localhost:8000/download/status/{task_id}"
    )
    status_data = status_response.json()
    
    print(f"Estado: {status_data['status']} - {status_data['progress']}%")
    
    if status_data['status'] in ['completed', 'failed']:
        break
    
    time.sleep(2)

print(f"Archivo: {status_data['file_path']}")
```

### Con JavaScript (fetch)

```javascript
// Iniciar descarga
const response = await fetch('http://localhost:8000/download', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    format: 'mp3'
  })
});

const { task_id } = await response.json();

// Consultar estado
const checkStatus = async (taskId) => {
  const statusResponse = await fetch(
    `http://localhost:8000/download/status/${taskId}`
  );
  return await statusResponse.json();
};

// Polling
const pollStatus = async (taskId) => {
  while (true) {
    const status = await checkStatus(taskId);
    console.log(`${status.status}: ${status.progress}%`);
    
    if (['completed', 'failed'].includes(status.status)) {
      return status;
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
};

const result = await pollStatus(task_id);
console.log('Archivo:', result.file_path);
```

## Formatos y Calidades

### Formatos Soportados
- `mp3`: Solo audio
- `mp4`: Video con audio

### Calidades de Video (solo MP4)
- `360`: 360p (Baja calidad)
- `480`: 480p (Media)
- `720`: 720p HD (Recomendado)
- `1080`: 1080p Full HD
- `best`: Mejor calidad disponible

## Estados de Tareas

- `pending`: Tarea creada, esperando procesamiento
- `downloading`: Descargando contenido
- `processing`: Procesando/convirtiendo archivo
- `completed`: Descarga completada exitosamente
- `failed`: Error durante la descarga

## Configuración

### CORS
Por defecto, la API permite solicitudes desde cualquier origen (`*`). En producción, modifica `api/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-dominio.com"],  # Especificar dominios
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Puerto y Host
Para cambiar el puerto o hacer la API accesible externamente:

```powershell
python -m uvicorn api.main:app --host 0.0.0.0 --port 3000
```

## Limitaciones Actuales

- Las tareas se almacenan en memoria (se pierden al reiniciar)
- No hay límite de rate limiting
- No hay autenticación/autorización
- Los archivos se guardan localmente (no hay storage en la nube)

## Próximas Mejoras

- [ ] Integración con Celery para colas persistentes
- [ ] Base de datos (PostgreSQL/MongoDB) para tareas
- [ ] Autenticación con JWT
- [ ] Rate limiting
- [ ] Endpoint para descargar archivos directamente
- [ ] WebSockets para progreso en tiempo real
- [ ] Storage en S3/Azure Blob
- [ ] Cleanup automático de archivos antiguos

## Licencia

Uso educativo. Respeta los derechos de autor.
