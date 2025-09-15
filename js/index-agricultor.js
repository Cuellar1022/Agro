/**
 * AgroMatch Dashboard - JavaScript COMPLETO Y CORREGIDO
 * Sistema completo de gestión para agricultores
 */

// ================================================================
// VARIABLES GLOBALES Y CONFIGURACIÓN
// ================================================================

let currentUser = {
    firstName: 'Carlos',
    lastName: 'González',
    role: 'Agricultor',
    email: 'carlos@finca.com',
    isLoggedIn: false
};

let map = null; // Variable para el mapa

// ================================================================
// FUNCIONES DE AUTENTICACIÓN Y SESIÓN
// ================================================================

/**
 * Obtener datos del usuario desde el backend Python
 */
async function fetchUserSession() {
    try {
        console.log('🔄 Obteniendo datos de sesión del servidor...');
        
        const response = await fetch('/get_user_session', {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.ok) {
            const data = await response.json();
            
            if (data.success && data.user) {
                // Actualizar datos del usuario
                currentUser = {
                    firstName: data.user.first_name,
                    lastName: data.user.last_name,
                    role: data.user.role,
                    email: data.user.email,
                    username: data.user.username,
                    userId: data.user.user_id,
                    telefono: data.user.telefono || '',
                    isLoggedIn: true
                };

                console.log('✅ Datos de usuario obtenidos:', currentUser);
                updateUIWithUserData();
                return true;
            } else {
                console.log('❌ No hay sesión activa en el servidor');
                handleNoSession();
                return false;
            }
        } else {
            console.log('❌ Error al obtener sesión:', response.status);
            handleNoSession();
            return false;
        }
    } catch (error) {
        console.error('❌ Error conectando con el servidor:', error);
        // En caso de error de conexión, usar datos por defecto para demo
        console.log('🔄 Usando datos por defecto para demo');
        currentUser.isLoggedIn = true;
        updateUIWithUserData();
        return true;
    }
}

/**
 * Actualizar la UI con los datos del usuario
 */
function updateUIWithUserData() {
    // Actualizar nombre en el dropdown
    const userNameElement = document.querySelector('.profile-dropdown-name');
    if (userNameElement) {
        userNameElement.textContent = `${currentUser.firstName} ${currentUser.lastName}`;
    }

    // Actualizar bienvenida en el header si existe
    updateHeaderWithUserName(currentUser.firstName, currentUser.role);

    console.log('✅ UI actualizada con datos del usuario');
}

/**
 * Manejar cuando no hay sesión
 */
function handleNoSession() {
    showStatusMessage('Sesión expirada. Redirigiendo al login...', 'warning');
    setTimeout(() => {
        // Redirigir según el rol esperado
        if (window.location.pathname.includes('agricultor')) {
            window.location.href = '/vista/login-trabajador.html';
        } else {
            window.location.href = '/vista/login-trabajador.html';
        }
    }, 2000);
}

/**
 * Actualizar el header con el nombre del usuario
 */
function updateHeaderWithUserName(firstName, userRole) {
    const logo = document.querySelector('.logo');
    
    // Verificar si ya existe el elemento de bienvenida
    let welcomeElement = document.querySelector('.user-welcome');
    
    if (logo && !welcomeElement) {
        welcomeElement = document.createElement('div');
        welcomeElement.className = 'user-welcome';
        
        const roleText = userRole === 'Agricultor' ? 'Agricultor' : 'Trabajador';
        const icon = userRole === 'Agricultor' ? '🌾' : '👨‍🌾';
        
        welcomeElement.innerHTML = `
            <span>${icon}</span>
            <span>Bienvenido, <strong style="color: #4a7c59;">${firstName}</strong></span>
            <span style="font-size: 12px; color: #64748b; margin-left: 5px;">(${roleText})</span>
        `;
        
        // Agregar estilos
        welcomeElement.style.cssText = `
            font-size: 16px;
            color: #1e3a2e;
            font-weight: 600;
            margin-left: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
        `;
        
        logo.parentNode.insertBefore(welcomeElement, logo.nextSibling);
    }
}

// ================================================================
// SISTEMA DE DROPDOWN DINÁMICO - SOLUCIÓN CORREGIDA
// ================================================================

/**
 * Crear dropdown dinámicamente en el body
 */
function createDynamicDropdown() {
    // Remover dropdown existente si ya existe
    const existingDropdown = document.getElementById('dynamicProfileDropdown');
    if (existingDropdown) {
        existingDropdown.remove();
    }

    // Crear nuevo dropdown
    const dropdown = document.createElement('div');
    dropdown.id = 'dynamicProfileDropdown';
    dropdown.innerHTML = `
        <div class="dynamic-dropdown-content">
            <!-- Header del dropdown -->
            <div class="dynamic-dropdown-header">
                <div class="dynamic-dropdown-avatar">
                    <i class="fas fa-user"></i>
                </div>
                <div class="dynamic-dropdown-name">${currentUser.firstName} ${currentUser.lastName}</div>
                <div class="dynamic-dropdown-role">
                    <i class="fas fa-seedling"></i>
                    <span>${currentUser.role}</span>
                </div>
            </div>
            
            <!-- Menú de opciones -->
            <div class="dynamic-dropdown-menu">
                <div class="dynamic-dropdown-item" onclick="viewProfile(); closeDynamicDropdown()">
                    <div class="icon"><i class="fas fa-user-circle"></i></div>
                    <span>Mi Perfil</span>
                </div>
                <div class="dynamic-dropdown-item" onclick="viewSettings(); closeDynamicDropdown()">
                    <div class="icon"><i class="fas fa-cog"></i></div>
                    <span>Configuración</span>
                </div>
                <div class="dynamic-dropdown-item" onclick="viewStatistics(); closeDynamicDropdown()">
                    <div class="icon"><i class="fas fa-chart-bar"></i></div>
                    <span>Estadísticas</span>
                </div>
                <div class="dynamic-dropdown-item" onclick="viewHistory(); closeDynamicDropdown()">
                    <div class="icon"><i class="fas fa-history"></i></div>
                    <span>Historial</span>
                </div>
                <div class="dynamic-dropdown-item" onclick="viewSupport(); closeDynamicDropdown()">
                    <div class="icon"><i class="fas fa-question-circle"></i></div>
                    <span>Ayuda y Soporte</span>
                </div>
                <div class="dynamic-dropdown-item logout" onclick="confirmLogout(); closeDynamicDropdown()">
                    <div class="icon"><i class="fas fa-sign-out-alt"></i></div>
                    <span>Cerrar Sesión</span>
                </div>
            </div>
        </div>
    `;

    // Estilos inline para garantizar que funcionen
    dropdown.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        z-index: 999999;
        background: white;
        border-radius: 15px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(144, 238, 144, 0.2);
        min-width: 280px;
        opacity: 0;
        visibility: hidden;
        transform: translateY(-15px) scale(0.95);
        transition: all 0.3s ease;
        overflow: hidden;
    `;

    // Añadir al body
    document.body.appendChild(dropdown);

    return dropdown;
}

/**
 * Mostrar dropdown dinámico
 */
function showDynamicDropdown() {
    const dropdown = createDynamicDropdown();
    
    // Calcular posición basada en el botón de perfil
    const profileBtn = document.getElementById('profileMenuBtn');
    if (profileBtn) {
        const rect = profileBtn.getBoundingClientRect();
        dropdown.style.top = (rect.bottom + 10) + 'px';
        dropdown.style.right = (window.innerWidth - rect.right) + 'px';
    }

    // Mostrar con animación
    requestAnimationFrame(() => {
        dropdown.style.opacity = '1';
        dropdown.style.visibility = 'visible';
        dropdown.style.transform = 'translateY(0) scale(1)';
    });

    // Mostrar overlay
    const overlay = document.getElementById('overlay');
    if (overlay) {
        overlay.classList.add('show');
    }

    return dropdown;
}

/**
 * Cerrar dropdown dinámico
 */
function closeDynamicDropdown() {
    const dropdown = document.getElementById('dynamicProfileDropdown');
    const overlay = document.getElementById('overlay');
    
    if (dropdown) {
        dropdown.style.opacity = '0';
        dropdown.style.visibility = 'hidden';
        dropdown.style.transform = 'translateY(-15px) scale(0.95)';
        
        setTimeout(() => {
            if (dropdown.parentNode) {
                dropdown.parentNode.removeChild(dropdown);
            }
        }, 300);
    }

    if (overlay) {
        overlay.classList.remove('show');
    }

    // Remover clase active del botón
    const profileBtn = document.getElementById('profileMenuBtn');
    if (profileBtn) {
        profileBtn.classList.remove('active');
    }
}

/**
 * Toggle del menú de perfil - FUNCIÓN PRINCIPAL
 */
function toggleProfileMenu() {
    const existingDropdown = document.getElementById('dynamicProfileDropdown');
    const profileBtn = document.getElementById('profileMenuBtn');
    
    if (existingDropdown) {
        closeDynamicDropdown();
    } else {
        showDynamicDropdown();
        if (profileBtn) {
            profileBtn.classList.add('active');
        }
    }
}

/**
 * Cerrar dropdown original (función de compatibilidad)
 */
function closeProfileDropdown() {
    closeDynamicDropdown();
}

// ================================================================
// FUNCIONES DEL MENÚ DE PERFIL
// ================================================================

/**
 * Ver perfil del usuario
 */
function viewProfile() {
    showStatusMessage('Abriendo perfil de usuario...', 'info');
    
    setTimeout(() => {
        const profileInfo = `👤 PERFIL DE USUARIO
                
Nombre: ${currentUser.firstName} ${currentUser.lastName}
Email: ${currentUser.email}
Rol: ${currentUser.role}
${currentUser.telefono ? `Teléfono: ${currentUser.telefono}` : ''}

Estado: Activo ✅
Fecha de registro: Enero 2024
Contratos completados: 15
Calificación: 4.8/5 ⭐`;
        
        alert(profileInfo);
    }, 500);
}

/**
 * Ver configuración
 */
function viewSettings() {
    showStatusMessage('Cargando configuración...', 'info');
    
    setTimeout(() => {
        alert(`⚙️ CONFIGURACIÓN DE ${currentUser.firstName}:

• Notificaciones: Activadas 🔔
• Idioma: Español 🇪🇸
• Zona horaria: Colombia (UTC-5) 🕐
• Privacidad: Público 👥
• Modo oscuro: Desactivado 🌞
• Notificaciones por email: Activadas 📧

Para cambiar estos ajustes, ve a tu panel de configuración.`);
    }, 500);
}

/**
 * Ver estadísticas
 */
function viewStatistics() {
    showStatusMessage('Cargando estadísticas...', 'info');
    
    setTimeout(() => {
        alert(`📊 ESTADÍSTICAS DE ${currentUser.firstName}:

📈 RENDIMIENTO GENERAL:
• Contratos completados: 15 ✅
• Contratos en progreso: 3 🔄
• Calificación promedio: 4.8/5 ⭐
• Trabajadores contratados: 47 👥

⏱️ TIEMPO DE RESPUESTA:
• Promedio: 2 horas
• Último mes: 1.5 horas (Mejorando! 📈)

💰 FINANCIERO:
• Total pagado: $2,450,000 COP
• Promedio por contrato: $163,333 COP`);
    }, 500);
}

/**
 * Ver historial
 */
function viewHistory() {
    showStatusMessage('Cargando historial...', 'info');
    
    setTimeout(() => {
        alert(`💼 HISTORIAL DE TRABAJOS DE ${currentUser.firstName}:

📅 RECIENTES:
• Cosecha de Café - Completado ✅ (⭐⭐⭐⭐⭐)
• Siembra de Maíz - En progreso 🔄
• Fumigación - Completado ✅ (⭐⭐⭐⭐⭐)
• Recolección Frutas - Completado ✅ (⭐⭐⭐⭐)

📊 ESTADÍSTICAS DEL MES:
• Trabajos completados: 4
• Trabajadores satisfechos: 12/12
• Puntuación promedio: 4.8/5

🏆 LOGROS:
• Agricultor confiable (15+ trabajos)
• Respuesta rápida (< 2h promedio)
• Excelente calificación (4.8/5)`);
    }, 500);
}

/**
 * Ver soporte
 */
function viewSupport() {
    showStatusMessage('Contactando soporte...', 'info');
    
    setTimeout(() => {
        alert(`🆘 SOPORTE AGROMATCH

📞 CONTACTO DIRECTO:
• Teléfono: +57 300 123 4567
• WhatsApp: +57 300 123 4567
• Email: soporte@agromatch.com

💬 CHAT EN LÍNEA:
• Disponible: 24/7
• Tiempo de respuesta: < 15 min

🕐 HORARIO TELEFÓNICO:
• Lunes a Domingo: 6:00 AM - 10:00 PM

📖 RECURSOS:
• FAQ: agromatch.com/ayuda
• Tutoriales: agromatch.com/tutoriales
• Guía del agricultor: agromatch.com/guia`);
    }, 500);
}

// ================================================================
// FUNCIÓN DE LOGOUT CON MODAL DE CONFIRMACIÓN
// ================================================================

/**
 * Confirmar logout
 */
function confirmLogout() {
    createLogoutModal();
}

/**
 * Crear modal de logout
 */
function createLogoutModal() {
    const modal = document.createElement('div');
    modal.className = 'modal-backdrop';
    modal.innerHTML = `
        <div class="modal-content">
            <div style="font-size: 50px; margin-bottom: 15px;">🚪</div>
            <h3 style="color: #1e3a2e; margin-bottom: 10px;">Cerrar Sesión</h3>
            <p style="color: #64748b; margin-bottom: 25px;">
                ¿Estás seguro de que deseas cerrar sesión, ${currentUser.firstName}?
            </p>
            <div class="modal-actions">
                <button class="modal-btn modal-btn-cancel" onclick="closeLogoutModal()">
                    Cancelar
                </button>
                <button class="modal-btn modal-btn-confirm" onclick="executeLogout()">
                    Sí, Cerrar Sesión
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeLogoutModal();
        }
    });
}

/**
 * Cerrar modal de logout
 */
function closeLogoutModal() {
    const modal = document.querySelector('.modal-backdrop');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(modal);
        }, 300);
    }
}

/**
 * Ejecutar logout con integración Python
 */
async function executeLogout() {
    closeLogoutModal();
    showStatusMessage('Cerrando sesión...', 'info');
    
    try {
        console.log('🔄 Enviando solicitud de logout al servidor...');
        
        const response = await fetch('/logout', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Logout exitoso:', data);
            
            // Limpiar datos locales
            currentUser.isLoggedIn = false;
            
            showStatusMessage(`¡Hasta pronto, ${currentUser.firstName}! 👋`, 'success');
            
            // Redirigir después de un momento
            setTimeout(() => {
                // Determinar a qué login redirigir según el rol
                if (currentUser.role === 'Agricultor') {
                    window.location.href = '/vista/login-trabajador.html';
                } else {
                    window.location.href = '/vista/login-trabajador.html';
                }
            }, 2000);
        } else {
            throw new Error(`Error del servidor: ${response.status}`);
        }
    } catch (error) {
        console.error('❌ Error en logout:', error);
        
        // En caso de error, limpiar datos locales y redirigir de todos modos
        showStatusMessage('Sesión cerrada localmente', 'warning');
        currentUser.isLoggedIn = false;
        
        setTimeout(() => {
            if (currentUser.role === 'Agricultor') {
                window.location.href = '/vista/login-trabajador.html';
            } else {
                window.location.href = '/vista/login-trabajador.html';
            }
        }, 1500);
    }
}

// ================================================================
// FUNCIONES DEL DASHBOARD
// ================================================================

/**
 * Crear nueva oferta
 */
function createNewOffer() {
    const button = event.target;
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creando...';
    button.disabled = true;
    
    setTimeout(() => {
        showStatusMessage('Redirigiendo al formulario de nueva oferta...', 'info');
        button.innerHTML = originalText;
        button.disabled = false;
        // En tu app real: window.location.href = '/vista/crear-oferta.html';
    }, 2000);
}

/**
 * Ver postulaciones
 */
function viewApplications(button, count) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cargando...';
    button.disabled = true;
    
    setTimeout(() => {
        showStatusMessage(`Mostrando ${count} postulaciones`, 'info');
        button.innerHTML = originalText;
        button.disabled = false;
        // En tu app real: window.location.href = `postulaciones.html?count=${count}`;
    }, 1500);
}

/**
 * Ver progreso del trabajo
 */
function viewProgress(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cargando...';
    button.disabled = true;
    
    setTimeout(() => {
        showStatusMessage('Mostrando progreso del trabajo...', 'info');
        button.innerHTML = originalText;
        button.disabled = false;
        // En tu app real: window.location.href = '/vista/progreso-trabajo.html';
    }, 1500);
}

/**
 * Mostrar notificaciones
 */
function showNotifications() {
    showStatusMessage('Abriendo panel de notificaciones...', 'info');
    setTimeout(() => {
        alert(`🔔 NOTIFICACIONES RECIENTES:

📝 NUEVAS POSTULACIONES:
• 2 trabajadores aplicaron a "Cosecha de Café"
• 1 trabajador aplicó a "Siembra de Maíz"

⏰ RECORDATORIOS:
• Contrato de recolección termina mañana
• Revisar progreso de fumigación

⭐ CALIFICACIONES:
• Juan Pérez completó su trabajo (5⭐)
• María García calificó tu trabajo (4⭐)

💰 PAGOS:
• Pago pendiente: $150,000 COP`);
    }, 800);
}

/**
 * Abrir mapa - MODIFICADA PARA USAR LEAFLET
 */
function openMap() {
    showStatusMessage('Mapa interactivo ya disponible abajo...', 'info');
    // Hacer scroll al mapa
    const mapElement = document.getElementById('map');
    if (mapElement) {
        mapElement.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Manejar notificación
 */
function handleNotification(element) {
    element.style.opacity = '0.7';
    element.style.transform = 'translateX(10px)';
    
    setTimeout(() => {
        element.style.opacity = '1';
        element.style.transform = 'translateX(0)';
        showStatusMessage('Notificación marcada como leída', 'success');
    }, 200);
}

// ================================================================
// NUEVA FUNCIÓN PARA INICIALIZAR LEAFLET MAP (REEMPLAZA GOOGLE MAPS)
// ================================================================

/**
 * Inicializar mapa con Leaflet
 */
function initMap() {
    console.log('Inicializando mapa con Leaflet...');
    
    const mapElement = document.getElementById("map");
    if (!mapElement) {
        console.error('Elemento del mapa no encontrado');
        return;
    }
    
    try {
        // Coordenadas de la finca (Chinchiná, Caldas)
        const fincaLocation = [5.0056, -75.6063];
        
        // Crear el mapa con Leaflet
        map = L.map('map').setView(fincaLocation, 13);
        
        // Agregar tiles de OpenStreetMap (gratis)
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18,
        }).addTo(map);
        
        // Trabajadores disponibles con ubicaciones
        const availableWorkers = [
            { lat: 5.0156, lng: -75.6163, name: "Juan Pérez", experience: "Café", rating: 4.9 },
            { lat: 4.9956, lng: -75.5963, name: "María García", experience: "Siembra", rating: 4.8 },
            { lat: 5.0256, lng: -75.5863, name: "Carlos López", experience: "Fumigación", rating: 4.7 },
            { lat: 4.9856, lng: -75.6263, name: "Ana Rodríguez", experience: "Cosecha", rating: 4.6 },
            { lat: 5.0356, lng: -75.6463, name: "Luis Martínez", experience: "Mantenimiento", rating: 4.8 }
        ];
        
        // Icono personalizado para la finca
        const fincaIcon = L.divIcon({
            className: 'custom-finca-marker',
            html: '<div style="background-color: #4a7c59; width: 30px; height: 30px; border-radius: 50%; border: 4px solid #fff; box-shadow: 0 3px 8px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center;"><i class="fas fa-home" style="color: white; font-size: 14px;"></i></div>',
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });
        
        // Icono personalizado para trabajadores
        const workerIcon = L.divIcon({
            className: 'custom-worker-marker',
            html: '<div style="background-color: #dc2626; width: 25px; height: 25px; border-radius: 50%; border: 3px solid #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center;"><i class="fas fa-user" style="color: white; font-size: 10px;"></i></div>',
            iconSize: [25, 25],
            iconAnchor: [12, 12]
        });
        
        // Agregar marcador de la finca
        L.marker(fincaLocation, { icon: fincaIcon }).addTo(map)
            .bindPopup(`
                <div style="padding: 10px; font-family: 'Segoe UI', sans-serif; min-width: 160px; text-align: center;">
                    <h4 style="margin: 0 0 8px 0; color: #1e3a2e; font-size: 14px;">Tu Finca</h4>
                    <p style="margin: 0 0 6px 0; color: #4a7c59; font-weight: bold; font-size: 12px;">Vereda El Paraíso</p>
                    <p style="margin: 0; color: #64748b; font-size: 11px;">Chinchiná, Caldas</p>
                </div>
            `);
        
        // Agregar marcadores para trabajadores disponibles
        availableWorkers.forEach((worker, index) => {
            const marker = L.marker([worker.lat, worker.lng], { icon: workerIcon }).addTo(map);
            
            // Crear estrellas para la calificación
            const stars = '★'.repeat(Math.floor(worker.rating)) + '☆'.repeat(5 - Math.floor(worker.rating));
            
            // Popup con información del trabajador
            const popupContent = `
                <div style="padding: 10px; font-family: 'Segoe UI', sans-serif; min-width: 180px;">
                    <h4 style="margin: 0 0 6px 0; color: #1e3a2e; font-size: 13px;">${worker.name}</h4>
                    <p style="margin: 0 0 4px 0; color: #4a7c59; font-weight: bold; font-size: 11px;">Especialidad: ${worker.experience}</p>
                    <p style="margin: 0 0 8px 0; color: #f59e0b; font-size: 11px;">${stars} ${worker.rating}/5</p>
                    <button onclick="contactWorker('${worker.name}')" style="
                        background: linear-gradient(135deg, #4a7c59, #1e3a2e);
                        color: white;
                        border: none;
                        padding: 6px 12px;
                        border-radius: 5px;
                        cursor: pointer;
                        font-size: 11px;
                        font-weight: 600;
                        width: 100%;
                    ">Contactar</button>
                </div>
            `;
            
            marker.bindPopup(popupContent);
        });
        
        console.log('Mapa inicializado correctamente con Leaflet');
        
    } catch (error) {
        console.error('Error inicializando el mapa:', error);
        handleMapError();
    }
}

/**
 * Contactar trabajador desde el mapa
 */
function contactWorker(workerName) {
    showStatusMessage(`Contactando a ${workerName}...`, 'info');
    setTimeout(() => {
        alert(`📞 CONTACTANDO A ${workerName.toUpperCase()}:

✅ Mensaje enviado exitosamente
📱 El trabajador recibirá tu solicitud
⏰ Tiempo de respuesta estimado: 2-4 horas

💬 Tu mensaje:
"Hola ${workerName}, estoy interesado en contratarte para trabajos en mi finca. ¿Podrías contactarme?"

📧 También se envió notificación por email
📲 Recibirás una respuesta en tu panel de notificaciones`);
    }, 1500);
}

/**
 * Función para manejar errores del mapa
 */
function handleMapError() {
    console.error('Error cargando el mapa');
    const mapElement = document.getElementById("map");
    if (mapElement) {
        mapElement.innerHTML = `
            <div style="
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100%;
                background: linear-gradient(135deg, rgba(144, 238, 144, 0.2), rgba(74, 124, 89, 0.1));
                border-radius: 15px;
                color: #1e3a2e;
                text-align: center;
                padding: 20px;
            ">
                <div>
                    <div style="font-size: 48px; margin-bottom: 15px; color: #4a7c59;">
                        <i class="fas fa-map-marked-alt"></i>
                    </div>
                    <strong style="font-size: 16px; color: #1e3a2e;">Mapa no disponible</strong><br>
                    <small style="color: #4a7c59; font-size: 14px; display: block; margin-top: 5px;">
                        📍 5 trabajadores en 10km de radio
                    </small>
                </div>
            </div>
        `;
    }
}

// ================================================================
// FUNCIÓN PARA MOSTRAR MENSAJES DE ESTADO
// ================================================================

/**
 * Mostrar mensaje de estado
 */
function showStatusMessage(message, type = 'info') {
    const messageElement = document.createElement('div');
    messageElement.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        z-index: 9999;
        max-width: 300px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        animation: slideInRight 0.3s ease;
    `;
    
    switch(type) {
        case 'success':
            messageElement.style.background = 'linear-gradient(135deg, #4a7c59, #1e3a2e)';
            messageElement.innerHTML = `<i class="fas fa-check-circle" style="margin-right: 8px;"></i>${message}`;
            break;
        case 'error':
            messageElement.style.background = 'linear-gradient(135deg, #dc2626, #991b1b)';
            messageElement.innerHTML = `<i class="fas fa-exclamation-triangle" style="margin-right: 8px;"></i>${message}`;
            break;
        case 'warning':
            messageElement.style.background = 'linear-gradient(135deg, #f59e0b, #d97706)';
            messageElement.innerHTML = `<i class="fas fa-exclamation-circle" style="margin-right: 8px;"></i>${message}`;
            break;
        default:
            messageElement.style.background = 'linear-gradient(135deg, #6366f1, #4f46e5)';
            messageElement.innerHTML = `<i class="fas fa-info-circle" style="margin-right: 8px;"></i>${message}`;
    }
    
    document.body.appendChild(messageElement);
    
    // Remover mensaje después de 3 segundos
    setTimeout(() => {
        messageElement.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (document.body.contains(messageElement)) {
                document.body.removeChild(messageElement);
            }
        }, 300);
    }, 3000);
}

// ================================================================
// EVENT LISTENERS Y INICIALIZACIÓN
// ================================================================

/**
 * Validar sesión periódicamente
 */
function startSessionValidation() {
    setInterval(async () => {
        try {
            const response = await fetch('/validate_session', {
                method: 'GET',
                credentials: 'include'
            });
            
            if (!response.ok || !(await response.json()).valid) {
                console.log('⚠️ Sesión inválida detectada');
                handleNoSession();
            }
        } catch (error) {
            console.log('⚠️ Error validando sesión:', error);
        }
    }, 300000); // Verificar cada 5 minutos
}

/**
 * Actualización en tiempo real de notificaciones
 */
function startNotificationUpdates() {
    setInterval(() => {
        const badges = document.querySelectorAll('.notification-badge');
        badges.forEach(badge => {
            if (Math.random() > 0.98) { // 2% probabilidad
                const currentCount = parseInt(badge.textContent);
                badge.textContent = currentCount + 1;
                
                // Animación de nueva notificación
                badge.style.animation = 'none';
                setTimeout(() => {
                    badge.style.animation = 'pulse 2s infinite';
                }, 10);
                
                showStatusMessage('Nueva notificación recibida', 'info');
            }
        });
    }, 10000); // Cada 10 segundos
}

/**
 * Configurar event listeners
 */
function setupEventListeners() {
    // Event listeners para dropdown dinámico
    document.addEventListener('click', function(event) {
        const dropdown = document.getElementById('dynamicProfileDropdown');
        const profileBtn = document.getElementById('profileMenuBtn');
        
        if (dropdown && 
            !dropdown.contains(event.target) && 
            !profileBtn.contains(event.target)) {
            closeDynamicDropdown();
        }
    });

    // Cerrar dropdown con overlay
    const overlay = document.getElementById('overlay');
    if (overlay) {
        overlay.addEventListener('click', closeDynamicDropdown);
    }

    // Cerrar dropdown con tecla Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeDynamicDropdown();
        }
    });

    // Manejo de errores globales
    window.addEventListener('error', function(event) {
        console.error('❌ Error en la aplicación:', event.error);
        showStatusMessage('Ha ocurrido un error. Recargando...', 'error');
    });

    window.addEventListener('unhandledrejection', function(event) {
        console.error('❌ Promesa rechazada:', event.reason);
        showStatusMessage('Error de conexión con el servidor', 'warning');
    });
}

/**
 * Animaciones de entrada
 */
function setupEntryAnimations() {
    const cards = document.querySelectorAll('.offer-card, .stat-card, .notification-item');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

/**
 * Inyectar estilos CSS dinámicos para el dropdown
 */
function injectDynamicStyles() {
    const dynamicStyles = document.createElement('style');
    dynamicStyles.textContent = `
    .dynamic-dropdown-content {
        background: white;
        border-radius: 15px;
        overflow: hidden;
    }

    .dynamic-dropdown-header {
        padding: 20px;
        background: linear-gradient(135deg, rgba(74, 124, 89, 0.1), rgba(144, 238, 144, 0.1));
        border-bottom: 1px solid rgba(144, 238, 144, 0.2);
        text-align: center;
    }

    .dynamic-dropdown-avatar {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #4a7c59, #1e3a2e);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin: 0 auto 12px;
        box-shadow: 0 4px 15px rgba(74, 124, 89, 0.3);
    }

    .dynamic-dropdown-name {
        font-size: 18px;
        font-weight: 700;
        color: #1e3a2e;
        margin-bottom: 4px;
    }

    .dynamic-dropdown-role {
        font-size: 14px;
        color: #4a7c59;
        font-weight: 500;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }

    .dynamic-dropdown-menu {
        padding: 8px 0;
    }

    .dynamic-dropdown-item {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px 20px;
        color: #1e3a2e;
        cursor: pointer;
        transition: all 0.3s ease;
        border-bottom: 1px solid rgba(144, 238, 144, 0.1);
        font-weight: 500;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .dynamic-dropdown-item:last-child {
        border-bottom: none;
    }

    .dynamic-dropdown-item:hover {
        background: linear-gradient(135deg, rgba(144, 238, 144, 0.1), rgba(74, 124, 89, 0.05));
        color: #4a7c59;
        padding-left: 25px;
    }

    .dynamic-dropdown-item .icon {
        width: 20px;
        text-align: center;
        font-size: 16px;
        color: #64748b;
        transition: color 0.3s ease;
        flex-shrink: 0;
    }

    .dynamic-dropdown-item:hover .icon {
        color: #4a7c59;
    }

    .dynamic-dropdown-item.logout {
        color: #dc2626;
        border-top: 2px solid rgba(220, 38, 38, 0.1);
        margin-top: 8px;
    }

    .dynamic-dropdown-item.logout:hover {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.1), rgba(220, 38, 38, 0.05));
        color: #dc2626;
    }

    .dynamic-dropdown-item.logout .icon {
        color: #dc2626;
    }

    /* Responsive para dropdown dinámico */
    @media (max-width: 768px) {
        #dynamicProfileDropdown {
            right: 10px !important;
            left: 10px !important;
            min-width: auto !important;
            max-width: calc(100vw - 20px) !important;
        }
    }

    /* Animaciones para mensajes */
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

    /* Estilos para el modal */
    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
    }

    .modal-backdrop.show {
        opacity: 1;
        visibility: visible;
    }

    .modal-content {
        background: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        max-width: 400px;
        margin: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        transform: scale(0.9) translateY(20px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .modal-backdrop.show .modal-content {
        transform: scale(1) translateY(0);
    }

    .modal-actions {
        display: flex;
        gap: 15px;
        justify-content: center;
        margin-top: 25px;
    }

    .modal-btn {
        padding: 12px 24px;
        border-radius: 10px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .modal-btn-cancel {
        background: #f1f5f9;
        color: #64748b;
        border: 2px solid #e2e8f0;
    }

    .modal-btn-cancel:hover {
        background: #e2e8f0;
        color: #475569;
    }

    .modal-btn-confirm {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white;
    }

    .modal-btn-confirm:hover {
        background: linear-gradient(135deg, #991b1b, #7f1d1d);
    }
    `;

    document.head.appendChild(dynamicStyles);
}

/**
 * Inicialización principal
 */
async function initializeDashboard() {
    console.log('🌱 Iniciando AgroMatch Dashboard...');
    
    // Inyectar estilos dinámicos
    injectDynamicStyles();
    
    // Configurar event listeners
    setupEventListeners();
    
    // Obtener datos de sesión del servidor
    const sessionValid = await fetchUserSession();
    
    if (!sessionValid) {
        console.log('❌ No se pudo obtener sesión válida');
        return;
    }
    
    // Inicializar el mapa después de un breve delay para asegurar que el DOM esté listo
    setTimeout(initMap, 500);
    
    // Configurar animaciones
    setupEntryAnimations();
    
    // Iniciar validación de sesión periódica
    startSessionValidation();
    
    // Iniciar actualizaciones de notificaciones
    startNotificationUpdates();
    
    console.log('✅ Dashboard inicializado correctamente');
    console.log('🎯 Sistema de dropdown dinámico activo - DEBE funcionar ahora');
    showStatusMessage('¡Bienvenido al dashboard de AgroMatch!', 'success');
}

// ================================================================
// INICIO DE LA APLICACIÓN
// ================================================================

// Asegurarse de que las funciones estén disponibles globalmente
window.initMap = initMap;
window.handleMapError = handleMapError;
window.contactWorker = contactWorker;

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', initializeDashboard);

// Logs de debugging
console.log('🚀 AgroMatch Dashboard - Sistema completo cargado');
console.log('🔐 Autenticación integrada con Python Flask');
console.log('👤 Gestión completa de perfiles y sesiones');
console.log('💡 NUEVO: Dropdown dinámico con position:fixed garantizado');
console.log('🗺️ NUEVO: Mapa interactivo con Leaflet (gratis)');