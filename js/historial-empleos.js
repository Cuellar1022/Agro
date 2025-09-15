// Variables globales
let historialData = [];
let currentPage = 1;
const itemsPerPage = 5;
let filteredData = [];
let userData = null;

// Datos de ejemplo del historial de empleos
const empleosEjemplo = [
    {
        id: 1,
        titulo: "Cosecha de Café Premium",
        empleador: "Finca El Paraíso",
        empleadorId: 101,
        tipo: "Cosecha",
        fechaInicio: "2024-08-15",
        fechaFin: "2024-08-18",
        duracion: "3 días",
        estado: "Completado",
        pago: 150000,
        ubicacion: "Huila, Colombia",
        calificacion: 5,
        comentario: "Excelente trabajador, muy puntual y eficiente",
        descripcion: "Recolección selectiva de café maduro en montaña",
        condiciones: "6:00 AM - 3:00 PM, alimentación incluida",
        coordenadas: { lat: 2.5355, lng: -75.5219 }
    },
    {
        id: 2,
        titulo: "Siembra de Maíz Tecnificado",
        empleador: "Agropecuaria San José",
        empleadorId: 102,
        tipo: "Siembra",
        fechaInicio: "2024-07-20",
        fechaFin: "2024-07-25",
        duracion: "5 días",
        estado: "Completado",
        pago: 225000,
        ubicacion: "Valle del Cauca",
        calificacion: 4,
        comentario: "Buen trabajo, conoce las técnicas modernas",
        descripcion: "Preparación de tierra y siembra tecnificada",
        condiciones: "7:00 AM - 4:00 PM, transporte incluido",
        coordenadas: { lat: 3.4516, lng: -76.5320 }
    },
    {
        id: 3,
        titulo: "Mantenimiento de Invernaderos",
        empleador: "Cultivos del Norte",
        empleadorId: 103,
        tipo: "Mantenimiento",
        fechaInicio: "2024-09-01",
        fechaFin: null,
        duracion: "En curso",
        estado: "En curso",
        pago: 42000,
        ubicacion: "Cundinamarca",
        calificacion: null,
        comentario: null,
        descripcion: "Poda, limpieza y mantenimiento de sistemas",
        condiciones: "8:00 AM - 5:00 PM, tiempo completo",
        coordenadas: { lat: 4.7110, lng: -74.0721 }
    },
    {
        id: 4,
        titulo: "Recolección de Frutas Cítricas",
        empleador: "Huerto Los Naranjos",
        empleadorId: 104,
        tipo: "Recolección",
        fechaInicio: "2024-06-10",
        fechaFin: "2024-06-12",
        duracion: "2 días",
        estado: "Completado",
        pago: 80000,
        ubicacion: "Tolima",
        calificacion: 5,
        comentario: "Muy cuidadoso con las frutas, recomendado",
        descripcion: "Recolección cuidadosa de naranjas y limones",
        condiciones: "5:30 AM - 2:00 PM, pago diario",
        coordenadas: { lat: 4.4389, lng: -75.2322 }
    },
    {
        id: 5,
        titulo: "Poda de Árboles Frutales",
        empleador: "Finca La Esperanza",
        empleadorId: 105,
        tipo: "Mantenimiento",
        fechaInicio: "2024-05-15",
        fechaFin: "2024-05-16",
        duracion: "2 días",
        estado: "Cancelado",
        pago: 0,
        ubicacion: "Risaralda",
        calificacion: null,
        comentario: "Trabajo cancelado por condiciones climáticas",
        descripcion: "Poda técnica de árboles de aguacate",
        condiciones: "7:00 AM - 4:00 PM",
        coordenadas: { lat: 4.8143, lng: -75.6946 }
    }
];

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

// Función para cargar historial desde el servidor
async function loadHistorialFromServer() {
    try {
        const response = await fetch('/api/historial-empleos');
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                historialData = data.empleos;
            } else {
                // Si no hay datos del servidor, usar datos de ejemplo
                historialData = empleosEjemplo;
            }
        } else {
            historialData = empleosEjemplo;
        }
    } catch (error) {
        console.error('Error cargando historial:', error);
        historialData = empleosEjemplo;
    }
    
    filteredData = [...historialData];
    renderHistorial();
    updateStats();
}

// Función para renderizar el historial
function renderHistorial() {
    const container = document.getElementById('historialList');
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageData = filteredData.slice(startIndex, endIndex);

    if (pageData.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-clipboard-list"></i>
                <h3>No se encontraron empleos</h3>
                <p>No hay empleos que coincidan con los filtros seleccionados.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = pageData.map(empleo => `
        <div class="empleo-card" data-id="${empleo.id}">
            <div class="empleo-header">
                <div>
                    <div class="empleo-title">${empleo.titulo}</div>
                    <div class="empleador-info">
                        <i class="fas fa-user-tie"></i>
                        ${empleo.empleador}
                    </div>
                </div>
                <div class="empleo-status status-${empleo.estado.toLowerCase().replace(' ', '-')}">
                    ${getStatusIcon(empleo.estado)}
                    ${empleo.estado}
                </div>
            </div>

            <div class="empleo-details">
                <div class="detail-item">
                    <i class="fas fa-calendar-alt"></i>
                    <span>${formatDateRange(empleo.fechaInicio, empleo.fechaFin)}</span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-clock"></i>
                    <span>${empleo.duracion}</span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>${empleo.ubicacion}</span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-dollar-sign"></i>
                    <span>${formatCurrency(empleo.pago)}</span>
                </div>
            </div>

            ${empleo.calificacion ? `
                <div class="empleo-rating">
                    <div class="rating-stars">
                        ${generateStars(empleo.calificacion)}
                    </div>
                    <span class="rating-value">${empleo.calificacion}.0</span>
                    ${empleo.comentario ? `<span class="rating-comment">"${empleo.comentario}"</span>` : ''}
                </div>
            ` : ''}

            <div class="empleo-footer">
                <div class="empleo-tags">
                    <span class="empleo-tag">${empleo.tipo}</span>
                    ${empleo.estado === 'Completado' ? '<span class="empleo-tag">Finalizado</span>' : ''}
                    ${empleo.calificacion === 5 ? '<span class="empleo-tag">★ Destacado</span>' : ''}
                </div>
                <button class="detail-btn" onclick="showEmpleoDetails(${empleo.id})">
                    <i class="fas fa-eye"></i> Ver Detalles
                </button>
            </div>
        </div>
    `).join('');

    updatePagination();
}

// Función para obtener el icono del estado
function getStatusIcon(estado) {
    const icons = {
        'Completado': '<i class="fas fa-check-circle"></i>',
        'En curso': '<i class="fas fa-clock"></i>',
        'Cancelado': '<i class="fas fa-times-circle"></i>'
    };
    return icons[estado] || '<i class="fas fa-question-circle"></i>';
}

// Función para formatear rango de fechas
function formatDateRange(inicio, fin) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    const fechaInicio = new Date(inicio).toLocaleDateString('es-ES', options);
    
    if (!fin) {
        return `${fechaInicio} - En curso`;
    }
    
    const fechaFin = new Date(fin).toLocaleDateString('es-ES', options);
    return `${fechaInicio} - ${fechaFin}`;
}

// Función para formatear moneda
function formatCurrency(amount) {
    if (amount === 0) return 'Sin pago';
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
}

// Función para generar estrellas
function generateStars(rating) {
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        stars += i <= rating ? '<i class="fas fa-star"></i>' : '<i class="far fa-star"></i>';
    }
    return stars;
}

// Función para actualizar estadísticas
function updateStats() {
    const completados = historialData.filter(e => e.estado === 'Completado').length;
    const horasTotal = historialData.reduce((total, empleo) => {
        if (empleo.estado === 'Completado') {
            const dias = parseInt(empleo.duracion) || 1;
            return total + (dias * 8); // 8 horas por día estimadas
        }
        return total;
    }, 0);
    
    const calificacionPromedio = historialData
        .filter(e => e.calificacion)
        .reduce((sum, e, _, arr) => sum + e.calificacion / arr.length, 0);
    
    const ingresoTotal = historialData
        .filter(e => e.estado === 'Completado')
        .reduce((total, e) => total + e.pago, 0);

    // Actualizar elementos del DOM
    const statCards = document.querySelectorAll('.stat-card');
    if (statCards.length >= 4) {
        statCards[0].querySelector('.stat-number').textContent = completados;
        statCards[1].querySelector('.stat-number').textContent = `${horasTotal}h`;
        statCards[2].querySelector('.stat-number').textContent = calificacionPromedio.toFixed(1);
        statCards[3].querySelector('.stat-number').textContent = formatCurrency(ingresoTotal);
    }
}

// Función para mostrar detalles del empleo
function showEmpleoDetails(empleoId) {
    const empleo = historialData.find(e => e.id === empleoId);
    if (!empleo) return;

    const modal = document.getElementById('detalleModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');

    modalTitle.textContent = `Detalles: ${empleo.titulo}`;
    
    modalBody.innerHTML = `
        <div class="modal-empleo-details">
            <div class="detail-section">
                <h4><i class="fas fa-briefcase"></i> Información del Empleo</h4>
                <div class="detail-grid">
                    <div class="detail-row">
                        <span class="label">Empleador:</span>
                        <span class="value">${empleo.empleador}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Tipo de trabajo:</span>
                        <span class="value">${empleo.tipo}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Ubicación:</span>
                        <span class="value">${empleo.ubicacion}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Estado:</span>
                        <span class="value status-badge status-${empleo.estado.toLowerCase().replace(' ', '-')}">${empleo.estado}</span>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h4><i class="fas fa-calendar-alt"></i> Fechas y Duración</h4>
                <div class="detail-grid">
                    <div class="detail-row">
                        <span class="label">Fecha de inicio:</span>
                        <span class="value">${new Date(empleo.fechaInicio).toLocaleDateString('es-ES', {year: 'numeric', month: 'long', day: 'numeric'})}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Fecha de finalización:</span>
                        <span class="value">${empleo.fechaFin ? new Date(empleo.fechaFin).toLocaleDateString('es-ES', {year: 'numeric', month: 'long', day: 'numeric'}) : 'En curso'}</span>
                    </div>
                    <div class="detail-row">
                        <span class="label">Duración:</span>
                        <span class="value">${empleo.duracion}</span>
                    </div>
                </div>
            </div>

            <div class="detail-section">
                <h4><i class="fas fa-file-alt"></i> Descripción del Trabajo</h4>
                <p class="description-text">${empleo.descripcion}</p>
            </div>

            <div class="detail-section">
                <h4><i class="fas fa-cog"></i> Condiciones Pactadas</h4>
                <p class="conditions-text">${empleo.condiciones}</p>
                <div class="payment-info">
                    <span class="payment-label">Pago total:</span>
                    <span class="payment-value">${formatCurrency(empleo.pago)}</span>
                </div>
            </div>

            ${empleo.calificacion ? `
                <div class="detail-section">
                    <h4><i class="fas fa-star"></i> Valoración Recibida</h4>
                    <div class="rating-display">
                        <div class="stars-large">
                            ${generateStars(empleo.calificacion)}
                        </div>
                        <span class="rating-number">${empleo.calificacion}.0/5.0</span>
                    </div>
                    ${empleo.comentario ? `
                        <div class="comment-box">
                            <p>"${empleo.comentario}"</p>
                        </div>
                    ` : ''}
                </div>
            ` : ''}

            <div class="detail-section">
                <h4><i class="fas fa-map-marker-alt"></i> Ubicación Aproximada</h4>
                <div class="map-placeholder" id="empleoMap">
                    <div class="map-info">
                        <i class="fas fa-map-marked-alt"></i>
                        <p><strong>${empleo.ubicacion}</strong></p>
                        <small>Vista del mapa no disponible</small>
                    </div>
                </div>
            </div>

            <div class="modal-actions">
                <button class="btn btn-secondary" onclick="contactarEmpleador(${empleo.empleadorId})">
                    <i class="fas fa-envelope"></i> Contactar Empleador
                </button>
                ${empleo.estado === 'Completado' ? `
                    <button class="btn btn-primary" onclick="descargarCertificado(${empleo.id})">
                        <i class="fas fa-certificate"></i> Descargar Certificado
                    </button>
                ` : ''}
            </div>
        </div>
    `;

    modal.classList.add('show');
}

// Funciones de filtrado y búsqueda
function setupFilters() {
    const searchInput = document.getElementById('searchHistorial');
    const estadoFilter = document.getElementById('estadoFilter');
    const fechaFilter = document.getElementById('fechaFilter');
    const tipoFilter = document.getElementById('tipoFilter');

    searchInput.addEventListener('input', applyFilters);
    estadoFilter.addEventListener('change', applyFilters);
    fechaFilter.addEventListener('change', applyFilters);
    tipoFilter.addEventListener('change', applyFilters);
}

function applyFilters() {
    const searchTerm = document.getElementById('searchHistorial').value.toLowerCase();
    const estadoFilter = document.getElementById('estadoFilter').value;
    const fechaFilter = document.getElementById('fechaFilter').value;
    const tipoFilter = document.getElementById('tipoFilter').value;

    filteredData = historialData.filter(empleo => {
        const matchesSearch = !searchTerm || 
            empleo.titulo.toLowerCase().includes(searchTerm) ||
            empleo.empleador.toLowerCase().includes(searchTerm) ||
            empleo.ubicacion.toLowerCase().includes(searchTerm);

        const matchesEstado = !estadoFilter || empleo.estado === estadoFilter;
        const matchesTipo = !tipoFilter || empleo.tipo === tipoFilter;

        return matchesSearch && matchesEstado && matchesTipo;
    });

    // Aplicar ordenación por fecha si se selecciona
    if (fechaFilter) {
        filteredData.sort((a, b) => {
            const fechaA = new Date(a.fechaInicio);
            const fechaB = new Date(b.fechaInicio);
            return fechaFilter === 'desc' ? fechaB - fechaA : fechaA - fechaB;
        });
    }

    currentPage = 1;
    renderHistorial();
}

// Funciones de paginación
function updatePagination() {
    const totalPages = Math.ceil(filteredData.length / itemsPerPage);
    const paginationInfo = document.querySelector('.pagination-info');
    const prevBtn = document.querySelector('.pagination-btn:first-child');
    const nextBtn = document.querySelector('.pagination-btn:last-child');

    paginationInfo.textContent = `Página ${currentPage} de ${totalPages}`;
    
    prevBtn.style.opacity = currentPage === 1 ? '0.5' : '1';
    prevBtn.style.pointerEvents = currentPage === 1 ? 'none' : 'auto';
    
    nextBtn.style.opacity = currentPage === totalPages ? '0.5' : '1';
    nextBtn.style.pointerEvents = currentPage === totalPages ? 'none' : 'auto';
}

function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        renderHistorial();
        window.scrollTo(0, 0);
    }
}

function nextPage() {
    const totalPages = Math.ceil(filteredData.length / itemsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        renderHistorial();
        window.scrollTo(0, 0);
    }
}

// Funciones de modal
function closeModal() {
    const modal = document.getElementById('detalleModal');
    modal.classList.remove('show');
}

// Funciones de utilidad
function goBack() {
    window.location.href = 'index-trabajador.html';
}

async function exportToPDF() {
    // Mostrar loading
    const btn = event.target.closest('.btn');
    const originalContent = btn.innerHTML;
    btn.innerHTML = '<div class="loading-spinner"></div> Generando PDF...';
    btn.disabled = true;

    try {
        // Simular generación de PDF
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Aquí iría la lógica real para generar el PDF
        alert('PDF generado exitosamente.\n\nEl archivo se descargará automáticamente con tu historial laboral completo.');
        
    } catch (error) {
        console.error('Error generando PDF:', error);
        alert('Error al generar el PDF. Intenta nuevamente.');
    } finally {
        btn.innerHTML = originalContent;
        btn.disabled = false;
    }
}

function contactarEmpleador(empleadorId) {
    alert(`Contactando empleador ID: ${empleadorId}\n\nEsta funcionalidad redirigirá al sistema de mensajería interno.`);
}

function descargarCertificado(empleoId) {
    const empleo = historialData.find(e => e.id === empleoId);
    if (empleo) {
        alert(`Descargando certificado de trabajo:\n\n"${empleo.titulo}"\nEmpleador: ${empleo.empleador}\n\nEl certificado se generará en formato PDF.`);
    }
}

// Event listeners para cerrar modal
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
    console.log('Inicializando historial de empleos...');
    
    loadUserData();
    loadHistorialFromServer();
    setupFilters();

    // Animaciones de entrada
    setTimeout(() => {
        const cards = document.querySelectorAll('.stat-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }, 500);
});