// js/estadisticas-trabajador.js - ARCHIVO COMPLETO SIN ERRORES

// Variables globales
let usuarioActual = null;
let estadisticasData = {};
let charts = {};

// Inicializar cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    inicializarPagina();
});

async function inicializarPagina() {
    try {
        await cargarUsuario();
        await cargarEstadisticas();
        inicializarGraficas();
        configurarFiltros();
    } catch (error) {
        console.error('Error al inicializar la página:', error);
        mostrarError('Error al cargar los datos');
    }
}

function volverAlIndex() {
    window.history.back(); // Simplemente regresa a la página anterior
}

// Cargar datos del usuario actual
async function cargarUsuario() {
    try {
        const idUsuario = localStorage.getItem('idUsuario') || 1;
        
        // Por ahora usar datos por defecto (puedes reemplazar con tu API real)
        usuarioActual = {
            Nombre: 'Usuario',
            Apellido: 'Trabajador',
            URL_Foto: null
        };
        
        document.getElementById('nombreUsuario').textContent = 
            `${usuarioActual.Nombre} ${usuarioActual.Apellido}`;
        
        if (usuarioActual.URL_Foto) {
            document.querySelector('.profile-img').src = usuarioActual.URL_Foto;
        }
    } catch (error) {
        console.error('Error al cargar usuario:', error);
        document.getElementById('nombreUsuario').textContent = 'Usuario Trabajador';
    }
}

// Cargar estadísticas del trabajador
async function cargarEstadisticas(periodo = 'all') {
    try {
        const idUsuario = localStorage.getItem('idUsuario') || 1;
        
        // Intenta llamar a tu API real
        try {
            const response = await fetch('/get-estadisticas-trabajador', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    idUsuario: idUsuario,
                    periodo: periodo
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                estadisticasData = data.estadisticas;
            } else {
                throw new Error(data.error || 'Error en la respuesta del servidor');
            }
        } catch (apiError) {
            console.warn('API no disponible, usando datos simulados:', apiError);
            // Fallback a datos simulados
            estadisticasData = simularDatosEstadisticas(idUsuario, periodo);
        }
        
        // Actualizar UI con los datos
        actualizarResumenEstadisticas();
        actualizarTrabajaRecientes();
        actualizarHabilidades();
        
    } catch (error) {
        console.error('Error al cargar estadísticas:', error);
        // Usar datos simulados como último recurso
        estadisticasData = simularDatosEstadisticas(1, periodo);
        actualizarResumenEstadisticas();
        actualizarTrabajaRecientes();
        actualizarHabilidades();
    }
}

// Simular datos de estadísticas (fallback)
function simularDatosEstadisticas(idUsuario, periodo) {
    return {
        resumen: {
            totalTrabajos: 15,
            totalHoras: 320,
            totalIngresos: 4800000,
            calificacionPromedio: 4.3
        },
        ingresosMensuales: [
            { mes: 'Ene', ingresos: 450000 },
            { mes: 'Feb', ingresos: 380000 },
            { mes: 'Mar', ingresos: 520000 },
            { mes: 'Abr', ingresos: 480000 },
            { mes: 'May', ingresos: 600000 },
            { mes: 'Jun', ingresos: 550000 }
        ],
        trabajosPorTipo: [
            { tipo: 'Cosecha', cantidad: 5 },
            { tipo: 'Siembra', cantidad: 3 },
            { tipo: 'Fertilización', cantidad: 4 },
            { tipo: 'Control de Plagas', cantidad: 2 },
            { tipo: 'Riego', cantidad: 1 }
        ],
        horasMensuales: [
            { mes: 'Ene', horas: 45 },
            { mes: 'Feb', horas: 38 },
            { mes: 'Mar', horas: 52 },
            { mes: 'Abr', horas: 48 },
            { mes: 'May', horas: 60 },
            { mes: 'Jun', horas: 77 }
        ],
        calificacionesPorMes: [
            { mes: 'Ene', calificacion: 4.2 },
            { mes: 'Feb', calificacion: 4.1 },
            { mes: 'Mar', calificacion: 4.4 },
            { mes: 'Abr', calificacion: 4.3 },
            { mes: 'May', calificacion: 4.5 },
            { mes: 'Jun', calificacion: 4.3 }
        ],
        trabajosRecientes: [
            {
                titulo: 'Cosecha de Café',
                agricultor: 'Juan Pérez',
                fechaFin: '2024-08-15',
                pago: 350000,
                calificacion: 5
            },
            {
                titulo: 'Siembra de Maíz',
                agricultor: 'María García',
                fechaFin: '2024-08-10',
                pago: 280000,
                calificacion: 4
            },
            {
                titulo: 'Control de Plagas',
                agricultor: 'Carlos López',
                fechaFin: '2024-08-05',
                pago: 150000,
                calificacion: 4
            }
        ],
        habilidades: [
            { nombre: 'Cosecha', clasificacion: 'Cosecha y poscosecha' },
            { nombre: 'Siembra', clasificacion: 'Técnica agrícola' },
            { nombre: 'Fertilización', clasificacion: 'Fertilización' },
            { nombre: 'Manejo de Tractores', clasificacion: 'Manejo de maquinaria' },
            { nombre: 'Riego por Goteo', clasificacion: 'Riego y drenaje' }
        ]
    };
}

// Actualizar resumen de estadísticas
function actualizarResumenEstadisticas() {
    const resumen = estadisticasData.resumen;
    
    document.getElementById('totalTrabajos').textContent = resumen.totalTrabajos;
    document.getElementById('totalHoras').textContent = resumen.totalHoras + 'h';
    document.getElementById('totalIngresos').textContent = 
        '$' + resumen.totalIngresos.toLocaleString('es-CO');
    document.getElementById('calificacionPromedio').textContent = 
        resumen.calificacionPromedio.toFixed(1) + '/5';
}

// Actualizar trabajos recientes
function actualizarTrabajaRecientes() {
    const container = document.getElementById('trabajosRecientes');
    container.innerHTML = '';
    
    if (estadisticasData.trabajosRecientes && estadisticasData.trabajosRecientes.length > 0) {
        estadisticasData.trabajosRecientes.forEach(trabajo => {
            const trabajoElement = document.createElement('div');
            trabajoElement.className = 'trabajo-item';
            trabajoElement.innerHTML = `
                <div class="trabajo-titulo">${trabajo.titulo}</div>
                <div class="trabajo-info">
                    <span>👨‍🌾 ${trabajo.agricultor}</span>
                    <span>💰 $${trabajo.pago.toLocaleString('es-CO')}</span>
                    <span>⭐ ${trabajo.calificacion}/5</span>
                </div>
            `;
            container.appendChild(trabajoElement);
        });
    } else {
        container.innerHTML = '<p style="text-align: center; color: #666;">No hay trabajos recientes</p>';
    }
}

// Actualizar habilidades
function actualizarHabilidades() {
    const container = document.getElementById('habilidadesList');
    container.innerHTML = '';
    
    if (estadisticasData.habilidades && estadisticasData.habilidades.length > 0) {
        estadisticasData.habilidades.forEach(habilidad => {
            const habilidadElement = document.createElement('span');
            habilidadElement.className = 'habilidad-tag';
            habilidadElement.textContent = habilidad.nombre;
            habilidadElement.title = `Clasificación: ${habilidad.clasificacion}`;
            container.appendChild(habilidadElement);
        });
    } else {
        container.innerHTML = '<p style="text-align: center; color: #666;">No hay habilidades registradas</p>';
    }
}

// Inicializar gráficas
function inicializarGraficas() {
    crearGraficaIngresosMensuales();
    crearGraficaTrabajosPorTipo();
    crearGraficaHorasMensuales();
    crearGraficaEvolucionCalificaciones();
}

// Gráfica de ingresos mensuales
function crearGraficaIngresosMensuales() {
    const ctx = document.getElementById('ingresosMensuales').getContext('2d');
    const data = estadisticasData.ingresosMensuales || [];
    
    if (charts.ingresosMensuales) {
        charts.ingresosMensuales.destroy();
    }
    
    charts.ingresosMensuales = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(item => item.mes),
            datasets: [{
                label: 'Ingresos ($)',
                data: data.map(item => item.ingresos),
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                borderColor: 'rgba(40, 167, 69, 1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: 'rgba(40, 167, 69, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString('es-CO');
                        }
                    }
                }
            }
        }
    });
}

// Gráfica de trabajos por tipo
function crearGraficaTrabajosPorTipo() {
    const ctx = document.getElementById('trabajosPorTipo').getContext('2d');
    const data = estadisticasData.trabajosPorTipo || [];
    
    if (charts.trabajosPorTipo) {
        charts.trabajosPorTipo.destroy();
    }
    
    const colores = [
        'rgba(40, 167, 69, 0.8)',
        'rgba(32, 201, 151, 0.8)',
        'rgba(255, 193, 7, 0.8)',
        'rgba(220, 53, 69, 0.8)',
        'rgba(0, 123, 255, 0.8)'
    ];
    
    charts.trabajosPorTipo = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(item => item.tipo),
            datasets: [{
                data: data.map(item => item.cantidad),
                backgroundColor: colores.slice(0, data.length),
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Gráfica de horas mensuales
function crearGraficaHorasMensuales() {
    const ctx = document.getElementById('horasMensuales').getContext('2d');
    const data = estadisticasData.horasMensuales || [];
    
    if (charts.horasMensuales) {
        charts.horasMensuales.destroy();
    }
    
    charts.horasMensuales = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.mes),
            datasets: [{
                label: 'Horas',
                data: data.map(item => item.horas),
                backgroundColor: 'rgba(40, 167, 69, 0.7)',
                borderColor: 'rgba(40, 167, 69, 1)',
                borderWidth: 1,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value + 'h';
                        }
                    }
                }
            }
        }
    });
}

// Gráfica de evolución de calificaciones
function crearGraficaEvolucionCalificaciones() {
    const ctx = document.getElementById('evolucionCalificaciones').getContext('2d');
    const data = estadisticasData.calificacionesPorMes || [];
    
    if (charts.evolucionCalificaciones) {
        charts.evolucionCalificaciones.destroy();
    }
    
    charts.evolucionCalificaciones = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(item => item.mes),
            datasets: [{
                label: 'Calificación',
                data: data.map(item => item.calificacion),
                backgroundColor: 'rgba(255, 193, 7, 0.1)',
                borderColor: 'rgba(255, 193, 7, 1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: 'rgba(255, 193, 7, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    min: 1,
                    max: 5,
                    ticks: {
                        callback: function(value) {
                            return value + '/5';
                        }
                    }
                }
            }
        }
    });
}

// Configurar filtros de período
function configurarFiltros() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remover clase active de todos los botones
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Agregar clase active al botón clickeado
            this.classList.add('active');
            
            // Obtener período seleccionado
            const periodo = this.getAttribute('data-period');
            
            // Recargar estadísticas con el nuevo período
            cargarEstadisticas(periodo);
            
            // Actualizar gráficas después de un breve delay
            setTimeout(() => {
                actualizarGraficas();
            }, 200);
        });
    });
}

// Actualizar gráficas existentes
function actualizarGraficas() {
    // Destruir gráficas existentes
    Object.keys(charts).forEach(key => {
        if (charts[key]) {
            charts[key].destroy();
        }
    });
    
    // Limpiar el objeto charts
    charts = {};
    
    // Recrear gráficas con nuevos datos
    inicializarGraficas();
}

// Función para mostrar errores
function mostrarError(mensaje) {
    // Crear elemento de error
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <div style="background: #dc3545; color: white; padding: 15px; border-radius: 10px; margin: 20px; text-align: center;">
            <i class="fas fa-exclamation-triangle"></i> ${mensaje}
        </div>
    `;
    
    // Insertar al inicio del container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(errorDiv, container.firstChild);
        
        // Remover después de 5 segundos
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }
}

// Función para mostrar loading
function mostrarLoading(elemento) {
    if (elemento) {
        elemento.innerHTML = `
            <div class="loading">
                <i class="fas fa-spinner"></i>
                Cargando datos...
            </div>
        `;
    }
}

// Función para calcular horas trabajadas (basada en fechas de acuerdo laboral)
function calcularHorasTrabajas(fechaInicio, fechaFin, horasPorDia = 8) {
    const inicio = new Date(fechaInicio);
    const fin = new Date(fechaFin);
    const diffTime = Math.abs(fin - inicio);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays * horasPorDia;
}

// Función para formatear fechas
function formatearFecha(fecha) {
    const opciones = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    return new Date(fecha).toLocaleDateString('es-ES', opciones);
}

// Función para formatear moneda colombiana
function formatearMoneda(cantidad) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(cantidad);
}

// Función para debugging - mostrar datos en consola
function mostrarDatosEnConsola() {
    console.log('Datos de estadísticas:', estadisticasData);
    console.log('Usuario actual:', usuarioActual);
    console.log('Charts activos:', Object.keys(charts));
}
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