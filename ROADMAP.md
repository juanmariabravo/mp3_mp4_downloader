# Roadmap - Descargador MP3/MP4

## Funcionalidades Implementadas

- [x] Descarga de audio desde YouTube
- [x] Conversión automática a MP3
- [x] Calidad de audio máxima (VBR 0)
- [x] Manejo de rutas con caracteres especiales
- [x] Opción `--no-playlist` para evitar descargas masivas
- [x] Integración con `static-ffmpeg` para conversión
- [x] Gestión de errores y mensajes informativos
- [x] Archivo `requirements.txt` para dependencias
- [x] Documentación básica (README)
- [x] **Vista previa de video**
  - [x] Endpoint GET /download/info para obtener metadatos
  - [x] VideoInfo class con formateo de duración y vistas
  - [x] Integración con yt-dlp --dump-json
  - [x] Miniatura, título, autor, duración, vistas y descripción
  - [x] Carga automática en blur y paste events
- [x] **Descarga de video (MP4)**
- [x] **Selector de calidad de video** (360p, 480p, 720p, 1080p, Best)
- [x] **Menú interactivo CLI** con emojis y formato mejorado
- [x] **Merge correcto de audio y video** en formato MP4

## Objetivos a Futuro

### Fase 1: Expansión de Formatos COMPLETADA
- [x] **Soporte para descarga de video (MP4)**
  - [x] Implementar opción de descarga en MP4
  - [x] Permitir selección de calidad de video (720p, 1080p, 4K)
  - [ ] Opción para descargar solo video sin audio
  - [x] Combinar video y audio en diferentes calidades

### Fase 2: Interfaz de Usuario COMPLETADA
- [x] **Frontend Web**
  - [x] Crear interfaz web con HTML/CSS/JavaScript
  - [x] Formulario para pegar URLs
  - [x] Selector de formato (MP3/MP4)
  - [x] Selector de calidad
  - [x] Barra de progreso en tiempo real
  - [x] Polling automático cada 1 segundo
  - [x] Descarga de archivos desde el navegador
  - [x] Iconos profesionales con Font Awesome
  - [x] Diseño responsive
  - [x] Vista previa de información del video con miniatura
  - [x] Carga automática de metadatos al pegar URL
  - [x] Scroll suave al resetear formulario
  - [ ] Historial de descargas

- [x] **Backend API**
  - [x] API REST con FastAPI
  - [x] Endpoints para:
    - [x] `POST /download` - Iniciar descarga
    - [x] `GET /status/{task_id}` - Consultar progreso
    - [x] `GET /download/file/{task_id}` - Descargar archivo
    - [x] `GET /download/info?url=...` - Obtener metadatos del video
    - [ ] `GET /history` - Historial de descargas
  - [x] Validación de URLs con Pydantic
  - [x] Gestión de tareas con TaskManager
  - [x] Documentación automática (Swagger/ReDoc)
  - [x] CORS configurado
  - [x] Archivos guardados con título original

### Fase 3: Sistema de Colas
- [ ] **Integración de Celery**
  - [ ] Configurar Celery con Redis/RabbitMQ
  - [ ] Crear tareas asíncronas para descargas
  - [ ] Sistema de prioridades en colas
  - [ ] Manejo de reintentos automáticos
  - [ ] Notificaciones de finalización

### Fase 4: Descarga de Listas
- [ ] **Soporte para Playlists**
  - [ ] Descargar listas completas de YouTube
  - [ ] Selector de videos individuales de una lista
  - [ ] Descarga por lotes con límite configurable
  - [ ] Organización automática en carpetas por playlist
  - [ ] Descarga de canales completos
  - [ ] Filtros por duración, fecha, etc.

## Mejoras Propuestas

### Funcionalidad
- [ ] Descarga de subtítulos
- [ ] Extracción de metadatos (artista, título, etc.)
- [ ] Normalización de audio
- [ ] Recorte de audio (inicio/fin)
- [ ] Conversión entre formatos (MP3, FLAC, WAV, AAC)

### Interfaz
- [x] Modo oscuro/claro
- [ ] Soporte multiidioma (ES/EN)
- [ ] Aplicación de escritorio con Electron
- [ ] Extensión de navegador
- [ ] App móvil (React Native)

### Rendimiento
- [ ] Caché de metadatos
- [ ] Descarga paralela de múltiples archivos
- [ ] Compresión de archivos descargados
- [ ] Limpieza automática de archivos antiguos
- [ ] Optimización de uso de memoria

### Seguridad
- [ ] Rate limiting en API
- [ ] Validación estricta de URLs
- [ ] Escaneo de virus en archivos descargados
- [ ] Logs de auditoría
- [ ] Sistema de cuotas por usuario

### DevOps
- [ ] Dockerización del proyecto
- [ ] CI/CD con GitHub Actions
- [ ] Tests unitarios y de integración
- [ ] Monitoreo con Prometheus/Grafana
- [ ] Despliegue en la nube (AWS/Azure/GCP)

## Arquitectura Futura Propuesta

```
┌─────────────────┐
│  Frontend Web   │
│  (React/Vue)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   API Gateway   │
│   (FastAPI)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌─────────────────┐
│  Celery Worker  │◄────►│  Redis/RabbitMQ │
│  (Descargador)  │      │  (Cola Tareas)  │
└────────┬────────┘      └─────────────────┘
         │
         ▼
┌─────────────────┐
│  Almacenamiento │
│  (Local/S3)     │
└─────────────────┘
```

## Notas de Desarrollo

### Prioridad Alta
1. Soporte MP4
2. Frontend básico
3. API REST

### Prioridad Media
1. Sistema de colas con Celery
2. Descarga de playlists
3. Dockerización

### Prioridad Baja
1. App móvil
2. Extensión de navegador
3. Soporte para otras plataformas

## Changelog

### v0.3.0 - API REST + Refactorización (15 Diciembre 2025)
- **API REST completa con FastAPI**
  - Endpoints POST /download y GET /download/status/{task_id}
  - Documentación automática con Swagger UI y ReDoc
  - Modelos Pydantic para validación
  - CORS configurado para frontend
  - TaskManager para gestión de descargas asíncronas
- **Refactorización completa del código**
  - Módulo `core/` con DownloaderService reutilizable
  - Configuración centralizada con enums tipados
  - CLI refactorizado usando el core
  - 8 tests unitarios con pytest
  - Estructura modular preparada para escalabilidad
- Documentación completa de la API con ejemplos

### v0.2.0 - Soporte MP4 (15 Diciembre 2025)
- Agregado soporte completo para descarga de video MP4
- Selector interactivo de calidad (360p - 1080p - Best)
- Menú CLI mejorado con emojis y mejor UX
- Corregido merge de audio y video en MP4
- Documentación actualizada con ejemplos y troubleshooting

### v0.1.0 - Versión Inicial (15 Diciembre 2025)
- Versión inicial con descarga de MP3
- Integración con yt-dlp y static-ffmpeg
- Línea de comandos básica

---

**Última actualización:** 15 de Diciembre de 2025
