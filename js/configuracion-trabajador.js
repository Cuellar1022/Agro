// ================================================================
// JAVASCRIPT PARA CONFIGURACIÓN DEL TRABAJADOR - AGROMATCH
// Archivo: assent/js/configuracion-trabajador.js
// ================================================================

// Variables globales
let currentUser = null;

// ================================================================
// INICIALIZACIÓN
// ================================================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('Configuración del Trabajador cargada');
    
    // Cargar datos del usuario
    loadUserData();
    
    // Configurar event listeners
    setupEventListeners();
    
    // Cargar configuraciones guardadas
    loadSavedSettings();
});

// ================================================================
// CARGAR DATOS DEL USUARIO DESDE EL BACKEND
// ================================================================
async function loadUserData() {
    try {
        const response = await fetch('/get_user_session', {
            method: 'GET',
            credentials: 'include'
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                currentUser = data.user;
                updateUIWithUserData(data.user);
            } else {
                // No hay sesión, redirigir al login
                window.location.href = '/vista/login-trabajador.html';
            }
        } else {
            console.error('Error obteniendo datos del usuario');
            window.location.href = '/vista/login-trabajador.html';
        }
    } catch (error) {
        console.error('Error:', error);
        // En caso de error, intentar datos locales
        loadLocalUserData();
    }
}

function loadLocalUserData() {
    try {
        const userData = localStorage.getItem('agroMatchUser');
        if (userData) {
            currentUser = JSON.parse(userData);
            updateUIWithUserData(currentUser);
        } else {
            // No hay datos, redirigir al login
            window.location.href = '/vista/login-trabajador.html';
        }
    } catch (error) {
        console.error('Error cargando datos locales:', error);
        window.location.href = '/vista/login-trabajador.html';
    }
}

function updateUIWithUserData(user) {
    const userNameElement = document.getElementById('userName');
    if (userNameElement) {
        const fullName = user.full_name || `${user.first_name || ''} ${user.last_name || ''}`.trim();
        userNameElement.textContent = fullName || user.username || user.email || 'Usuario';
    }
    
    // Pre-llenar campo de WhatsApp si existe
    const whatsappField = document.getElementById('whatsappNumber');
    if (whatsappField && user.telefono) {
        whatsappField.value = user.telefono;
    }
    
    console.log('Datos de usuario cargados:', user.first_name || user.username || user.email);
}

// ================================================================
// CONFIGURAR EVENT LISTENERS
// ================================================================
function setupEventListeners() {
    // Formulario de cambio de contraseña
    const passwordForm = document.getElementById('changePasswordForm');
    if (passwordForm) {
        passwordForm.addEventListener('submit', handlePasswordChange);
    }
    
    // Formulario de notificaciones
    const notificationForm = document.getElementById('notificationForm');
    if (notificationForm) {
        notificationForm.addEventListener('submit', handleNotificationSettings);
    }
    
    // Formulario de preferencias
    const preferencesForm = document.getElementById('preferencesForm');
    if (preferencesForm) {
        preferencesForm.addEventListener('submit', handlePreferencesSettings);
    }
    
    // Validación en tiempo real de contraseñas
    const confirmPasswordField = document.getElementById('confirmPassword');
    if (confirmPasswordField) {
        confirmPasswordField.addEventListener('input', validatePasswordMatch);
    }
}

// ================================================================
// FUNCIONES DE UTILIDAD
// ================================================================
function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    const button = field.nextElementSibling;
    if (!button) return;
    
    const icon = button.querySelector('i');
    if (!icon) return;
    
    if (field.type === 'password') {
        field.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        field.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}

function validatePasswordMatch() {
    const newPassword = document.getElementById('newPassword');
    const confirmPassword = document.getElementById('confirmPassword');
    
    if (!newPassword || !confirmPassword) return;
    
    if (confirmPassword.value && newPassword.value !== confirmPassword.value) {
        confirmPassword.style.borderColor = '#f44336';
        confirmPassword.style.boxShadow = '0 0 0 3px rgba(244, 67, 54, 0.1)';
    } else {
        confirmPassword.style.borderColor = '#4CAF50';
        confirmPassword.style.boxShadow = '0 0 0 3px rgba(76, 175, 80, 0.1)';
    }
}

// ================================================================
// MANEJO DE CAMBIO DE CONTRASEÑA
// ================================================================
async function handlePasswordChange(e) {
    e.preventDefault();
    
    const currentPassword = document.getElementById('currentPassword')?.value;
    const newPassword = document.getElementById('newPassword')?.value;
    const confirmPassword = document.getElementById('confirmPassword')?.value;
    
    // Validaciones
    if (!currentPassword || !newPassword || !confirmPassword) {
        showNotification('Por favor, completa todos los campos.', 'error');
        return;
    }
    
    if (newPassword !== confirmPassword) {
        showNotification('Las contraseñas nuevas no coinciden.', 'error');
        return;
    }
    
    if (newPassword.length < 8) {
        showNotification('La nueva contraseña debe tener al menos 8 caracteres.', 'error');
        return;
    }
    
    if (newPassword === currentPassword) {
        showNotification('La nueva contraseña debe ser diferente a la actual.', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/change-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                currentPassword: currentPassword,
                newPassword: newPassword
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showNotification('Contraseña actualizada correctamente.', 'success');
            const form = document.getElementById('changePasswordForm');
            if (form) form.reset();
        } else {
            showNotification(data.message || 'Error al cambiar la contraseña.', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error de conexión. Intenta de nuevo.', 'error');
    }
}

// ================================================================
// MANEJO DE CONFIGURACIÓN DE NOTIFICACIONES
// ================================================================
async function handleNotificationSettings(e) {
    e.preventDefault();
    
    const emailNotifications = document.getElementById('emailNotifications');
    const emailUpdates = document.getElementById('emailUpdates');
    const whatsappNumber = document.getElementById('whatsappNumber');
    const whatsappNotifications = document.getElementById('whatsappNotifications');
    const whatsappUrgent = document.getElementById('whatsappUrgent');
    
    const settings = {
        emailNotifications: emailNotifications ? emailNotifications.checked : true,
        emailUpdates: emailUpdates ? emailUpdates.checked : true,
        whatsappNumber: whatsappNumber ? whatsappNumber.value.trim() : '',
        whatsappNotifications: whatsappNotifications ? whatsappNotifications.checked : false,
        whatsappUrgent: whatsappUrgent ? whatsappUrgent.checked : false
    };
    
    // Validar número de WhatsApp si está habilitado
    if (settings.whatsappNotifications && !settings.whatsappNumber) {
        showNotification('Por favor, ingresa tu número de WhatsApp.', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/update-notification-settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(settings)
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showNotification('Configuración de notificaciones guardada.', 'success');
        } else {
            showNotification(data.message || 'Error al guardar configuración.', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error de conexión. Intenta de nuevo.', 'error');
    }
}

// ================================================================
// MANEJO DE PREFERENCIAS
// ================================================================
async function handlePreferencesSettings(e) {
    e.preventDefault();
    
    const languageSelect = document.getElementById('language');
    const themeSelect = document.getElementById('theme');
    const timezoneSelect = document.getElementById('timezone');
    
    const preferences = {
        language: languageSelect ? languageSelect.value : 'es',
        theme: themeSelect ? themeSelect.value : 'light',
        timezone: timezoneSelect ? timezoneSelect.value : 'America/Bogota'
    };
    
    try {
        const response = await fetch('/api/update-preferences', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(preferences)
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showNotification('Preferencias guardadas correctamente.', 'success');
            applyPreferences(preferences);
        } else {
            showNotification(data.message || 'Error al guardar preferencias.', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error de conexión. Intenta de nuevo.', 'error');
    }
}

// ================================================================
// APLICAR PREFERENCIAS
// ================================================================
function applyPreferences(preferences) {
    // Aplicar tema
    if (preferences.theme === 'dark') {
        document.body.classList.add('dark-theme');
    } else if (preferences.theme === 'light') {
        document.body.classList.remove('dark-theme');
    } else if (preferences.theme === 'auto') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.body.classList.toggle('dark-theme', prefersDark);
    }
    
    console.log('Preferencias aplicadas:', preferences);
}

// ================================================================
// CARGAR CONFIGURACIONES DESDE BASE DE DATOS Y LOCALSTORAGE
// ================================================================
async function loadSavedSettings() {
    try {
        // Primero intentar cargar desde la base de datos
        const response = await fetch('/api/get-user-settings', {
            method: 'GET',
            credentials: 'include'
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success && data.settings) {
                // Cargar configuración de notificaciones desde BD
                const notif = data.settings.notifications;
                const emailNotifications = document.getElementById('emailNotifications');
                const emailUpdates = document.getElementById('emailUpdates');
                const whatsappNumber = document.getElementById('whatsappNumber');
                const whatsappNotifications = document.getElementById('whatsappNotifications');
                const whatsappUrgent = document.getElementById('whatsappUrgent');
                
                if (emailNotifications) emailNotifications.checked = notif.emailNotifications !== false;
                if (emailUpdates) emailUpdates.checked = notif.emailUpdates !== false;
                if (whatsappNumber && data.settings.whatsappNumber) {
                    whatsappNumber.value = data.settings.whatsappNumber;
                }
                if (whatsappNotifications) whatsappNotifications.checked = notif.whatsappNotifications || false;
                if (whatsappUrgent) whatsappUrgent.checked = notif.whatsappUrgent || false;
                
                // Cargar preferencias desde BD
                const pref = data.settings.preferences;
                const languageSelect = document.getElementById('language');
                const themeSelect = document.getElementById('theme');
                const timezoneSelect = document.getElementById('timezone');
                
                if (languageSelect) languageSelect.value = pref.language || 'es';
                if (themeSelect) themeSelect.value = pref.theme || 'light';
                if (timezoneSelect) timezoneSelect.value = pref.timezone || 'America/Bogota';
                
                applyPreferences(pref);
                
                console.log('Configuraciones cargadas desde base de datos');
                return;
            }
        }
        
        // Si falla la carga desde BD, usar localStorage como fallback
        loadLocalSettings();
        
    } catch (error) {
        console.error('Error cargando configuraciones desde BD:', error);
        // Usar localStorage como fallback
        loadLocalSettings();
    }
}

function loadLocalSettings() {
    try {
        const allSettings = JSON.parse(localStorage.getItem('agroMatchSettings') || '{}');
        
        // Cargar configuración de notificaciones local
        if (allSettings.notifications) {
            const notif = allSettings.notifications;
            const emailNotifications = document.getElementById('emailNotifications');
            const emailUpdates = document.getElementById('emailUpdates');
            const whatsappNumber = document.getElementById('whatsappNumber');
            const whatsappNotifications = document.getElementById('whatsappNotifications');
            const whatsappUrgent = document.getElementById('whatsappUrgent');
            
            if (emailNotifications) emailNotifications.checked = notif.emailNotifications !== false;
            if (emailUpdates) emailUpdates.checked = notif.emailUpdates !== false;
            if (whatsappNumber && notif.whatsappNumber) {
                whatsappNumber.value = notif.whatsappNumber;
            }
            if (whatsappNotifications) whatsappNotifications.checked = notif.whatsappNotifications || false;
            if (whatsappUrgent) whatsappUrgent.checked = notif.whatsappUrgent || false;
        }
        
        // Cargar preferencias locales
        if (allSettings.preferences) {
            const pref = allSettings.preferences;
            const languageSelect = document.getElementById('language');
            const themeSelect = document.getElementById('theme');
            const timezoneSelect = document.getElementById('timezone');
            
            if (languageSelect) languageSelect.value = pref.language || 'es';
            if (themeSelect) themeSelect.value = pref.theme || 'light';
            if (timezoneSelect) timezoneSelect.value = pref.timezone || 'America/Bogota';
            
            applyPreferences(pref);
        }
        
        console.log('Configuraciones locales cargadas como fallback');
        
    } catch (error) {
        console.error('Error cargando configuraciones locales:', error);
    }
}

// ================================================================
// FUNCIONES DE MODAL
// ================================================================
function showModal(title, message, confirmCallback) {
    const modal = document.getElementById('confirmationModal');
    const titleEl = document.getElementById('modalTitle');
    const messageEl = document.getElementById('modalMessage');
    const confirmBtn = document.getElementById('confirmButton');
    
    if (!modal || !titleEl || !messageEl || !confirmBtn) return;
    
    titleEl.textContent = title;
    messageEl.textContent = message;
    modal.style.display = 'flex';
    
    confirmBtn.onclick = function() {
        hideModal();
        if (confirmCallback) confirmCallback();
    };
}

function hideModal() {
    const modal = document.getElementById('confirmationModal');
    if (modal) modal.style.display = 'none';
}

function showDeleteConfirmation() {
    const modal = document.getElementById('deleteAccountModal');
    if (modal) modal.style.display = 'flex';
}

function hideDeleteModal() {
    const modal = document.getElementById('deleteAccountModal');
    if (modal) modal.style.display = 'none';
    
    // Limpiar campos
    const deletePassword = document.getElementById('deletePassword');
    const confirmDelete = document.getElementById('confirmDelete');
    
    if (deletePassword) deletePassword.value = '';
    if (confirmDelete) confirmDelete.checked = false;
}

// ================================================================
// ELIMINACIÓN DE CUENTA
// ================================================================
async function deleteAccount() {
    const passwordField = document.getElementById('deletePassword');
    const confirmedField = document.getElementById('confirmDelete');
    
    const password = passwordField ? passwordField.value : '';
    const confirmed = confirmedField ? confirmedField.checked : false;
    
    if (!password) {
        showNotification('Por favor, ingresa tu contraseña actual.', 'error');
        return;
    }
    
    if (!confirmed) {
        showNotification('Debes confirmar que entiendes que esta acción no se puede deshacer.', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/delete-account', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showNotification('Cuenta eliminada correctamente. Serás redirigido en unos segundos.', 'success');
            
            // Limpiar datos locales
            localStorage.clear();
            sessionStorage.clear();
            
            // Redirigir después de 3 segundos
            setTimeout(() => {
                window.location.href = '/vista/login-trabajador.html';
            }, 3000);
            
        } else {
            showNotification(data.message || 'Error al eliminar la cuenta.', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error de conexión. Intenta de nuevo.', 'error');
    }
    
    hideDeleteModal();
}

// ================================================================
// SISTEMA DE NOTIFICACIONES
// ================================================================
function showNotification(message, type = 'info', duration = 4000) {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    const icon = getNotificationIcon(type);
    
    notification.innerHTML = `
        <div class="notification-content">
            <i class="${icon}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="closeNotification(this.parentElement)">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Agregar estilos si no existen
    if (!document.getElementById('notification-styles')) {
        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 1rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                z-index: 10000;
                max-width: 400px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                animation: slideInRight 0.3s ease-out;
            }
            
            .notification-success {
                border-left: 4px solid #4CAF50;
            }
            
            .notification-error {
                border-left: 4px solid #f44336;
            }
            
            .notification-info {
                border-left: 4px solid #2196F3;
            }
            
            .notification-content {
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .notification-success .notification-content i {
                color: #4CAF50;
            }
            
            .notification-error .notification-content i {
                color: #f44336;
            }
            
            .notification-info .notification-content i {
                color: #2196F3;
            }
            
            .notification-close {
                background: none;
                border: none;
                color: #666;
                cursor: pointer;
                padding: 0.25rem;
                border-radius: 4px;
            }
            
            .notification-close:hover {
                background: #f0f0f0;
            }
            
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOutRight {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(styles);
    }
    
    // Agregar al DOM
    document.body.appendChild(notification);
    
    // Auto-cerrar después del tiempo especificado
    setTimeout(() => {
        closeNotification(notification);
    }, duration);
    
    return notification;
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success':
            return 'fas fa-check-circle';
        case 'error':
            return 'fas fa-exclamation-circle';
        case 'info':
        default:
            return 'fas fa-info-circle';
    }
}

function closeNotification(element) {
    if (element && element.parentNode) {
        element.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            if (element.parentNode) {
                element.parentNode.removeChild(element);
            }
        }, 300);
    }
}

// ================================================================
// FUNCIONES ADICIONALES Y UTILIDADES
// ================================================================

// Detectar cambios en el tema del sistema
if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addListener(function(e) {
        const savedPreferences = JSON.parse(localStorage.getItem('agroMatchSettings') || '{}');
        if (savedPreferences.preferences && savedPreferences.preferences.theme === 'auto') {
            document.body.classList.toggle('dark-theme', e.matches);
        }
    });
}

// Prevenir envío accidental de formularios con Enter
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.target.type !== 'submit' && e.target.tagName !== 'TEXTAREA') {
        const form = e.target.closest('form');
        if (form && !e.ctrlKey && !e.metaKey) {
            e.preventDefault();
        }
    }
});

// Cerrar modales con Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        hideModal();
        hideDeleteModal();
    }
});

// Cerrar modales al hacer clic fuera
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
        hideModal();
        hideDeleteModal();
    }
});

// Validar formularios antes de envío
document.addEventListener('submit', function(e) {
    const form = e.target;
    const requiredFields = form.querySelectorAll('[required]');
    
    for (let field of requiredFields) {
        if (!field.value.trim()) {
            e.preventDefault();
            field.focus();
            const label = field.previousElementSibling;
            const fieldName = label ? label.textContent : 'requerido';
            showNotification(`Por favor, completa el campo: ${fieldName}`, 'error');
            return;
        }
    }
});

console.log('Sistema de configuración del trabajador cargado completamente');

// Exportar funciones para uso global
window.ConfiguracionTrabajador = {
    showNotification,
    showModal,
    hideModal,
    showDeleteConfirmation,
    hideDeleteModal,
    deleteAccount,
    togglePassword
};

// Hacer funciones disponibles globalmente para el HTML
window.togglePassword = togglePassword;
window.hideModal = hideModal;
window.hideDeleteModal = hideDeleteModal;
window.deleteAccount = deleteAccount;
window.showDeleteConfirmation = showDeleteConfirmation;
window.showModal = showModal;
window.showNotification = showNotification;

// Función para obtener y mostrar la foto de perfil del usuario
function loadUserProfilePhoto() {
    fetch('/get_user_session')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.user) {
                const photoUrl = data.user.url_foto;
                
                // Buscar todos los elementos de foto de perfil en la página
                const profilePhotoElements = document.querySelectorAll('.profile-photo, #profilePhoto, .user-avatar, .profile-image');
                
                profilePhotoElements.forEach(element => {
                    if (photoUrl && photoUrl !== '' && photoUrl !== null) {
                        // Si hay foto, mostrarla como imagen de fondo
                        element.style.backgroundImage = `url('${photoUrl}')`;
                        element.style.backgroundSize = 'cover';
                        element.style.backgroundPosition = 'center';
                        element.innerHTML = ''; // Quitar el emoji por defecto
                    } else {
                        // Si no hay foto, mantener el emoji por defecto
                        element.innerHTML = '👤';
                        element.style.backgroundImage = 'none';
                    }
                });
                
                console.log('Foto de perfil cargada:', photoUrl);
            }
        })
        .catch(error => {
            console.error('Error cargando foto de perfil:', error);
        });
}

// ================================================================
// FUNCIONES ADICIONALES PARA ELIMINACIÓN CON REDES SOCIALES
// Agregar estas funciones a tu configuracion-trabajador.js existente
// ================================================================

// Variable global para almacenar el proveedor de red social seleccionado
let selectedSocialProvider = '';

// ================================================================
// FUNCIONES PARA ELIMINAR CUENTA CON REDES SOCIALES
// ================================================================

function deletAccountWithGoogle() {
    selectedSocialProvider = 'google';
    showSocialDeleteModal('Google');
}

function deleteAccountWithFacebook() {
    selectedSocialProvider = 'facebook';
    showSocialDeleteModal('Facebook');
}

function showSocialDeleteModal(providerName) {
    const modal = document.getElementById('deleteSocialModal');
    const providerText = document.getElementById('socialProviderText');
    const confirmBtn = document.getElementById('confirmSocialDeleteBtn');
    
    if (!modal || !providerText || !confirmBtn) return;
    
    providerText.textContent = providerName;
    modal.style.display = 'flex';
    
    // Configurar el botón de confirmación según el proveedor
    if (selectedSocialProvider === 'google') {
        confirmBtn.innerHTML = '<i class="fab fa-google"></i> Eliminar con Google';
        confirmBtn.onclick = processSocialAccountDeletion;
    } else if (selectedSocialProvider === 'facebook') {
        confirmBtn.innerHTML = '<i class="fab fa-facebook-f"></i> Eliminar con Facebook';
        confirmBtn.onclick = processSocialAccountDeletion;
    }
}

function hideSocialDeleteModal() {
    const modal = document.getElementById('deleteSocialModal');
    if (modal) {
        modal.style.display = 'none';
    }
    
    // Limpiar campos
    const confirmSocialDelete = document.getElementById('confirmSocialDelete');
    if (confirmSocialDelete) {
        confirmSocialDelete.checked = false;
    }
    
    selectedSocialProvider = '';
}

async function processSocialAccountDeletion() {
    const confirmSocialDelete = document.getElementById('confirmSocialDelete');
    
    if (!confirmSocialDelete || !confirmSocialDelete.checked) {
        showNotification('Debes confirmar que entiendes que esta acción no se puede deshacer.', 'error');
        return;
    }
    
    if (!selectedSocialProvider) {
        showNotification('Error: No se pudo determinar el proveedor de red social.', 'error');
        return;
    }
    
    try {
        // Mostrar notificación de procesamiento
        showNotification('Procesando eliminación de cuenta...', 'info');
        
        // Construir la URL según el proveedor seleccionado
        let deleteUrl = '';
        if (selectedSocialProvider === 'google') {
            deleteUrl = '/auth/google/delete-account';
        } else if (selectedSocialProvider === 'facebook') {
            deleteUrl = '/auth/facebook/delete-account';
        } else {
            throw new Error('Proveedor no válido');
        }
        
        // Hacer la petición al backend
        const response = await fetch(deleteUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include'
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            hideSocialDeleteModal();
            showNotification('Cuenta eliminada correctamente. Serás redirigido en unos segundos.', 'success');
            
            // Limpiar datos locales
            localStorage.clear();
            sessionStorage.clear();
            
            // Redirigir después de 3 segundos
            setTimeout(() => {
                window.location.href = '/vista/login-trabajador.html';
            }, 3000);
            
        } else {
            showNotification(data.message || 'Error al eliminar la cuenta con la red social.', 'error');
        }
        
    } catch (error) {
        console.error('Error eliminando cuenta con red social:', error);
        showNotification('Error de conexión. Intenta de nuevo.', 'error');
    }
}

// ================================================================
// FUNCIONES PARA VERIFICAR SI EL USUARIO TIENE REDES SOCIALES
// ================================================================

async function checkUserSocialProviders() {
    try {
        const response = await fetch('/get_user_session', {
            method: 'GET',
            credentials: 'include'
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success && data.user) {
                const redSocial = data.user.red_social;
                
                let hasGoogle = false;
                let hasFacebook = false;
                
                // Verificar redes sociales asociadas
                if (redSocial && redSocial !== '') {
                    if (redSocial.includes('google:')) {
                        hasGoogle = true;
                        console.log('Usuario tiene Google asociado');
                    }
                    if (redSocial.includes('facebook:')) {
                        hasFacebook = true;
                        console.log('Usuario tiene Facebook asociado');
                    }
                }
                
                // Mostrar/ocultar botones según corresponda
                const googleBtn = document.getElementById('deleteGoogleBtn');
                const facebookBtn = document.getElementById('deleteFacebookBtn');
                const separator = document.getElementById('deleteSeparator');
                const socialContainer = document.getElementById('deleteSocialContainer');
                const noSocialMessage = document.getElementById('noSocialMessage');
                
                if (hasGoogle && googleBtn) {
                    googleBtn.style.display = 'flex';
                }
                
                if (hasFacebook && facebookBtn) {
                    facebookBtn.style.display = 'flex';
                }
                
                // Si no tiene ninguna red social, ocultar todo y mostrar mensaje
                if (!hasGoogle && !hasFacebook) {
                    if (separator) separator.style.display = 'none';
                    if (socialContainer) socialContainer.style.display = 'none';
                    if (noSocialMessage) noSocialMessage.style.display = 'block';
                    console.log('Usuario no tiene redes sociales asociadas');
                } else {
                    // Si tiene al menos una, mostrar separador y contenedor
                    if (separator) separator.style.display = 'flex';
                    if (socialContainer) socialContainer.style.display = 'block';
                    if (noSocialMessage) noSocialMessage.style.display = 'none';
                }
                
                // Ocultar botones específicos que no corresponden
                if (!hasGoogle && googleBtn) {
                    googleBtn.style.display = 'none';
                }
                if (!hasFacebook && facebookBtn) {
                    facebookBtn.style.display = 'none';
                }
                
            } else {
                console.log('No se pudieron obtener datos del usuario');
            }
        }
    } catch (error) {
        console.error('Error verificando proveedores sociales:', error);
    }
}

// ================================================================
// FUNCIÓN DE PRUEBA (TEMPORAL) - PARA MOSTRAR SIEMPRE LOS BOTONES
// ================================================================

function showAllDeleteButtonsForTesting() {
    // Función temporal para mostrar siempre los botones (para pruebas)
    const googleBtn = document.getElementById('deleteGoogleBtn');
    const facebookBtn = document.getElementById('deleteFacebookBtn');
    const separator = document.getElementById('deleteSeparator');
    const socialContainer = document.getElementById('deleteSocialContainer');
    const noSocialMessage = document.getElementById('noSocialMessage');
    
    if (googleBtn) googleBtn.style.display = 'flex';
    if (facebookBtn) facebookBtn.style.display = 'flex';
    if (separator) separator.style.display = 'flex';
    if (socialContainer) socialContainer.style.display = 'block';
    if (noSocialMessage) noSocialMessage.style.display = 'none';
    
    console.log('Botones de eliminación social mostrados para pruebas');
}

// ================================================================
// MODIFICAR LA FUNCIÓN DE INICIALIZACIÓN EXISTENTE
// ================================================================

// Agregar esta línea a tu función DOMContentLoaded existente:
document.addEventListener('DOMContentLoaded', function() {
    // Tu código existente...
    
    // Agregar estas líneas:
    checkUserSocialProviders();
    
    // TEMPORAL: Para mostrar siempre los botones durante las pruebas
    // Comentar esta línea cuando esté funcionando correctamente
    // showAllDeleteButtonsForTesting();
});

// ================================================================
// HACER FUNCIONES DISPONIBLES GLOBALMENTE
// ================================================================

// Agregar estas líneas al final de tu archivo JS existente:
window.deletAccountWithGoogle = deletAccountWithGoogle;
window.deleteAccountWithFacebook = deleteAccountWithFacebook;
window.showSocialDeleteModal = showSocialDeleteModal;
window.hideSocialDeleteModal = hideSocialDeleteModal;
window.processSocialAccountDeletion = processSocialAccountDeletion;

console.log('Funciones de eliminación social cargadas correctamente');