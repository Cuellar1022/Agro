// Variables globales
let postulacionesData = [];
let currentPage = 1;
const itemsPerPage = 6;
let filteredData = [];
let userData = null;
let refreshInterval;

// Función para cargar datos del usuario
async function loadUserData() {
    try {
        const response = await fetch('/get_user_session');
        if (response.ok) {
            const data = await response.json();
            if (data.success && data.user) {
                userData = data.user;
                console.log('Usuario cargado:', userData);
            }
        }
    } catch (error) {
        console.error('Error cargando datos del usuario:', error);
    }
}

// Función para cargar postulaciones desde el servidor
async function loadPostulacionesFromServer() {
    try {
        showLoadingState();
        const response = await fetch('/api/postulaciones');
        
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                postulacionesData = data.postulaciones || [];
                showToast('success', 'Actualizado', 'Postulaciones cargadas correctamente');
            } else {
                postulacionesData = [];
                showToast('error', 'Error', data.error || 'Error al cargar postulaciones');
            }
        } else if (response.status === 403) {
            showToast('error', 'Acceso Denegado', 'No tienes permisos para ver las postulaciones');
            postulacionesData = [];
        } else {
            throw new Error(`Error del servidor: ${response.status}`);
        }
    } catch (error) {
        console.error('Error cargando postulaciones:', error);
        postulacionesData = [];
        showToast('error', 'Error de Conexión', 'No se pudieron cargar las postulaciones');
    }
    
    filteredData = [...postulacionesData];
    renderPostulaciones();
    updateTabCounts();
    hideLoadingState();
}

// Función para mostrar estado de carga
function showLoadingState() {
    const container = document.getElementById('postulacionesList');
    container.innerHTML = `
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p>Cargando postulaciones...</p>
        </div>
    `;
}

function hideLoadingState() {
    // Se oculta automáticamente cuando se renderiza el contenido
}

// Función para renderizar postulaciones
function renderPostulaciones() {
    const container = document.getElementById('postulacionesList');
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageData = filteredData.slice(startIndex, endIndex);

    if (pageData.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-paper-plane"></i>
                <h3>No se encontraron postulaciones</h3>
                <p>No hay postulaciones que coincidan con los filtros seleccionados.</p>
                ${postulacionesData.length === 0 ? '<p><small>Es posible que aún no hayas postulado a ningún trabajo.</small></p>' : ''}
            </div>
        `;
        updatePagination();
        return;
    }

    container.innerHTML = pageData.map(postulacion => `
        <div class="postulacion-card" data-id="${postulacion.id}" data-estado="${postulacion.estado}">
            ${postulacion.estado === 'Aceptada' && isRecent(postulacion.ultimaActualizacion) ? 
                '<div class="notificacion-badge">NUEVO</div>' : ''}
            
            <div class="postulacion-header">
                <div>
                    <div class="postulacion-title">${postulacion.titulo}</div>
                    <div class="agricultor-info">
                        <i class="fas fa-seedling"></i>
                        ${postulacion.agricultor}
                    </div>
                </div>
                <div class="postulacion-status status-${postulacion.estado.toLowerCase()}">
                    ${getStatusIcon(postulacion.estado)}
                    ${postulacion.estado}
                </div>
            </div>

            <div class="postulacion-details">
                <div class="detail-item">
                    <i class="fas fa-calendar-plus"></i>
                    <span>Postulado: ${formatDate(postulacion.fechaPostulacion)}</span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-dollar-sign"></i>
                    <span>${formatCurrency(postulacion.pago)}/día</span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>${postulacion.ubicacion}</span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-clock"></i>
                    <span>${postulacion.duracion}</span>
                </div>
                ${postulacion.fechaInicio ? `
                    <div class="detail-item">
                        <i class="fas fa-play-circle"></i>
                        <span>Inicia: ${formatDate(postulacion.fechaInicio)}</span>
                    </div>
                ` : ''}
                ${postulacion.mensajes > 0 ? `
                    <div class="detail-item">
                        <i class="fas fa-envelope"></i>
                        <span>${postulacion.mensajes} mensaje${postulacion.mensajes !== 1 ? 's' : ''}</span>
                    </div>
                ` : ''}
            </div>

            <div class="postulacion-timeline">
                ${generateTimeline(postulacion)}
            </div>

            ${postulacion.motivoRechazo ? `
                <div class="rechazo-info">
                    <i class="fas fa-info-circle"></i>
                    <span><strong>Motivo:</strong> ${postulacion.motivoRechazo}</span>
                </div>
            ` : ''}

            ${postulacion.calificacionRecibida ? `
                <div class="calificacion-final">
                    <i class="fas fa-star"></i>
                    <span>Calificación recibida: ${generateStars(postulacion.calificacionRecibida)} ${postulacion.calificacionRecibida}.0</span>
                </div>
            ` : ''}

            <div class="postulacion-footer">
                <div class="postulacion-actions">
                    <button class="action-btn" onclick="showPostulacionDetails(${postulacion.id})">
                        <i class="fas fa-eye"></i> Ver Detalles
                    </button>
                    ${postulacion.mensajes > 0 ? `
                        <button class="action-btn" onclick="openMessages(${postulacion.agricultorId})">
                            <i class="fas fa-comments"></i> Mensajes
                        </button>
                    ` : ''}
                    ${postulacion.estado === 'Aceptada' ? `
                        <button class="action-btn" onclick="viewContract(${postulacion.id})">
                            <i class="fas fa-file-contract"></i> Contrato
                        </button>
                    ` : ''}
                    ${postulacion.estado === 'Pendiente' ? `
                        <button class="action-btn btn-danger" onclick="cancelarPostulacion(${postulacion.id})">
                            <i class="fas fa-times"></i> Cancelar
                        </button>
                    ` : ''}
                </div>
            </div>
        </div>
    `).join('');

    updatePagination();
    addCardAnimations();
}

// Función para obtener icono del estado
function getStatusIcon(estado) {
    const icons = {
        'Pendiente': '<i class="fas fa-hourglass-half"></i>',
        'Aceptada': '<i class="fas fa-check-circle"></i>',
        'Rechazada': '<i class="fas fa-times-circle"></i>',
        'Finalizada': '<i class="fas fa-flag-checkered"></i>'
    };
    return icons[estado] || '<i class="fas fa-question-circle"></i>';
}

// Función para generar timeline de la postulación
function generateTimeline(postulacion) {
    const items = [];
    
    items.push(`
        <div class="timeline-item">
            <i class="fas fa-paper-plane"></i>
            <span>Postulación enviada - ${formatDateTime(postulacion.fechaPostulacion)}</span>
        </div>
    `);

    if (postulacion.estado === 'Aceptada') {
        items.push(`
            <div class="timeline-item">
                <i class="fas fa-check"></i>
                <span>Postulación aceptada - ${formatDateTime(postulacion.ultimaActualizacion)}</span>
            </div>
        `);
        if (postulacion.fechaInicio) {
            const fechaInicio = new Date(postulacion.fechaInicio);
            const now = new Date();
            if (fechaInicio > now) {
                items.push(`
                    <div class="timeline-item">
                        <i class="fas fa-calendar-check"></i>
                        <span>Trabajo programado para ${formatDate(postulacion.fechaInicio)}</span>
                    </div>
                `);
            }
        }
    } else if (postulacion.estado === 'Rechazada') {
        items.push(`
            <div class="timeline-item">
                <i class="fas fa-times"></i>
                <span>Postulación rechazada - ${formatDateTime(postulacion.ultimaActualizacion)}</span>
            </div>
        `);
    } else if (postulacion.estado === 'Finalizada') {
        items.push(`
            <div class="timeline-item">
                <i class="fas fa-check-double"></i>
                <span>Trabajo completado - ${formatDateTime(postulacion.fechaFin || postulacion.ultimaActualizacion)}</span>
            </div>
        `);
    }

    return items.join('');
}

// Función para verificar si una fecha es reciente
function isRecent(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffHours = (now - date) / (1000 * 60 * 60);
    return diffHours < 24; // Menos de 24 horas
}

// Funciones de formato
function formatDate(dateString) {
    if (!dateString) return 'Fecha no disponible';
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

function formatDateTime(dateString) {
    if (!dateString) return 'Fecha no disponible';
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
    };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

function formatCurrency(amount) {
    if (!amount) return '$0';
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
}

function generateStars(rating) {
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        stars += i <= rating ? '<i class="fas fa-star"></i>' : '<i class="far fa-star"></i>';
    }
    return stars;
}

// Función para mostrar detalles de la postulación
function showPostulacionDetails(postulacionId) {
    const postulacion = postulacionesData.find(p => p.id === postulacionId);
    if (!postulacion) return;

    const modal = document.getElementById('detalleModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');

    modalTitle.textContent = `Detalles: ${postulacion.titulo}`;
    
    modalBody.innerHTML = `
        <div class="modal-postulacion-details">
            <div class="detail-section">
                <h4><i class="fas fa-briefcase"></i> Información del Trabajo</h4>
                <div class="detail-grid">
                    <div class="detail-row">
                        <span class="label">Agricultor:</span>
                        <span class="value">${postulacion.agricultor}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Ubicación:</span>
                        <span class="value">${postulacion.ubicacion}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Duración:</span>
                        <span class="value">${postulacion.duracion}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Pago ofrecido:</span>
                        <span class="value payment-highlight">${formatCurrency(postulacion.pago)}/día</span>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h4><i class="fas fa-file-alt"></i> Descripción del Trabajo</h4>
                <p class="description-text">${postulacion.descripcion}</p>
            </div>

            <div class="detail-section">
                <h4><i class="fas fa-timeline"></i> Estado de la Postulación</h4>
                <div class="status-display">
                    <div class="status-current">
                        <span class="status-badge status-${postulacion.estado.toLowerCase()}">${getStatusIcon(postulacion.estado)} ${postulacion.estado}</span>
                        <span class="status-date">Actualizado: ${formatDateTime(postulacion.ultimaActualizacion)}</span>
                    </div>
                </div>
                <div class="timeline-full">
                    ${generateTimeline(postulacion)}
                </div>
            </div>

            ${postulacion.fechaInicio ? `
                <div class="detail-section">
                    <h4><i class="fas fa-calendar-alt"></i> Programación</h4>
                    <div class="schedule-info">
                        <div class="schedule-item">
                            <span class="schedule-label">Fecha de inicio:</span>
                            <span class="schedule-value">${formatDate(postulacion.fechaInicio)}</span>
                        </div>
                        ${postulacion.fechaFin ? `
                            <div class="schedule-item">
                                <span class="schedule-label">Fecha de finalización:</span>
                                <span class="schedule-value">${formatDate(postulacion.fechaFin)}</span>
                            </div>
                        ` : ''}
                    </div>
                </div>
            ` : ''}

            ${postulacion.motivoRechazo ? `
                <div class="detail-section rejection-section">
                    <h4><i class="fas fa-exclamation-triangle"></i> Motivo del Rechazo</h4>
                    <div class="rejection-box">
                        <p>${postulacion.motivoRechazo}</p>
                    </div>
                </div>
            ` : ''}

            ${postulacion.calificacionRecibida ? `
                <div class="detail-section">
                    <h4><i class="fas fa-star"></i> Calificación Final</h4>
                    <div class="rating-display">
                        <div class="stars-large">
                            ${generateStars(postulacion.calificacionRecibida)}
                        </div>
                        <span class="rating-number">${postulacion.calificacionRecibida}.0/5.0</span>
                    </div>
                </div>
            ` : ''}

            <div class="modal-actions">
                ${postulacion.estado === 'Pendiente' ? `
                    <button class="btn btn-danger" onclick="cancelarPostulacion(${postulacion.id})">
                        <i class="fas fa-times"></i> Cancelar Postulación
                    </button>
                ` : ''}
                <button class="btn btn-secondary" onclick="contactarAgricultor(${postulacion.agricultorId})">
                    <i class="fas fa-envelope"></i> Contactar Agricultor
                </button>
                ${postulacion.estado === 'Finalizada' ? `
                    <button class="btn btn-primary" onclick="descargarCertificado(${postulacion.id})">
                        <i class="fas fa-certificate"></i> Certificado de Trabajo
                    </button>
                ` : ''}
            </div>
        </div>
    `;

    modal.classList.add('show');
}

// Funciones de filtrado
function filterByStatus(status) {
    // Actualizar botones activos
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    // Filtrar datos
    if (status === '') {
        filteredData = [...postulacionesData];
    } else {
        filteredData = postulacionesData.filter(p => p.estado === status);
    }

    currentPage = 1;
    renderPostulaciones();
}

function setupSearch() {
    const searchInput = document.getElementById('searchPostulaciones');
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        
        filteredData = postulacionesData.filter(postulacion => 
            postulacion.titulo.toLowerCase().includes(searchTerm) ||
            postulacion.agricultor.toLowerCase().includes(searchTerm) ||
            postulacion.ubicacion.toLowerCase().includes(searchTerm) ||
            (postulacion.descripcion && postulacion.descripcion.toLowerCase().includes(searchTerm))
        );

        currentPage = 1;
        renderPostulaciones();
    });
}

// Actualizar contadores de tabs
function updateTabCounts() {
    const pendientes = postulacionesData.filter(p => p.estado === 'Pendiente').length;
    const aceptadas = postulacionesData.filter(p => p.estado === 'Aceptada').length;
    const rechazadas = postulacionesData.filter(p => p.estado === 'Rechazada').length;
    const finalizadas = postulacionesData.filter(p => p.estado === 'Finalizada').length;
    const favoritos = 0; // Los favoritos se manejan por separado
    const total = postulacionesData.length;

    const tabs = document.querySelectorAll('.tab-btn');
    if (tabs.length >= 6) {
        tabs[0].innerHTML = `<i class="fas fa-list"></i> Todas (${total})`;
        tabs[1].innerHTML = `<i class="fas fa-hourglass-half"></i> Pendientes (${pendientes})`;
        tabs[2].innerHTML = `<i class="fas fa-check-circle"></i> Aceptadas (${aceptadas})`;
        tabs[3].innerHTML = `<i class="fas fa-times-circle"></i> Rechazadas (${rechazadas})`;
        tabs[4].innerHTML = `<i class="fas fa-flag-checkered"></i> Finalizadas (${finalizadas})`;
        tabs[5].innerHTML = `<i class="fas fa-heart"></i> Favoritos (${favoritos})`;
    }
}

// Funciones de paginación
function updatePagination() {
    const totalPages = Math.ceil(filteredData.length / itemsPerPage);
    const paginationInfo = document.querySelector('.pagination-info');
    const prevBtn = document.querySelector('.pagination-btn:first-child');
    const nextBtn = document.querySelector('.pagination-btn:last-child');

    if (paginationInfo) {
        paginationInfo.textContent = `Página ${currentPage} de ${totalPages || 1}`;
    }
    
    if (prevBtn) {
        prevBtn.style.opacity = currentPage === 1 ? '0.5' : '1';
        prevBtn.style.pointerEvents = currentPage === 1 ? 'none' : 'auto';
    }
    
    if (nextBtn) {
        nextBtn.style.opacity = currentPage === totalPages ? '0.5' : '1';
        nextBtn.style.pointerEvents = currentPage === totalPages ? 'none' : 'auto';
    }
}

function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        renderPostulaciones();
        window.scrollTo(0, 0);
    }
}

function nextPage() {
    const totalPages = Math.ceil(filteredData.length / itemsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        renderPostulaciones();
        window.scrollTo(0, 0);
    }
}

// Función de actualización manual
function refreshPostulaciones() {
    const btn = event?.target;
    if (btn) {
        const originalContent = btn.innerHTML;
        btn.innerHTML = '<div class="loading-spinner"></div> Actualizando...';
        btn.disabled = true;

        setTimeout(() => {
            loadPostulacionesFromServer();
            btn.innerHTML = originalContent;
            btn.disabled = false;
        }, 1000);
    } else {
        loadPostulacionesFromServer();
    }
}

// Sistema de notificaciones Toast
function showToast(type, title, message) {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const iconMap = {
        success: 'fa-check-circle',
        info: 'fa-info-circle',
        warning: 'fa-exclamation-triangle',
        error: 'fa-times-circle'
    };

    toast.innerHTML = `
        <div class="toast-header">
            <i class="fas ${iconMap[type]} toast-icon"></i>
            <span class="toast-title">${title}</span>
        </div>
        <div class="toast-message">${message}</div>
    `;

    container.appendChild(toast);

    // Mostrar toast
    setTimeout(() => toast.classList.add('show'), 100);

    // Remover toast después de 5 segundos
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            if (container.contains(toast)) {
                container.removeChild(toast);
            }
        }, 300);
    }, 5000);
}

// Funciones de acciones
async function cancelarPostulacion(postulacionId) {
    const postulacion = postulacionesData.find(p => p.id === postulacionId);
    if (!postulacion) return;

    if (confirm(`¿Estás seguro de que deseas cancelar tu postulación para "${postulacion.titulo}"?`)) {
        try {
            const response = await fetch(`/api/postulaciones/${postulacionId}/cancelar`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                showToast('success', 'Cancelada', 'Postulación cancelada exitosamente');
                loadPostulacionesFromServer();
                closeModal();
            } else {
                throw new Error('Error al cancelar');
            }
        } catch (error) {
            console.error('Error cancelando postulación:', error);
            showToast('error', 'Error', 'No se pudo cancelar la postulación');
        }
    }
}

function contactarAgricultor(agricultorId) {
    showToast('info', 'Funcionalidad en desarrollo', 'El sistema de mensajería estará disponible pronto');
}

function openMessages(agricultorId) {
    showToast('info', 'Funcionalidad en desarrollo', 'El chat estará disponible pronto');
}

function viewContract(postulacionId) {
    const postulacion = postulacionesData.find(p => p.id === postulacionId);
    if (postulacion) {
        showToast('info', 'Funcionalidad en desarrollo', 'Los contratos estarán disponibles pronto');
    }
}

function descargarCertificado(postulacionId) {
    const postulacion = postulacionesData.find(p => p.id === postulacionId);
    if (postulacion) {
        showToast('info', 'Funcionalidad en desarrollo', 'Los certificados estarán disponibles pronto');
    }
}

// Funciones de animación
function addCardAnimations() {
    const cards = document.querySelectorAll('.postulacion-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Funciones de modal
function closeModal() {
    const modal = document.getElementById('detalleModal');
    if (modal) {
        modal.classList.remove('show');
    }
}

// Función para ir atrás
function goBack() {
    window.location.href = 'index-trabajador.html';
}

// Event listeners
document.addEventListener('click', function(event) {
    const modal = document.getElementById('detalleModal');
    if (event.target === modal) {
        closeModal();
    }
});

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando página de postulaciones...');
    
    loadUserData();
    loadPostulacionesFromServer();
    setupSearch();

    // Animaciones iniciales
    setTimeout(() => {
        const controls = document.querySelector('.controls-section');
        if (controls) {
            controls.style.opacity = '0';
            controls.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                controls.style.transition = 'all 0.6s ease';
                controls.style.opacity = '1';
                controls.style.transform = 'translateY(0)';
            }, 300);
        }
    }, 500);
});