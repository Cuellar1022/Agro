// Variables globales para gestión de favoritos
let favoritosData = [];
let currentPage = 1;
const itemsPerPage = 6;
let filteredData = [];
let selectedItems = [];
let userData = null;
let pendingAction = null;

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

// Función para cargar favoritos desde el servidor
async function loadFavoritosFromServer() {
    try {
        const response = await fetch('/api/favoritos');
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                // Convertir datos del servidor al formato esperado
                favoritosData = data.favoritos.map((fav, index) => ({
                    id: fav.job_id || index + 1,
                    oferta_id: fav.job_id,
                    titulo: fav.titulo || 'Sin título',
                    agricultor: fav.agricultor || 'Agricultor',
                    agricultorId: Math.floor(Math.random() * 1000) + 200,
                    fechaAgregado: fav.fecha_agregado || new Date().toISOString(),
                    estado: fav.estado === 'Abierta' ? 'activa' : 'expirada',
                    pago: fav.pago || 0,
                    ubicacion: fav.ubicacion || 'Colombia',
                    duracion: "Por determinar",
                    descripcion: fav.descripcion || 'Sin descripción',
                    tipo: "General",
                    fechaPublicacion: new Date().toISOString(),
                    fechaExpiracion: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
                    aplicada: false,
                    tags: ["Favorito", "Guardado"]
                }));
                
                showToast('success', 'Actualizado', 'Favoritos cargados correctamente');
            } else {
                throw new Error(data.error || 'Error cargando favoritos');
            }
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        console.error('Error cargando favoritos:', error);
        favoritosData = [];
        showToast('info', 'Sin favoritos', 'No tienes favoritos guardados aún');
    }
    
    filteredData = [...favoritosData];
    renderFavoritos();
    updateFavoritosCount();
}

// Función para renderizar la lista de favoritos
function renderFavoritos() {
    const container = document.getElementById('favoritosList');
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageData = filteredData.slice(startIndex, endIndex);

    if (pageData.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-heart-broken"></i>
                <h3>No tienes favoritos guardados</h3>
                <p>Explora las ofertas disponibles y marca las que te interesen como favoritas para consultarlas fácilmente.</p>
                <button class="btn btn-primary" onclick="goToOffers()">
                    <i class="fas fa-search"></i> Explorar Ofertas
                </button>
            </div>
        `;
        return;
    }

    container.innerHTML = pageData.map(favorito => `
        <div class="favorito-card ${favorito.estado}" data-id="${favorito.id}">
            <div class="favorito-header">
                <div>
                    <div class="favorito-title">${favorito.titulo}</div>
                    <div class="agricultor-info">
                        <i class="fas fa-seedling"></i>
                        ${favorito.agricultor}
                    </div>
                </div>
                <div class="favorito-status">
                    <div class="status-indicator status-${favorito.estado}">
                        ${getStatusIcon(favorito.estado)}
                        ${getStatusText(favorito.estado)}
                    </div>
                    <div class="favorito-select">
                        <div class="favorito-checkbox" onclick="toggleSelect(${favorito.id})" data-id="${favorito.id}"></div>
                    </div>
                </div>
            </div>

            <div class="favorito-details">
                <div class="detail-item">
                    <i class="fas fa-dollar-sign"></i>
                    <span class="salary-highlight">${formatCurrency(favorito.pago)}/día</span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>${favorito.ubicacion}</span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-clock"></i>
                    <span>${favorito.duracion}</span>
                </div>
                <div class="detail-item">
                    <i class="fas fa-calendar-alt"></i>
                    <span>Expira: ${formatDate(favorito.fechaExpiracion)}</span>
                </div>
                ${favorito.aplicada ? `
                    <div class="detail-item">
                        <i class="fas fa-paper-plane"></i>
                        <span style="color: #4CAF50; font-weight: 600;">Ya postulado</span>
                    </div>
                ` : ''}
            </div>

            <div class="favorito-description">
                ${favorito.descripcion}
            </div>

            <div class="favorito-footer">
                <div class="favorito-tags">
                    ${favorito.tags.map(tag => `<span class="favorito-tag">${tag}</span>`).join('')}
                </div>
                <div class="favorito-actions">
                    <button class="action-btn secondary" onclick="viewDetails(${favorito.id})">
                        <i class="fas fa-eye"></i> Ver Detalles
                    </button>
                    ${favorito.estado === 'activa' && !favorito.aplicada ? `
                        <button class="action-btn primary" onclick="applyToOffer(${favorito.oferta_id})">
                            <i class="fas fa-paper-plane"></i> Postularme
                        </button>
                    ` : ''}
                    <button class="action-btn danger" onclick="removeFavorite(${favorito.id})">
                        <i class="fas fa-heart-broken"></i> Quitar
                    </button>
                </div>
            </div>

            <div class="favorito-date">
                <i class="fas fa-heart"></i>
                <span>Agregado el ${formatDateTime(favorito.fechaAgregado)}</span>
            </div>
        </div>
    `).join('');

    updatePagination();
    addCardAnimations();
    updateSelectedCheckboxes();
}

// Funciones de utilidad para estados
function getStatusIcon(estado) {
    const icons = {
        'activa': '<i class="fas fa-check-circle"></i>',
        'expirada': '<i class="fas fa-clock"></i>',
        'retirada': '<i class="fas fa-times-circle"></i>'
    };
    return icons[estado] || '<i class="fas fa-question-circle"></i>';
}

function getStatusText(estado) {
    const texts = {
        'activa': 'Activa',
        'expirada': 'Expirada',
        'retirada': 'Retirada'
    };
    return texts[estado] || 'Desconocido';
}

// Funciones de formato
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

function formatDateTime(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
    };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

// Funciones de filtrado y búsqueda
function setupFilters() {
    const searchInput = document.getElementById('searchFavoritos');
    const estadoFilter = document.getElementById('estadoFilter');
    const tipoFilter = document.getElementById('tipoFilter');
    const ordenFilter = document.getElementById('ordenFilter');

    searchInput.addEventListener('input', applyFilters);
    estadoFilter.addEventListener('change', applyFilters);
    tipoFilter.addEventListener('change', applyFilters);
    ordenFilter.addEventListener('change', applyFilters);
}

function applyFilters() {
    const searchTerm = document.getElementById('searchFavoritos').value.toLowerCase();
    const estadoFilter = document.getElementById('estadoFilter').value;
    const tipoFilter = document.getElementById('tipoFilter').value;
    const ordenFilter = document.getElementById('ordenFilter').value;

    // Filtrar
    filteredData = favoritosData.filter(favorito => {
        const matchesSearch = !searchTerm || 
            favorito.titulo.toLowerCase().includes(searchTerm) ||
            favorito.agricultor.toLowerCase().includes(searchTerm) ||
            favorito.descripcion.toLowerCase().includes(searchTerm) ||
            favorito.ubicacion.toLowerCase().includes(searchTerm);

        const matchesEstado = !estadoFilter || favorito.estado === estadoFilter;
        const matchesTipo = !tipoFilter || favorito.tipo === tipoFilter;

        return matchesSearch && matchesEstado && matchesTipo;
    });

    // Ordenar
    if (ordenFilter) {
        filteredData.sort((a, b) => {
            switch (ordenFilter) {
                case 'fecha_desc':
                    return new Date(b.fechaAgregado) - new Date(a.fechaAgregado);
                case 'fecha_asc':
                    return new Date(a.fechaAgregado) - new Date(b.fechaAgregado);
                case 'pago_desc':
                    return b.pago - a.pago;
                case 'pago_asc':
                    return a.pago - b.pago;
                default:
                    return 0;
            }
        });
    }

    currentPage = 1;
    renderFavoritos();
    updateFavoritosCount();
}

// Gestión de selección múltiple
function toggleSelect(id) {
    const index = selectedItems.indexOf(id);
    if (index > -1) {
        selectedItems.splice(index, 1);
    } else {
        selectedItems.push(id);
    }
    updateSelectedCheckboxes();
    updateBulkActions();
}

function updateSelectedCheckboxes() {
    document.querySelectorAll('.favorito-checkbox').forEach(checkbox => {
        const id = parseInt(checkbox.dataset.id);
        const isSelected = selectedItems.includes(id);
        checkbox.classList.toggle('checked', isSelected);
    });
}

function updateBulkActions() {
    const removeBtn = document.getElementById('removeSelectedBtn');
    removeBtn.disabled = selectedItems.length === 0;
}

function selectAll() {
    const visibleIds = filteredData.slice(
        (currentPage - 1) * itemsPerPage,
        currentPage * itemsPerPage
    ).map(f => f.id);

    const allSelected = visibleIds.every(id => selectedItems.includes(id));

    if (allSelected) {
        selectedItems = selectedItems.filter(id => !visibleIds.includes(id));
    } else {
        visibleIds.forEach(id => {
            if (!selectedItems.includes(id)) {
                selectedItems.push(id);
            }
        });
    }

    updateSelectedCheckboxes();
    updateBulkActions();
}

// Función principal para remover favorito
function removeFavorite(id) {
    const favorito = favoritosData.find(f => f.id === id);
    if (!favorito) return;

    showConfirmModal(
        'Quitar de favoritos',
        `¿Estás seguro de que deseas quitar "${favorito.titulo}" de tus favoritos?`,
        () => executeRemoveFavorite(favorito)
    );
}

// Función corregida para ejecutar remoción de favorito
async function executeRemoveFavorite(favorito) {
    try {
        console.log('Removiendo favorito:', favorito);
        
        const response = await fetch('/api/favoritos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                job_id: favorito.oferta_id,
                action: 'remove'
            })
        });

        const data = await response.json();
        console.log('Respuesta del servidor:', data);
        
        if (data.success) {
            // Remover localmente
            favoritosData = favoritosData.filter(f => f.id !== favorito.id);
            filteredData = filteredData.filter(f => f.id !== favorito.id);
            selectedItems = selectedItems.filter(itemId => itemId !== favorito.id);
            
            renderFavoritos();
            updateFavoritosCount();
            updateBulkActions();
            
            showToast('success', 'Favorito eliminado', favorito.titulo);
        } else {
            throw new Error(data.error || 'Error al eliminar favorito');
        }
    } catch (error) {
        console.error('Error eliminando favorito:', error);
        showToast('error', 'Error', 'No se pudo eliminar el favorito: ' + error.message);
    }
}

function removeSelected() {
    if (selectedItems.length === 0) return;

    const count = selectedItems.length;
    showConfirmModal(
        'Quitar favoritos seleccionados',
        `¿Estás seguro de que deseas quitar ${count} ${count === 1 ? 'favorito' : 'favoritos'} seleccionados?`,
        () => executeRemoveSelected()
    );
}

async function executeRemoveSelected() {
    try {
        const favoritosToRemove = favoritosData.filter(f => selectedItems.includes(f.id));
        const promises = favoritosToRemove.map(favorito => 
            fetch('/api/favoritos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    job_id: favorito.oferta_id,
                    action: 'remove'
                })
            })
        );

        await Promise.all(promises);
        
        // Remover localmente
        favoritosData = favoritosData.filter(f => !selectedItems.includes(f.id));
        filteredData = filteredData.filter(f => !selectedItems.includes(f.id));
        const count = selectedItems.length;
        selectedItems = [];
        
        renderFavoritos();
        updateFavoritosCount();
        updateBulkActions();
        
        showToast('success', 'Favoritos eliminados', `${count} favoritos eliminados correctamente`);
    } catch (error) {
        console.error('Error eliminando favoritos:', error);
        showToast('error', 'Error', 'No se pudieron eliminar todos los favoritos');
    }
}

// Función para postularse a una oferta desde favoritos
async function applyToOffer(ofertaId) {
    try {
        const response = await fetch('/api/postular', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ oferta_id: ofertaId })
        });

        const data = await response.json();
        if (data.success) {
            const favorito = favoritosData.find(f => f.oferta_id === ofertaId);
            if (favorito) {
                favorito.aplicada = true;
                renderFavoritos();
            }
            
            showToast('success', 'Postulación enviada', 'Te has postulado exitosamente a esta oferta');
        } else {
            throw new Error(data.error || 'Error al postularse');
        }
    } catch (error) {
        console.error('Error postulándose:', error);
        showToast('error', 'Error', 'No se pudo enviar la postulación');
    }
}

// Ver detalles de una oferta favorita
function viewDetails(id) {
    const favorito = favoritosData.find(f => f.id === id);
    if (!favorito) return;

    const modal = document.getElementById('detalleModal');
    const modalTitle = document.getElementById('detalleTitle');
    const modalBody = document.getElementById('detalleBody');

    modalTitle.textContent = favorito.titulo;
    
    modalBody.innerHTML = `
        <div class="detalle-favorito">
            <div class="detalle-header">
                <div class="status-indicator status-${favorito.estado}">
                    ${getStatusIcon(favorito.estado)}
                    ${getStatusText(favorito.estado)}
                </div>
                <div class="detalle-salary">${formatCurrency(favorito.pago)}/día</div>
            </div>

            <div class="detalle-section">
                <h4><i class="fas fa-seedling"></i> Información del Agricultor</h4>
                <p><strong>${favorito.agricultor}</strong></p>
                <p><i class="fas fa-map-marker-alt"></i> ${favorito.ubicacion}</p>
            </div>

            <div class="detalle-section">
                <h4><i class="fas fa-file-alt"></i> Descripción del Trabajo</h4>
                <p>${favorito.descripcion}</p>
            </div>

            <div class="detalle-section">
                <h4><i class="fas fa-info-circle"></i> Detalles de la Oferta</h4>
                <div class="detalle-grid">
                    <div><strong>Duración:</strong> ${favorito.duracion}</div>
                    <div><strong>Tipo:</strong> ${favorito.tipo}</div>
                    <div><strong>Publicada:</strong> ${formatDate(favorito.fechaPublicacion)}</div>
                    <div><strong>Expira:</strong> ${formatDate(favorito.fechaExpiracion)}</div>
                </div>
            </div>

            <div class="detalle-section">
                <h4><i class="fas fa-heart"></i> Estado del Favorito</h4>
                <p>Agregado a favoritos el ${formatDateTime(favorito.fechaAgregado)}</p>
                ${favorito.aplicada ? '<p style="color: #4CAF50;"><i class="fas fa-check"></i> Ya te postulaste a esta oferta</p>' : ''}
            </div>

            <div class="detalle-actions">
                ${favorito.estado === 'activa' && !favorito.aplicada ? `
                    <button class="btn btn-primary" onclick="applyToOffer(${favorito.oferta_id}); closeDetalleModal();">
                        <i class="fas fa-paper-plane"></i> Postularme Ahora
                    </button>
                ` : ''}
                <button class="btn btn-danger" onclick="removeFavorite(${favorito.id}); closeDetalleModal();">
                    <i class="fas fa-heart-broken"></i> Quitar de Favoritos
                </button>
            </div>
        </div>
    `;

    modal.classList.add('show');
}

// Funciones de utilidad y navegación
function updateFavoritosCount() {
    document.getElementById('favoritosCount').textContent = filteredData.length;
}

function updatePagination() {
    const totalPages = Math.ceil(filteredData.length / itemsPerPage);
    const paginationInfo = document.querySelector('.pagination-info');
    const prevBtn = document.querySelector('.pagination-btn:first-child');
    const nextBtn = document.querySelector('.pagination-btn:last-child');

    if (paginationInfo) {
        paginationInfo.textContent = `Página ${currentPage} de ${totalPages || 1}`;
    }
    
    if (prevBtn) {
        prevBtn.disabled = currentPage === 1;
    }
    
    if (nextBtn) {
        nextBtn.disabled = currentPage === totalPages || totalPages === 0;
    }
}

function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        renderFavoritos();
        window.scrollTo(0, 0);
    }
}

function nextPage() {
    const totalPages = Math.ceil(filteredData.length / itemsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        renderFavoritos();
        window.scrollTo(0, 0);
    }
}

// Modales y confirmaciones
function showConfirmModal(title, message, onConfirm) {
    const modal = document.getElementById('confirmModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    
    modalTitle.textContent = title;
    modalBody.innerHTML = `<p>${message}</p>`;
    
    pendingAction = onConfirm;
    modal.classList.add('show');
}

function confirmAction() {
    if (pendingAction) {
        pendingAction();
        pendingAction = null;
    }
    closeModal();
}

function closeModal() {
    document.getElementById('confirmModal').classList.remove('show');
    pendingAction = null;
}

function closeDetalleModal() {
    document.getElementById('detalleModal').classList.remove('show');
}

// Funciones adicionales
function refreshFavoritos() {
    const btn = event?.target;
    if (btn) {
        const originalContent = btn.innerHTML;
        btn.innerHTML = '<div class="loading-spinner"></div> Actualizando...';
        btn.disabled = true;

        setTimeout(() => {
            loadFavoritosFromServer();
            btn.innerHTML = originalContent;
            btn.disabled = false;
        }, 1500);
    } else {
        loadFavoritosFromServer();
    }
}

function goBack() {
    window.location.href = 'index-trabajador.html';
}

function goToOffers() {
    window.location.href = 'index-trabajador.html';
}

// Sistema de notificaciones Toast
function showToast(type, title, message) {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
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

    setTimeout(() => toast.classList.add('show'), 100);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            if (container.contains(toast)) {
                container.removeChild(toast);
            }
        }, 300);
    }, 4000);
}

// Funciones de animación
function addCardAnimations() {
    const cards = document.querySelectorAll('.favorito-card');
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

// Event listeners para modales
document.addEventListener('click', function(event) {
    const confirmModal = document.getElementById('confirmModal');
    const detalleModal = document.getElementById('detalleModal');
    
    if (event.target === confirmModal) {
        closeModal();
    }
    if (event.target === detalleModal) {
        closeDetalleModal();
    }
});

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const confirmModal = document.getElementById('confirmModal');
        const detalleModal = document.getElementById('detalleModal');
        
        if (confirmModal.classList.contains('show')) {
            closeModal();
        }
        if (detalleModal.classList.contains('show')) {
            closeDetalleModal();
        }
    }
});

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando página de favoritos...');
    
    loadUserData();
    loadFavoritosFromServer();
    setupFilters();

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

// Funciones globales adicionales
window.toggleSelect = toggleSelect;
window.selectAll = selectAll;
window.removeSelected = removeSelected;
window.removeFavorite = removeFavorite;
window.viewDetails = viewDetails;
window.applyToOffer = applyToOffer;
window.refreshFavoritos = refreshFavoritos;
window.goBack = goBack;
window.goToOffers = goToOffers;
window.previousPage = previousPage;
window.nextPage = nextPage;
window.closeModal = closeModal;
window.closeDetalleModal = closeDetalleModal;
window.confirmAction = confirmAction;