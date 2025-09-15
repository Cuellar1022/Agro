// JavaScript completo corregido para perfil - js/perfil-trabajador.js

document.addEventListener('DOMContentLoaded', function() {
    loadUserData();
    setupFormHandler();
    setupPhotoUpload();
    setupDocumentUploads();
    setupRatingSystem();
    loadDocuments();
    loadEmployers();
    loadSentRatings();
});

// Cargar datos del usuario - CORREGIDO
async function loadUserData() {
    try {
        console.log('Cargando datos del usuario...');
        const response = await fetch('/get_user_session');
        const data = await response.json();
        
        if (data.success && data.user) {
            const user = data.user;
            console.log('Datos del usuario:', user);
            
            // Actualizar interfaz principal
            updateElement('profileName', user.full_name || user.user_name || 'Usuario');
            updateElement('profileRole', user.rol || 'Trabajador Agrícola');
            
            // Información personal
            updateElement('displayName', user.full_name || user.user_name || 'Usuario');
            updateElement('displayEmail', user.email || 'No especificado');
            updateElement('displayPhone', user.telefono || 'No especificado');
            updateElement('displayLocation', user.ubicacion || 'No especificado');
            
            // Información profesional
            updateElement('displayRole', user.rol || 'Trabajador Agrícola');
            updateElement('displayArea', user.area_trabajo || 'No especificado');
            updateElement('displaySpecialty', user.especializacion || 'No especificado');
            updateElement('displayExperience', user.anos_experiencia ? `${user.anos_experiencia} años` : 'No especificado');
            
            // Estadísticas
            updateElement('displayJobsCompleted', user.trabajos_completados || '0');
            updateElement('displayRating', generateStars(user.calificacion_promedio || 0), true);
            updateElement('displayMemberSince', formatDate(user.fecha_registro));
            
            // Formulario de edición - valores básicos
            setInputValue('editName', user.full_name || '');
            setInputValue('editEmail', user.email || '');
            setInputValue('editPhone', user.telefono || '');
            
            // Campos profesionales adicionales
            setInputValue('editSocialMedia', user.red_social || '');
            setSelectValue('editArea', user.area_trabajo || '');
            setInputValue('editSpecialty', user.especializacion || '');
            setInputValue('editExperience', user.anos_experiencia || '');
            setSelectValue('editEducation', user.nivel_educativo || '');
            
            // Cargar foto si existe
            if (user.url_foto) {
                updatePhotoDisplay(user.url_foto);
            }
            
        } else {
            console.error('Error en respuesta:', data);
            showMessage('Error cargando datos del usuario', 'error');
            if (!data.user) {
                setTimeout(() => {
                    window.location.href = '/vista/login-trabajador.html';
                }, 2000);
            }
        }
    } catch (error) {
        console.error('Error al cargar datos:', error);
        showMessage('Error de conexión al cargar datos', 'error');
    }
}

// Funciones auxiliares para actualización segura de elementos
function updateElement(id, value, isHtml = false) {
    const element = document.getElementById(id);
    if (element) {
        if (isHtml) {
            element.innerHTML = value;
        } else {
            element.textContent = value;
        }
    } else {
        console.warn(`Elemento no encontrado: ${id}`);
    }
}

function setInputValue(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.value = value || '';
    } else {
        console.warn(`Input no encontrado: ${id}`);
    }
}

function setSelectValue(id, value) {
    const element = document.getElementById(id);
    if (element && value) {
        element.value = value;
    } else if (!element) {
        console.warn(`Select no encontrado: ${id}`);
    }
}

// Configurar manejador del formulario - COMPLETAMENTE CORREGIDO
function setupFormHandler() {
    const form = document.getElementById('profileForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            console.log('Enviando formulario...');
            
            // Obtener valores del formulario
            const fullName = document.getElementById('editName').value.trim();
            const telefono = document.getElementById('editPhone').value.trim();
            
            // Validar datos requeridos
            if (!fullName) {
                showMessage('El nombre completo es requerido', 'error');
                return;
            }
            
            // Separar nombre y apellido
            const nameParts = fullName.split(' ');
            const nombre = nameParts[0] || '';
            const apellido = nameParts.slice(1).join(' ') || '';
            
            // Preparar datos para enviar
            const profileData = {
                nombre: nombre,
                apellido: apellido,
                telefono: telefono
            };
            
            // Agregar campos profesionales
            const redSocial = document.getElementById('editSocialMedia')?.value.trim() || '';
            const areaTrabajoEl = document.getElementById('editArea');
            const especializacion = document.getElementById('editSpecialty')?.value.trim() || '';
            const experienciaEl = document.getElementById('editExperience');
            const educacionEl = document.getElementById('editEducation');
            
            if (redSocial) profileData.red_social = redSocial;
            if (areaTrabajoEl?.value) profileData.area_trabajo = areaTrabajoEl.value;
            if (especializacion) profileData.especializacion = especializacion;
            if (experienciaEl?.value) profileData.anos_experiencia = parseInt(experienciaEl.value) || 0;
            if (educacionEl?.value) profileData.nivel_educativo = educacionEl.value;
            
            console.log('Datos a enviar:', profileData);
            
            try {
                showMessage('Guardando cambios...', 'info');
                
                const response = await fetch('/api/update-profile', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(profileData)
                });
                
                console.log('Response status:', response.status);
                const result = await response.json();
                console.log('Respuesta del servidor:', result);
                
                if (response.ok && result.success) {
                    showMessage('Perfil actualizado correctamente', 'success');
                    await loadUserData();
                    showTab('info');
                } else {
                    showMessage(result.message || 'Error al actualizar el perfil', 'error');
                }
                
            } catch (error) {
                console.error('Error al actualizar perfil:', error);
                showMessage('Error de conexión al actualizar perfil', 'error');
            }
        });
    } else {
        console.error('Formulario de perfil no encontrado');
    }
}

// Cargar lista de documentos subidos
async function loadDocuments() {
    try {
        console.log('Cargando documentos...');
        
        const response = await fetch('/api/user-documents');
        const data = await response.json();
        
        console.log('Documentos cargados:', data);
        
        if (data.success && data.documents) {
            updateDocumentsList(data.documents);
            updateDocumentCount(data.documents.length);
        } else {
            console.log('No hay documentos o error:', data.message);
            updateDocumentsList([]);
        }
        
    } catch (error) {
        console.error('Error al cargar documentos:', error);
        updateDocumentsList([]);
    }
}

// Actualizar lista de documentos en la interfaz
function updateDocumentsList(documents) {
    const filesList = document.getElementById('filesList');
    if (!filesList) {
        console.error('Contenedor de archivos no encontrado');
        return;
    }
    
    if (documents.length === 0) {
        filesList.innerHTML = '<p style="color: #6c757d; text-align: center;">No hay archivos subidos aún</p>';
        return;
    }
    
    let html = '';
    documents.forEach(doc => {
        const fecha = new Date(doc.fecha_subida).toLocaleDateString('es-ES');
        const estado = doc.estado || 'Subido';
        const estadoColor = estado === 'Verificado' ? '#28a745' : estado === 'Rechazado' ? '#dc3545' : '#ffc107';
        
        html += `
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #333; margin-bottom: 5px;">${doc.tipo_documento}</div>
                    <div style="color: #666; font-size: 14px; margin-bottom: 3px;">${doc.nombre_archivo}</div>
                    <div style="color: #999; font-size: 12px;">Subido el ${fecha}</div>
                </div>
                <div style="text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 5px;">
                    <span style="color: ${estadoColor}; font-weight: bold; font-size: 14px;">${estado}</span>
                    ${doc.url_documento ? `<a href="${doc.url_documento}" target="_blank" style="font-size: 13px; color: #007bff; text-decoration: none; padding: 4px 8px; border: 1px solid #007bff; border-radius: 4px; transition: all 0.2s;">📄 Ver archivo</a>` : ''}
                </div>
            </div>
        `;
    });
    
    filesList.innerHTML = html;
}

// Actualizar contador de documentos
function updateDocumentCount(count) {
    const documentCount = document.getElementById('documentCount');
    if (documentCount) {
        documentCount.textContent = `${count}/3 documentos subidos`;
    }
    
    const profileStatus = document.getElementById('profileStatus');
    if (profileStatus) {
        if (count >= 2) {
            profileStatus.innerHTML = '<span style="color: #28a745;">✅ Perfil completo</span>';
        } else {
            profileStatus.innerHTML = '<span style="color: #dc3545;">⏳ Pendiente de verificación</span>';
        }
    }
}

// Cargar empleadores para el sistema de calificación
async function loadEmployers() {
    try {
        console.log('Cargando empleadores...');
        
        const response = await fetch('/api/user-employers');
        const data = await response.json();
        
        if (data.success && data.employers) {
            updateEmployerSelect(data.employers);
            console.log(`Empleadores cargados: ${data.employers.length}`);
        } else {
            console.log('No hay empleadores disponibles');
            updateEmployerSelect([]);
        }
        
    } catch (error) {
        console.error('Error al cargar empleadores:', error);
        updateEmployerSelect([]);
    }
}

// Actualizar select de empleadores
function updateEmployerSelect(employers) {
    const select = document.getElementById('employerSelect');
    if (!select) {
        console.error('Select de empleadores no encontrado');
        return;
    }
    
    // Limpiar opciones existentes
    select.innerHTML = '<option value="">Selecciona el empleador a calificar</option>';
    
    if (employers.length === 0) {
        const option = document.createElement('option');
        option.value = '';
        option.textContent = 'No hay empleadores disponibles para calificar';
        option.disabled = true;
        select.appendChild(option);
        return;
    }
    
    employers.forEach(employer => {
        const option = document.createElement('option');
        option.value = employer.id;
        option.textContent = employer.nombre || employer.empresa || 'Empleador';
        select.appendChild(option);
    });
}

// Configurar sistema de calificaciones
function setupRatingSystem() {
    const stars = document.querySelectorAll('.star-input');
    const ratingDisplay = document.getElementById('ratingDisplay');
    let selectedRating = 0;
    
    console.log(`Sistema de calificaciones configurado con ${stars.length} estrellas`);
    
    // Event listeners para las estrellas
    stars.forEach((star, index) => {
        star.addEventListener('click', function() {
            selectedRating = parseInt(this.dataset.rating);
            updateStarDisplay(selectedRating);
            if (ratingDisplay) {
                ratingDisplay.textContent = `${selectedRating} estrella${selectedRating !== 1 ? 's' : ''}`;
            }
            console.log(`Calificación seleccionada: ${selectedRating}`);
        });
        
        star.addEventListener('mouseover', function() {
            const rating = parseInt(this.dataset.rating);
            updateStarDisplay(rating, true);
        });
    });
    
    // Reset visual en mouseleave
    const starContainer = document.getElementById('starRating');
    if (starContainer) {
        starContainer.addEventListener('mouseleave', function() {
            updateStarDisplay(selectedRating);
        });
    }
    
    // Manejar envío de calificación
    const ratingForm = document.getElementById('ratingForm');
    if (ratingForm) {
        ratingForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const employerSelect = document.getElementById('employerSelect');
            const commentTextarea = document.getElementById('ratingComment');
            
            if (!employerSelect || !commentTextarea) {
                showMessage('Error en el formulario de calificación', 'error');
                return;
            }
            
            const employerId = employerSelect.value;
            const comment = commentTextarea.value.trim();
            
            console.log('Enviando calificación:', { employerId, rating: selectedRating, comment });
            
            if (!employerId || !selectedRating || !comment) {
                showMessage('Complete todos los campos para enviar la calificación', 'error');
                return;
            }
            
            try {
                showMessage('Enviando calificación...', 'info');
                
                const response = await fetch('/api/submit-rating', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        employerId: employerId,
                        rating: selectedRating,
                        comment: comment
                    })
                });
                
                const result = await response.json();
                console.log('Resultado calificación:', result);
                
                if (response.ok && result.success) {
                    showMessage('Calificación enviada correctamente', 'success');
                    
                    // Limpiar formulario
                    ratingForm.reset();
                    selectedRating = 0;
                    updateStarDisplay(0);
                    if (ratingDisplay) ratingDisplay.textContent = '';
                    
                    // Recargar datos
                    loadSentRatings();
                    loadEmployers();
                } else {
                    showMessage(result.message || 'Error al enviar calificación', 'error');
                }
                
            } catch (error) {
                console.error('Error al enviar calificación:', error);
                showMessage('Error de conexión al enviar calificación', 'error');
            }
        });
    } else {
        console.error('Formulario de calificación no encontrado');
    }
}

// Cargar calificaciones enviadas
async function loadSentRatings() {
    try {
        console.log('Cargando calificaciones enviadas...');
        
        const response = await fetch('/api/user-ratings');
        const data = await response.json();
        
        if (data.success && data.ratings) {
            updateSentRatings(data.ratings);
            console.log(`Calificaciones enviadas cargadas: ${data.ratings.length}`);
        } else {
            console.log('No hay calificaciones enviadas');
            updateSentRatings([]);
        }
    } catch (error) {
        console.error('Error al cargar calificaciones:', error);
        updateSentRatings([]);
    }
}

// Actualizar lista de calificaciones enviadas
function updateSentRatings(ratings) {
    const container = document.getElementById('sentRatings');
    if (!container) {
        console.error('Contenedor de calificaciones no encontrado');
        return;
    }
    
    if (ratings.length === 0) {
        container.innerHTML = '<div class="empty-state"><p style="color: #6c757d; text-align: center; padding: 20px; background: #f8f9fa; border-radius: 8px;">No has enviado calificaciones aún</p></div>';
        return;
    }
    
    let html = '';
    ratings.forEach(rating => {
        const fecha = new Date(rating.fecha).toLocaleDateString('es-ES');
        const stars = '★'.repeat(rating.calificacion) + '☆'.repeat(5 - rating.calificacion);
        
        html += `
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <strong style="color: #333; font-size: 16px;">${rating.empleador_nombre}</strong>
                    <span style="color: #ffc107; font-size: 18px;">${stars}</span>
                </div>
                <p style="color: #666; margin: 10px 0; line-height: 1.5;">${rating.comentario}</p>
                <small style="color: #999;">Enviada el ${fecha}</small>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Configurar subida de documentos
function setupDocumentUploads() {
    console.log('Configurando subida de documentos...');
}

// Configurar subida de foto de perfil
function setupPhotoUpload() {
    const photoInput = document.getElementById('profilePhotoInput');
    const profilePhoto = document.getElementById('profilePhoto');
    
    if (photoInput && profilePhoto) {
        profilePhoto.addEventListener('click', function() {
            photoInput.click();
        });
        
        photoInput.addEventListener('change', async function(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
            if (!allowedTypes.includes(file.type)) {
                showMessage('Formato de archivo no válido. Use JPG, PNG o GIF', 'error');
                return;
            }
            
            if (file.size > 5 * 1024 * 1024) {
                showMessage('El archivo es muy grande. Máximo 5MB', 'error');
                return;
            }
            
            const formData = new FormData();
            formData.append('profilePhoto', file);
            
            try {
                showMessage('Subiendo foto...', 'info');
                
                const response = await fetch('/api/upload-profile-photo', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (response.ok && result.success) {
                    showMessage('Foto de perfil actualizada', 'success');
                    updatePhotoDisplay(result.photoUrl);
                } else {
                    showMessage(result.message || 'Error al subir la foto', 'error');
                }
                
            } catch (error) {
                console.error('Error al subir foto:', error);
                showMessage('Error de conexión al subir foto', 'error');
            }
        });
    }
}

// Funciones auxiliares
function updatePhotoDisplay(photoUrl) {
    const profilePhoto = document.getElementById('profilePhoto');
    const editProfilePhotoPreview = document.getElementById('editProfilePhotoPreview');
    
    if (profilePhoto) {
        profilePhoto.innerHTML = `<img src="${photoUrl}" alt="Foto de perfil" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">`;
    }
    
    if (editProfilePhotoPreview) {
        editProfilePhotoPreview.innerHTML = `<img src="${photoUrl}" alt="Foto de perfil" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">`;
    }
}

function updateStarDisplay(rating, isHover = false) {
    const stars = document.querySelectorAll('.star-input');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.style.color = '#ffc107';
        } else {
            star.style.color = '#ddd';
        }
    });
}

function generateStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
    
    let starsHtml = '';
    
    for (let i = 0; i < fullStars; i++) {
        starsHtml += '<span style="color: #ffc107;">⭐</span>';
    }
    
    if (hasHalfStar) {
        starsHtml += '<span style="color: #ffc107;">⭐</span>';
    }
    
    for (let i = 0; i < emptyStars; i++) {
        starsHtml += '<span style="color: #ddd;">⭐</span>';
    }
    
    return `${starsHtml} ${rating.toFixed(1)}`;
}

function formatDate(dateString) {
    if (!dateString) return 'No especificado';
    
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long', 
        day: 'numeric'
    });
}

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    const selectedContent = document.getElementById(tabName);
    if (selectedContent) {
        selectedContent.classList.add('active');
    }
    
    const selectedTab = document.querySelector(`.tab[onclick="showTab('${tabName}')"]`);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
}

function cancelEdit() {
    loadUserData();
    showTab('info');
}

function showMessage(message, type = 'info') {
    const existingMessages = document.querySelectorAll('.temp-message');
    existingMessages.forEach(msg => msg.remove());
    
    const colors = {
        success: '#d4edda',
        error: '#f8d7da',
        warning: '#fff3cd',
        info: '#d1ecf1'
    };
    
    const textColors = {
        success: '#155724',
        error: '#721c24',
        warning: '#856404',
        info: '#0c5460'
    };
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'temp-message';
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type]};
        color: ${textColors[type]};
        padding: 12px 16px;
        border-radius: 8px;
        z-index: 9999;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        max-width: 300px;
        word-wrap: break-word;
        font-size: 14px;
    `;
    messageDiv.textContent = message;
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 4000);
}

// Funciones globales
window.showTab = showTab;
window.cancelEdit = cancelEdit;

// Función global para upload de documentos
window.uploadDocument = async function(docType) {
    console.log('Subiendo documento tipo:', docType);
    
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.pdf,.doc,.docx,.png,.jpg,.jpeg';
    
    input.onchange = async function(e) {
        const file = e.target.files[0];
        if (!file) return;
        
        const allowedTypes = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'image/jpeg',
            'image/jpg', 
            'image/png'
        ];
        
        if (!allowedTypes.includes(file.type)) {
            showMessage('Formato no válido. Use PDF, DOC, DOCX, JPG o PNG', 'error');
            return;
        }
        
        if (file.size > 5 * 1024 * 1024) {
            showMessage('Archivo muy grande. Máximo 5MB', 'error');
            return;
        }
        
        const formData = new FormData();
        formData.append('document', file);
        formData.append('docType', docType);
        
        try {
            showMessage(`Subiendo ${docType.toLowerCase()}...`, 'info');
            
            const response = await fetch('/api/upload-document', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                showMessage(`${docType} subido correctamente`, 'success');
                loadDocuments();
            } else {
                showMessage(result.message || `Error al subir ${docType.toLowerCase()}`, 'error');
            }
            
        } catch (error) {
            console.error('Error al subir documento:', error);
            showMessage('Error de conexión al subir documento', 'error');
        }
    };
    
    input.click();
};

console.log('✅ Perfil trabajador JS cargado completamente');