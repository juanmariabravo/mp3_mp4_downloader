// Configuration
const API_BASE_URL = 'http://localhost:8000';
const POLLING_INTERVAL = 1000; // 1 second

// DOM Elements
const form = document.getElementById('downloadForm');
const urlInput = document.getElementById('videoUrl');
const formatRadios = document.getElementsByName('format');
const qualityGroup = document.getElementById('qualityGroup');
const qualitySelect = document.getElementById('quality');
const submitBtn = document.getElementById('downloadBtn');
const progressSection = document.getElementById('progressSection');
const errorSection = document.getElementById('errorSection');
const previewSection = document.getElementById('previewSection');
const taskIdSpan = document.getElementById('taskIdDisplay');
const statusBadge = document.getElementById('statusBadge');
const statusText = document.getElementById('statusText');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const statusMessage = document.getElementById('statusMessage');
const errorMessage = document.getElementById('errorMessage');
const downloadFileBtn = document.getElementById('downloadFileBtn');
const themeToggle = document.getElementById('themeToggle');

// Preview elements
const videoThumbnail = document.getElementById('videoThumbnail');
const videoTitle = document.getElementById('videoTitle');
const videoUploader = document.getElementById('videoUploader');
const videoDuration = document.getElementById('videoDuration');
const videoViews = document.getElementById('videoViews');
const videoDescription = document.getElementById('videoDescription');

// State
let currentTaskId = null;
let pollingInterval = null;
let videoInfo = null;

// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const icon = themeToggle.querySelector('i');
    if (theme === 'dark') {
        icon.className = 'fas fa-sun';
    } else {
        icon.className = 'fas fa-moon';
    }
}

// Event Listeners
themeToggle.addEventListener('click', toggleTheme);

formatRadios.forEach(radio => {
    radio.addEventListener('change', handleFormatChange);
});

form.addEventListener('submit', handleSubmit);
downloadFileBtn.addEventListener('click', handleDownloadFile);
urlInput.addEventListener('blur', loadVideoPreview);
urlInput.addEventListener('paste', () => {
    setTimeout(loadVideoPreview, 100);
});

// Functions
async function loadVideoPreview() {
    const url = urlInput.value.trim();

    if (!url || !url.includes('youtube.com') && !url.includes('youtu.be')) {
        hidePreview();
        return;
    }

    // Add loading state
    urlInput.classList.add('loading');

    try {
        const response = await fetch(`${API_BASE_URL}/download/info?url=${encodeURIComponent(url)}`);

        if (!response.ok) {
            hidePreview();
            return;
        }

        videoInfo = await response.json();
        showPreview(videoInfo);

    } catch (error) {
        console.error('Error loading preview:', error);
        hidePreview();
    } finally {
        urlInput.classList.remove('loading');
    }
}

function showPreview(info) {
    videoThumbnail.src = info.thumbnail;
    videoTitle.textContent = info.title;
    videoUploader.innerHTML = `<i class="fas fa-user"></i> ${info.uploader}`;
    videoDuration.innerHTML = `<i class="fas fa-clock"></i> ${info.duration_string}`;
    videoViews.innerHTML = `<i class="fas fa-eye"></i> ${info.view_count_string} vistas`;
    videoDescription.textContent = info.description;

    previewSection.style.display = 'block';
}

function hidePreview() {
    previewSection.style.display = 'none';
    videoInfo = null;
}

function handleFormatChange(e) {
    const isMp4 = e.target.value === 'mp4';
    qualityGroup.style.display = isMp4 ? 'block' : 'none';
    qualitySelect.required = isMp4;
}

async function handleSubmit(e) {
    e.preventDefault();

    // Clear previous errors
    hideError();
    hideProgress();

    // Get form data
    const url = urlInput.value.trim();
    const format = document.querySelector('input[name="format"]:checked').value;
    const quality = format === 'mp4' ? qualitySelect.value : null;

    // Validate
    if (!url) {
        showError('Por favor ingresa una URL de YouTube');
        return;
    }

    if (format === 'mp4' && !quality) {
        showError('Por favor selecciona una calidad de video');
        return;
    }

    // Prepare request
    const requestData = {
        url: url,
        format: format
    };

    if (quality) {
        requestData.quality = quality;
    }

    console.log('Sending request:', requestData);

    // Disable form
    setFormDisabled(true);

    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/download`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al iniciar la descarga');
        }

        const data = await response.json();
        currentTaskId = data.task_id;

        // Show progress section
        showProgress(data.task_id);

        // Start polling
        startPolling(data.task_id);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
        setFormDisabled(false);
    }
}

function resetForm() {
    // Hacer scroll hacia arriba suavemente
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Limpiar formulario
    form.reset();
    qualityGroup.style.display = 'none';
    
    // Ocultar todas las secciones
    hideError();
    hideProgress();
    hidePreview();
    
    // Resetear estado
    setFormDisabled(false);
    document.getElementById('successActions').style.display = 'none';
    currentTaskId = null;
    videoInfo = null;
    
    // Enfocar en el campo de URL
    urlInput.focus();
}

function handleDownloadFile() {
    if (!currentTaskId) return;

    // Crear un link temporal para descargar el archivo
    window.open(`${API_BASE_URL}/download/file/${currentTaskId}`, '_blank');
}

async function pollTaskStatus(taskId) {
    try {
        const response = await fetch(`${API_BASE_URL}/download/status/${taskId}`);

        if (!response.ok) {
            throw new Error('Error al obtener el estado de la descarga');
        }

        const data = await response.json();
        updateProgress(data);

        // Stop polling if task is completed or failed
        if (data.status === 'completed' || data.status === 'failed') {
            stopPolling();
            setFormDisabled(false);
        }

    } catch (error) {
        console.error('Polling error:', error);
        showError(error.message);
        stopPolling();
        setFormDisabled(false);
    }
}

function startPolling(taskId) {
    // Clear any existing interval
    stopPolling();

    // Immediate poll
    pollTaskStatus(taskId);

    // Start interval
    pollingInterval = setInterval(() => {
        pollTaskStatus(taskId);
    }, POLLING_INTERVAL);
}

function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
}

function showProgress(taskId) {
    taskIdSpan.textContent = `ID: ${taskId}`;
    progressSection.style.display = 'block';
    errorSection.style.display = 'none';

    // Reset progress
    updateProgress({
        status: 'pending',
        progress: 0,
        message: 'Inicializando descarga...'
    });
}

function hideProgress() {
    progressSection.style.display = 'none';
    currentTaskId = null;
}

function updateProgress(data) {
    // Update status badge
    const statusConfig = {
        'pending': { icon: '<i class="fas fa-hourglass-half"></i>', text: 'Pendiente', class: 'pending' },
        'downloading': { icon: '<i class="fas fa-cloud-download-alt"></i>', text: 'Descargando', class: 'downloading' },
        'processing': { icon: '<i class="fas fa-cog fa-spin"></i>', text: 'Procesando', class: 'processing' },
        'completed': { icon: '<i class="fas fa-check-circle"></i>', text: 'Completado', class: 'completed' },
        'failed': { icon: '<i class="fas fa-times-circle"></i>', text: 'Error', class: 'failed' }
    };

    const config = statusConfig[data.status] || statusConfig['pending'];

    statusBadge.className = `status-badge ${config.class}`;

    // Update status text with icon
    const statusIcon = statusBadge.querySelector('.status-icon');
        if (statusIcon) {
            statusIcon.innerHTML = config.icon;
            progressFill.style.width = `${data.progress || 0}%`;
            progressText.textContent = `${data.progress || 0}%`;
    
            // Update status message
            if (data.message) {
                statusMessage.textContent = data.message;
            }
    
            // Show error if failed
            if (data.status === 'failed' && data.error) {
                showError(data.error);
            }
    
            // Show success info if completed
            if (data.status === 'completed') {
                let successMsg = '¡Descarga completada exitosamente!';
                if (data.file_name) {
                    // Remover el task_id del nombre
                    let displayName = data.file_name;
                    if (displayName.includes('_')) {
                        // Formato: task_id_título.ext -> título.ext
                        displayName = displayName.substring(displayName.indexOf('_') + 1);
                    }
                    successMsg += `\nArchivo: ${displayName}`;
                }
                statusMessage.textContent = successMsg;
                document.getElementById('successActions').style.display = 'block';
            }
        }
    }
    
    // Helper functions moved outside updateProgress
    
    function showError(message) {
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
    }
    
    function hideError() {
        errorSection.style.display = 'none';
        errorMessage.textContent = '';
    }
    
    function setFormDisabled(disabled) {
        urlInput.disabled = disabled;
        formatRadios.forEach(radio => radio.disabled = disabled);
        qualitySelect.disabled = disabled;
        submitBtn.disabled = disabled;
    }
    
    // Initialize
    document.addEventListener('DOMContentLoaded', () => {
        console.log('YouTube Downloader Frontend initialized');
        console.log(`API Base URL: ${API_BASE_URL}`);

        // Initialize theme
        initTheme();
    
        // Check if API is reachable
        fetch(`${API_BASE_URL}/health`)
            .then(response => response.json())
            .then(data => {
                console.log('API Health:', data);
            })
            .catch(error => {
                console.error('API not reachable:', error);
                showError('El servidor API no está disponible. Por favor asegúrate de que el backend esté corriendo en http://localhost:8000');
            });
    });
