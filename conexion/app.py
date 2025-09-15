# ================================================================
# APLICACIÓN PRINCIPAL FLASK - AGROMATCH PYTHON MODIFICADO
# Ruta: conexion/app.py
# ================================================================

from flask import Flask, request, redirect, url_for, session, jsonify, render_template, send_from_directory
from flask import Flask, request, redirect, url_for, session, jsonify
from flask import Flask, request, jsonify, session
import hashlib
from urllib.parse import quote
import uuid
import bcrypt
from conexion import execute_query
import re
from urllib.parse import quote, unquote
import os
from flask import Flask, render_template, send_from_directory
import uuid  
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import request, jsonify, session
from conexion import execute_query
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = 'agromatch_secret_key_2024'  # Cambia esto por una clave más segura

# ================================================================
# CONFIGURACIÓN DE RUTAS ESTÁTICAS MODIFICADAS PARA TU ESTRUCTURA
# ================================================================

@app.route('/vista/<path:filename>')
def serve_vista(filename):
    """Sirve archivos HTML desde la carpeta vista"""
    try:
        # Obtener la ruta absoluta del directorio actual
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        
        # Verificar que el archivo existe
        file_path = os.path.join(vista_path, filename)
        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {file_path}")
            return f"Archivo no encontrado: {filename}", 404
            
        print(f"✅ Sirviendo archivo: {file_path}")
        return send_from_directory(vista_path, filename)
    except Exception as e:
        print(f"❌ Error sirviendo vista {filename}: {str(e)}")
        return f"Error sirviendo archivo: {filename}", 500

# NUEVAS RUTAS PARA DASHBOARD DE TRABAJADOR
@app.route('/dashboard-trabajador.css')
def serve_dashboard_trabajador_css():
    """Sirve el archivo dashboard-trabajador.css"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        
        response = send_from_directory(vista_path, 'index-trabajador.css')
        response.headers['Content-Type'] = 'text/css'
        return response
    except Exception as e:
        return f"Error sirviendo CSS: {str(e)}", 500

@app.route('/dashboard-trabajador.js')
def serve_dashboard_trabajador_js():
    """Sirve el archivo dashboard-trabajador.js"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        
        response = send_from_directory(vista_path, 'index-trabajador.js')
        response.headers['Content-Type'] = 'application/javascript'
        return response
    except Exception as e:
        return f"Error sirviendo JS: {str(e)}", 500

@app.route('/script.js')
def serve_script():
    """Sirve el archivo script.js desde la carpeta vista"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        
        file_path = os.path.join(vista_path, 'script.js')
        if not os.path.exists(file_path):
            print(f"❌ script.js no encontrado: {file_path}")
            return "script.js no encontrado", 404
            
        print(f"✅ Sirviendo script.js: {file_path}")
        response = send_from_directory(vista_path, 'script.js')
        response.headers['Content-Type'] = 'application/javascript'
        return response
    except Exception as e:
        print(f"❌ Error sirviendo script.js: {str(e)}")
        return f"Error sirviendo script.js: {str(e)}", 500

@app.route('/css/<path:filename>')
def serve_css(filename):
    """Sirve archivos CSS desde assent/css"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(base_dir, '..', 'assent', 'css')
        css_path = os.path.abspath(css_path)
        
        if not os.path.exists(os.path.join(css_path, filename)):
            print(f"❌ CSS no encontrado: {filename}")
            return f"CSS no encontrado: {filename}", 404
            
        response = send_from_directory(css_path, filename)
        response.headers['Content-Type'] = 'text/css'
        return response
    except Exception as e:
        print(f"❌ Error sirviendo CSS {filename}: {str(e)}")
        return f"Error sirviendo CSS: {filename}", 500

@app.route('/js/<path:filename>')
def serve_js(filename):
    """Sirve archivos JavaScript desde js/"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        js_path = os.path.join(base_dir, '..', 'js')
        js_path = os.path.abspath(js_path)
        
        if not os.path.exists(os.path.join(js_path, filename)):
            print(f"❌ JS no encontrado: {filename}")
            return f"JS no encontrado: {filename}", 404
            
        response = send_from_directory(js_path, filename)
        response.headers['Content-Type'] = 'application/javascript'
        return response
    except Exception as e:
        print(f"❌ Error sirviendo JS {filename}: {str(e)}")
        return f"Error sirviendo JS: {filename}", 500

@app.route('/assent/css/<path:filename>')
def serve_assent_css(filename):
    """Sirve archivos CSS desde assent/css"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assent_css_path = os.path.join(base_dir, '..', 'assent', 'css')
        assent_css_path = os.path.abspath(assent_css_path)
        
        if not os.path.exists(os.path.join(assent_css_path, filename)):
            print(f"❌ Assent CSS no encontrado: {filename}")
            return f"Assent CSS no encontrado: {filename}", 404
            
        response = send_from_directory(assent_css_path, filename)
        response.headers['Content-Type'] = 'text/css'
        return response
    except Exception as e:
        print(f"❌ Error sirviendo Assent CSS {filename}: {str(e)}")
        return f"Error sirviendo Assent CSS: {filename}", 500

@app.route('/img/<path:filename>')
def serve_img(filename):
    """Sirve archivos de imágenes"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, '..', 'img')
        img_path = os.path.abspath(img_path)
        
        if not os.path.exists(os.path.join(img_path, filename)):
            print(f"❌ Imagen no encontrada: {filename}")
            return f"Imagen no encontrada: {filename}", 404
            
        return send_from_directory(img_path, filename)
    except Exception as e:
        print(f"❌ Error sirviendo imagen {filename}: {str(e)}")
        return f"Error sirviendo imagen: {filename}", 500

@app.route('/assent/img/<path:filename>')
def serve_assent_img(filename):
    """Sirve archivos de imágenes desde assent/img"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assent_img_path = os.path.join(base_dir, '..', 'assent', 'img')
        assent_img_path = os.path.abspath(assent_img_path)
        
        if not os.path.exists(os.path.join(assent_img_path, filename)):
            print(f"❌ Assent imagen no encontrada: {filename}")
            return f"Assent imagen no encontrada: {filename}", 404
            
        return send_from_directory(assent_img_path, filename)
    except Exception as e:
        print(f"❌ Error sirviendo Assent imagen {filename}: {str(e)}")
        return f"Error sirviendo Assent imagen: {filename}", 500

@app.route('/assent/js/<path:filename>')
def serve_assent_js(filename):
    """Sirve archivos JavaScript desde assent/js"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assent_js_path = os.path.join(base_dir, '..', 'assent', 'js')
        assent_js_path = os.path.abspath(assent_js_path)
        
        if not os.path.exists(os.path.join(assent_js_path, filename)):
            print(f"❌ Assent JS no encontrado: {filename}")
            return f"Assent JS no encontrado: {filename}", 404
            
        response = send_from_directory(assent_js_path, filename)
        response.headers['Content-Type'] = 'application/javascript'
        return response
    except Exception as e:
        print(f"❌ Error sirviendo Assent JS {filename}: {str(e)}")
        return f"Error sirviendo Assent JS: {filename}", 500

# RUTA ESPECIAL PARA EL DASHBOARD DE AGRICULTOR
@app.route('/vista/dashboard-agricultor.html')
def serve_dashboard_agricultor():
    """Sirve el dashboard del agricultor con archivos separados"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        
        # Verificar que existen los archivos necesarios
        html_file = os.path.join(vista_path, 'dashboard-agricultor.html')
        css_file = os.path.join(vista_path, 'styles.css')
        js_file = os.path.join(vista_path, 'script.js')
        
        if not os.path.exists(html_file):
            print(f"❌ dashboard-agricultor.html no encontrado: {html_file}")
            return "Dashboard de agricultor no encontrado", 404
            
        print(f"✅ Sirviendo dashboard del agricultor")
        print(f"   HTML: {'✅' if os.path.exists(html_file) else '❌'}")
        print(f"   CSS:  {'✅' if os.path.exists(css_file) else '❌'}")
        print(f"   JS:   {'✅' if os.path.exists(js_file) else '❌'}")
        
        return send_from_directory(vista_path, 'dashboard-agricultor.html')
        
    except Exception as e:
        print(f"❌ Error sirviendo dashboard del agricultor: {str(e)}")
        return f"Error sirviendo dashboard: {str(e)}", 500
    
# ================================================================
# RUTA DE ESTADISTICAS DEL TRABAJADOR
# ================================================================    
    
# Ruta para la página de estadísticas
import os

@app.route('/estadisticas-trabajador')
def estadisticas_trabajador():
    file_path = os.path.join('vista', 'estadisticas-trabajador.html')
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return f"Archivo no encontrado en: {os.path.abspath(file_path)}", 404

# Ruta para servir archivos de la carpeta js
@app.route('/js/<path:filename>')
def serve_js_files(filename):
    return send_from_directory('js', filename)

@app.route('/index-trabajador.html')
def serve_index_trabajador():
    return send_from_directory('vista', 'index-trabajador.html')

# Ruta para obtener estadísticas (sin API separada)
    try:
        from conexion.get_estadisticas_trabajador import obtener_estadisticas_trabajador
        
        data = request.get_json()
        id_usuario = data.get('idUsuario')
        periodo = data.get('periodo', 'all')
        
        if not id_usuario:
            return jsonify({'success': False, 'error': 'ID de usuario requerido'})
        
        estadisticas = obtener_estadisticas_trabajador(id_usuario, periodo)
        return jsonify({'success': True, 'estadisticas': estadisticas})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ================================================================
# RUTA PARA VERIFICAR ARCHIVOS (DEBUGGING MEJORADO)
# ================================================================

# ...existing code...
@app.route('/check_files')
def check_files():
    """Verifica qué archivos existen en las carpetas"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Verificar carpetas
        folders_to_check = ['vista', 'css', 'js', 'img', 'assent/css', 'assent/js', 'assent/img']
        result = {
            'base_dir': base_dir,
            'folders': {},
            'dashboard_files': {}
        }
        
        for folder in folders_to_check:
            folder_path = os.path.join(base_dir, '..', folder)
            folder_path = os.path.abspath(folder_path)
            
            if os.path.exists(folder_path):
                files = os.listdir(folder_path)
                result['folders'][folder] = {
                    'exists': True,
                    'path': folder_path,
                    'files': files
                }
            else:
                result['folders'][folder] = {
                    'exists': False,
                    'path': folder_path,
                    'files': []
                }
        
        # Verificar específicamente los archivos del dashboard de agricultor
        vista_path = os.path.join(base_dir, '..', 'vista')
        dashboard_files = {
            'dashboard-agricultor.html': os.path.join(vista_path, 'dashboard-agricultor.html'),
            'styles.css': os.path.join(vista_path, 'styles.css'),
            'script.js': os.path.join(vista_path, 'script.js')
        }
        
        for file_name, file_path in dashboard_files.items():
            result['dashboard_files'][file_name] = {
                'exists': os.path.exists(file_path),
                'path': file_path
            }
        
        # Verificar archivos del dashboard de trabajador
        trabajador_files = {
            'index-trabajador.html': os.path.join(vista_path, 'index-trabajador.html'),
            'dashboard-trabajador.css': os.path.join(vista_path, 'index-trabajador.css'),
            'dashboard-trabajador.js': os.path.join(vista_path, 'index-trabajador.js')
        }

        result['trabajador_files'] = {}
        for file_name, file_path in trabajador_files.items():
            result['trabajador_files'][file_name] = {
                'exists': os.path.exists(file_path),
                'path': file_path
            }

        return jsonify(result)
# ...existing code...
        
        # Verificar específicamente los archivos del dashboard
        vista_path = os.path.join(base_dir, '..', 'vista')
        dashboard_files = {
            'dashboard-agricultor.html': os.path.join(vista_path, 'dashboard-agricultor.html'),
            'styles.css': os.path.join(vista_path, 'styles.css'),
            'script.js': os.path.join(vista_path, 'script.js')
        }
        
        for file_name, file_path in dashboard_files.items():
            result['dashboard_files'][file_name] = {
                'exists': os.path.exists(file_path),
                'path': file_path
            }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'base_dir': os.path.dirname(os.path.abspath(__file__))
        })
        
# ================================================================
# FUNCIONES AUXILIARES
# ================================================================

def validate_email(email):
    """Valida formato de email"""
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(pattern, email) is not None

def validate_name(name):
    """Valida que el nombre solo contenga letras y espacios"""
    pattern = r'^[A-Za-zÀ-ÿ\s]+$'
    return re.match(pattern, name) is not None

def hash_password(password):
    """Hashea la contraseña usando bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verifica una contraseña contra su hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# ================================================================
# RUTA DE REGISTRO MEJORADA
# ================================================================

@app.route('/registro.py', methods=['POST'])
def registro():
    """Procesa el registro de usuarios (Trabajador o Agricultor)"""
    
    try:
        # Obtener y limpiar datos del formulario
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        correo = request.form.get('correo', '').strip()
        telefono = request.form.get('telefono', '').strip() if request.form.get('telefono') else None
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        rol = request.form.get('rol', '').strip()
        
        # Debug: Imprimir información del registro
        print(f"=== NUEVO REGISTRO ===")
        print(f"Nombre: {nombre}")
        print(f"Apellido: {apellido}")
        print(f"Correo: {correo}")
        print(f"Rol recibido: '{rol}'")
        print(f"Tipo de rol: {type(rol)}")
        
        # Validación de campos obligatorios
        errores = []
        
        if not nombre:
            errores.append('El nombre es obligatorio')
        elif not validate_name(nombre):
            errores.append('El nombre solo puede contener letras y espacios')
        
        if not apellido:
            errores.append('El apellido es obligatorio')
        elif not validate_name(apellido):
            errores.append('El apellido solo puede contener letras y espacios')
        
        if not correo:
            errores.append('El correo es obligatorio')
        elif not validate_email(correo):
            errores.append('El formato del correo electrónico no es válido')
        
        if not password:
            errores.append('La contraseña es obligatoria')
        elif len(password) < 8:
            errores.append('La contraseña debe tener mínimo 8 caracteres')
        
        if not confirm_password:
            errores.append('Debe confirmar la contraseña')
        elif password != confirm_password:
            errores.append('Las contraseñas no coinciden')
        
        if not rol:
            errores.append('No se pudo determinar el tipo de usuario')
        elif rol not in ['Trabajador', 'Agricultor']:
            errores.append('Tipo de usuario no válido')
        
        # Validar términos y condiciones
        if not request.form.get('terminos'):
            errores.append('Debe aceptar los términos y condiciones')
        
        # Si hay errores, mostrarlos
        if errores:
            print(f"Errores encontrados: {errores}")
            raise Exception('<br>'.join(errores))
        
        # Verificar si el email ya existe
        existing_user = execute_query(
            "SELECT ID_Usuario FROM Usuario WHERE Correo = %s",
            (correo,),
            fetch_one=True
        )
        
        if existing_user:
            # Determinar el enlace de login según el rol
            login_link = '/vista/login-trabajador.html' if rol == 'Agricultor' else '/vista/login-trabajador.html'
            raise Exception(f'El correo electrónico ya está registrado. <a href="{login_link}">¿Ya tienes cuenta? Inicia sesión aquí</a>')
        
        # Encriptar contraseña
        hashed_password = hash_password(password)
        
        # Insertar usuario en la base de datos
        user_id = execute_query(
            "INSERT INTO Usuario (Nombre, Apellido, Correo, Contrasena, Telefono, Rol) VALUES (%s, %s, %s, %s, %s, %s)",
            (nombre, apellido, correo, hashed_password, telefono, rol)
        )
        
        print(f"Usuario registrado exitosamente con ID: {user_id}")
        
        # VERIFICAR QUE EL ARCHIVO DE LOGIN EXISTE ANTES DE REDIRIGIR
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        if rol == 'Trabajador':
            login_file = 'login-trabajador.html'
            tipo_usuario = 'trabajador'
            print("🔄 Preparando redirección a login de TRABAJADOR")
        elif rol == 'Agricultor':
            login_file = 'login-trabajador.html'
            tipo_usuario = 'agricultor'
            print("🔄 Preparando redirección a login de AGRICULTOR")
        else:
            print(f"❌ Rol no reconocido: '{rol}'")
            login_file = 'login-trabajador.html'
            tipo_usuario = 'trabajador'
        
        # Verificar que el archivo existe
        login_file_path = os.path.join(base_dir, '..', 'vista', login_file)
        login_file_path = os.path.abspath(login_file_path)
        
        if not os.path.exists(login_file_path):
            print(f"❌ ARCHIVO DE LOGIN NO EXISTE: {login_file_path}")
            # Si no existe el archivo específico, usar el genérico
            login_file = 'login-trabajador.html'
            tipo_usuario = 'trabajador'
        else:
            print(f"✅ Archivo de login encontrado: {login_file_path}")
        
        redirect_url = f'/vista/{login_file}'
        
        mensaje_exito = f"¡Registro exitoso {nombre}! Tu cuenta como {tipo_usuario} fue creada. Ahora puedes iniciar sesión con tu correo y contraseña."
        
        print(f"✅ Mensaje: {mensaje_exito}")
        print(f"🎯 Redirigiendo a: {redirect_url}")
        
        # Redireccionar con mensaje de éxito
        return redirect(f"{redirect_url}?message={quote(mensaje_exito)}&type=success")
        
    except Exception as e:
        print(f"❌ Error en registro: {str(e)}")
        
        # Determinar la URL de retorno según el rol
        return_url = '/vista/registro-trabajador.html'  # Por defecto
        
        if rol:
            if rol == 'Agricultor':
                # Verificar que existe el archivo de registro de agricultor
                base_dir = os.path.dirname(os.path.abspath(__file__))
                reg_file_path = os.path.join(base_dir, '..', 'vista', 'registro-agricultor.html')
                if os.path.exists(reg_file_path):
                    return_url = '/vista/registro-agricultor.html'
                else:
                    print(f"❌ Archivo de registro de agricultor no existe: {reg_file_path}")
                    return_url = '/vista/registro-trabajador.html'
            else:
                return_url = '/vista/registro-trabajador.html'
        else:
            # Si no hay rol, usar el referer para determinar dónde regresar
            referer = request.headers.get('Referer', '')
            if 'registro-agricultor.html' in referer:
                return_url = '/vista/registro-agricultor.html'
        
        print(f"🔙 Redirigiendo con error a: {return_url}")
        
        # Redireccionar de vuelta al formulario con el mensaje de error
        error_message = quote(str(e))
        return redirect(f"{return_url}?message={error_message}&type=error")

# ================================================================
# RUTA DE LOGIN MEJORADA
# ================================================================

@app.route('/login.py', methods=['POST'])
def login():
    """Procesa el login de usuarios"""
    
    try:
        # Recoger datos del formulario
        email = request.form.get('email', '').strip()
        password = request.form.get('contrasena', '')
        
        print(f"🔐 Intento de login para: {email}")
        
        # Validaciones básicas
        if not email or not password:
            raise Exception('Por favor completa todos los campos.')
        
        # Buscar usuario en la base de datos
        user = execute_query(
            """SELECT u.ID_Usuario, u.Nombre, u.Apellido, u.Correo, u.Contrasena, u.Rol, u.Estado, u.Telefono
               FROM Usuario u 
               WHERE u.Correo = %s OR u.Telefono = %s""",
            (email, email),
            fetch_one=True
        )
        
        if not user:
            raise Exception('Credenciales incorrectas.')
        
        # Verificar contraseña
        if not verify_password(password, user['Contrasena']):
            raise Exception('Credenciales incorrectas.')
        
        # Verificar que el usuario esté activo
        if user['Estado'] != 'Activo':
            raise Exception('Tu cuenta está inactiva. Contacta al administrador.')
        
        # Crear sesión con todos los datos necesarios
        session['user_id'] = user['ID_Usuario']
        session['username'] = user['Correo']  # Usamos el email como username
        session['first_name'] = user['Nombre']
        session['last_name'] = user['Apellido']
        session['email'] = user['Correo']
        session['user_role'] = user['Rol']
        session['user_name'] = f"{user['Nombre']} {user['Apellido']}"
        session['telefono'] = user.get('Telefono', '')
        
        print(f"✅ Login exitoso para: {user['Nombre']} {user['Apellido']} - Rol: {user['Rol']}")
        print(f"📊 Datos de sesión guardados: ID={user['ID_Usuario']}, Role={user['Rol']}")
        
        # Redireccionar según el rol - ACTUALIZADO PARA USAR LOS NUEVOS DASHBOARDS
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        if user['Rol'] == 'Agricultor':
            # Para agricultor, usar el nuevo dashboard separado
            dashboard_file = 'index-agricultor.html'
            redirect_url = '/vista/index-agricultor.html'
            
            dashboard_path = os.path.join(base_dir, '..', 'vista', dashboard_file)
            if not os.path.exists(dashboard_path):
                print(f"❌ Dashboard de agricultor no existe: {dashboard_path}")
                redirect_url = '/vista/index-agricultor.html'
            
        elif user['Rol'] == 'Trabajador':
            redirect_url = '/vista/index-trabajador.html'
            
        elif user['Rol'] == 'Administrador':
            redirect_url = '/vista/dashboard-admin.html'
            
        else:
            raise Exception('Rol de usuario no válido.')
        
        print(f"🎯 Redirigiendo a: {redirect_url}")
        return redirect(redirect_url)
        
    except Exception as e:
        print(f"❌ Error en login: {str(e)}")
        
        # Redireccionar con error - determinar la página de login correcta
        referer = request.headers.get('Referer', '')
        if 'login-trabajador.html' in referer:
            login_page = '/vista/login-trabajador.html'
        else:
            login_page = '/vista/login-trabajador.html'
        
        error_message = quote(str(e))
        return redirect(f"{login_page}?message={error_message}&type=error")



# ================================================================
# NUEVOS ENDPOINTS PARA MANEJO DE SESIÓN
# ================================================================

@app.route('/get_user_session')
def get_user_session():
    """Obtiene los datos de la sesión actual del usuario - VERSIÓN ACTUALIZADA"""
    try:
        if 'user_id' in session:
            user_id = session['user_id']
            
            # Obtener datos actualizados del usuario desde la base de datos
            user_data = execute_query(
                """SELECT ID_Usuario, Nombre, Apellido, Correo, Telefono, 
                          URL_Foto, Red_Social, Rol, Estado, Fecha_Registro
                   FROM Usuario WHERE ID_Usuario = %s""",
                (user_id,),
                fetch_one=True
            )
            
            if not user_data:
                return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
            
            # Actualizar datos de sesión con información fresca de la BD
            session['first_name'] = user_data['Nombre']
            session['last_name'] = user_data['Apellido']
            session['email'] = user_data['Correo']
            session['user_name'] = f"{user_data['Nombre']} {user_data['Apellido']}"
            session['telefono'] = user_data.get('Telefono', '')
            
            print(f"Obteniendo datos de sesión para usuario ID: {user_id}")
            
            return jsonify({
                'success': True,
                'user': {
                    'user_id': user_data['ID_Usuario'],
                    'full_name': f"{user_data['Nombre']} {user_data['Apellido']}",
                    'nombre': user_data['Nombre'],
                    'apellido': user_data['Apellido'],
                    'first_name': user_data['Nombre'],
                    'last_name': user_data['Apellido'],
                    'email': user_data['Correo'],
                    'telefono': user_data.get('Telefono', ''),
                    'url_foto': user_data.get('URL_Foto'),
                    'red_social': user_data.get('Red_Social', ''),
                    'rol': user_data['Rol'],
                    'role': user_data['Rol'],  # Alias para compatibilidad
                    'estado': user_data['Estado'],
                    'fecha_registro': user_data['Fecha_Registro'].isoformat() if user_data['Fecha_Registro'] else None,
                    'username': user_data['Correo']  # Para compatibilidad
                }
            })
        else:
            print("No hay sesión activa")
            return jsonify({'success': False, 'error': 'No hay sesión activa'}), 401
            
    except Exception as e:
        print(f"Error obteniendo sesión: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500



@app.route('/get_user_data.py', methods=['GET'])
def get_user_data():
    """API para obtener datos del usuario logueado (mantener compatibilidad)"""
    
    # Verificar que el usuario esté logueado
    if 'user_id' not in session:
        return jsonify({
            'error': True,
            'message': 'Usuario no autenticado'
        }), 401
    
    # Devolver datos del usuario
    return jsonify({
        'error': False,
        'data': {
            'user_id': session['user_id'],
            'user_name': session['user_name'],
            'user_email': session['email'],
            'user_role': session['user_role'],
            'first_name': session['first_name'],
            'last_name': session['last_name'],
            'username': session['username'],
            'telefono': session.get('telefono', '')
        }
    })

# ================================================================
# RUTAS DE DASHBOARD ACTUALIZADAS
# ================================================================

@app.route('/dashboard-agricultor')
def dashboard_agricultor():
    """Ruta para el dashboard del agricultor"""
    if 'user_id' not in session:
        print("❌ Usuario no autenticado, redirigiendo a login")
        return redirect('/vista/login-trabajador.html')
    
    # Verificar que el usuario sea agricultor
    if session.get('user_role') != 'Agricultor':
        print(f"❌ Usuario no es agricultor: {session.get('user_role')}")
        return redirect('/vista/index-trabajador.html')
    
    print(f"✅ Acceso autorizado al dashboard de agricultor: {session.get('user_name')}")
    return redirect('/vista/dashboard-agricultor.html')

@app.route('/dashboard-trabajador')
def dashboard_trabajador():
    """Ruta para el dashboard del trabajador"""
    if 'user_id' not in session:
        print("❌ Usuario no autenticado, redirigiendo a login")
        return redirect('/vista/login-trabajador.html')
    
    # Verificar que el usuario sea trabajador
    if session.get('user_role') != 'Trabajador':
        print(f"❌ Usuario no es trabajador: {session.get('user_role')}")
        return redirect('/vista/index-agricultor.html')
    
    print(f"✅ Acceso autorizado al dashboard de trabajador: {session.get('user_name')}")
    return redirect('/vista/index-trabajador.html')

@app.route('/dashboard-admin')
def dashboard_admin():
    """Ruta para el dashboard del administrador"""
    if 'user_id' not in session:
        print("❌ Usuario no autenticado, redirigiendo a login")
        return redirect('/vista/login-trabajador.html')
    
    # Verificar que el usuario sea administrador
    if session.get('user_role') != 'Administrador':
        print(f"❌ Usuario no es administrador: {session.get('user_role')}")
        return redirect('/vista/index-trabajador.html')
    
    print(f"✅ Acceso autorizado al dashboard de administrador: {session.get('user_name')}")
    return redirect('/vista/dashboard-admin.html')


# ================================================================
# RUTA DE LOGOUT MEJORADA
# ================================================================

@app.route('/logout', methods=['POST'])
def logout():
    """Cierra la sesión del usuario (nueva ruta)"""
    try:
        user_name = session.get('user_name', 'Desconocido')
        print(f"👋 Cerrando sesión para usuario: {user_name}")
        
        # Limpiar toda la sesión
        session.clear()
        
        return jsonify({
            'success': True, 
            'message': 'Sesión cerrada correctamente'
        })
        
    except Exception as e:
        print(f"❌ Error cerrando sesión: {str(e)}")
        return jsonify({
            'success': False, 
            'error': str(e)
        }), 500

@app.route('/logout.py', methods=['POST', 'GET'])
def logout_legacy():
    """Cierra la sesión del usuario (ruta legacy para compatibilidad)"""
    
    print(f"👋 Cerrando sesión para usuario: {session.get('user_name', 'Desconocido')}")
    
    # Limpiar sesión
    session.clear()
    
    # Devolver respuesta JSON
    return jsonify({
        'success': True,
        'message': 'Sesión cerrada correctamente'
    })

# ================================================================
# VERIFICACIÓN DE SESIÓN
# ================================================================

@app.route('/check_session', methods=['GET'])
def check_session():
    """Verifica si hay una sesión activa"""
    try:
        if 'user_id' in session:
            return jsonify({
                'authenticated': True,
                'user_id': session['user_id'],
                'user_role': session.get('user_role'),
                'user_name': session.get('user_name')
            })
        else:
            return jsonify({
                'authenticated': False
            })
    except Exception as e:
        return jsonify({
            'authenticated': False,
            'error': str(e)
        }), 500

@app.route('/validate_session', methods=['GET'])
def validate_session():
    """Valida que la sesión sea válida y el usuario exista"""
    try:
        if 'user_id' not in session:
            return jsonify({
                'valid': False,
                'message': 'No hay sesión activa'
            }), 401
        
        # Verificar que el usuario aún existe en la base de datos
        user = execute_query(
            "SELECT ID_Usuario, Nombre, Apellido, Rol, Estado FROM Usuario WHERE ID_Usuario = %s",
            (session['user_id'],),
            fetch_one=True
        )
        
        if not user:
            # Usuario no existe, limpiar sesión
            session.clear()
            return jsonify({
                'valid': False,
                'message': 'Usuario no encontrado'
            }), 401
        
        if user['Estado'] != 'Activo':
            # Usuario inactivo, limpiar sesión
            session.clear()
            return jsonify({
                'valid': False,
                'message': 'Usuario inactivo'
            }), 401
        
        return jsonify({
            'valid': True,
            'user': {
                'id': user['ID_Usuario'],
                'nombre': user['Nombre'],
                'apellido': user['Apellido'],
                'rol': user['Rol']
            }
        })
        
    except Exception as e:
        print(f"❌ Error validando sesión: {str(e)}")
        return jsonify({
            'valid': False,
            'error': str(e)
        }), 500

# ================================================================
# RUTAS ADICIONALES PARA REDIRECCIONES
# ================================================================

@app.route('/')
def index():
    """Ruta principal - redirige al login de trabajador"""
    return redirect('/vista/login-trabajador.html')

@app.route('/registro-trabajador')
def registro_trabajador():
    """Redirige al registro de trabajador"""
    return redirect('/vista/registro-trabajador.html')

@app.route('/registro-agricultor')
def registro_agricultor():
    """Redirige al registro de agricultor"""
    return redirect('/vista/registro-agricultor.html')

@app.route('/login-trabajador')
def login_trabajador():
    """Redirige al login de trabajador"""
    return redirect('/vista/login-trabajador.html')

@app.route('/login-agricultor')
def login_agricultor():
    """Redirige al login de agricultor"""
    return redirect('/vista/login-trabajador.html')

# ================================================================
# RUTA DE PRUEBA MEJORADA
# ================================================================

@app.route('/test', methods=['GET'])
def test():
    """Ruta de prueba para verificar que el servidor funciona"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        return jsonify({
            'message': 'Servidor Flask funcionando correctamente',
            'status': 'OK',
            'base_directory': base_dir,
            'session_active': 'user_id' in session,
            'session_user': session.get('user_name', 'No logueado'),
            'rutas_disponibles': [
                '/test',
                '/check_files',
                '/check_session',
                '/validate_session',
                '/get_user_session',
                '/get_user_data.py',
                '/registro.py',
                '/login.py',
                '/logout',
                '/logout.py',
                '/dashboard-agricultor',
                '/dashboard-trabajador', 
                '/dashboard-admin',
                '/vista/<archivo>',
                '/css/<archivo>',
                '/assent/css/<archivo>',
                '/img/<archivo>',
                '/assent/img/<archivo>',
                '/js/<archivo>',
                '/assent/js/<archivo>',
                '/styles.css',
                '/script.js'
            ],
            'dashboard_files': {
                'html': '/vista/dashboard-agricultor.html',
                'css': '/styles.css',
                'js': '/script.js'
            }
        })
    except Exception as e:
        return jsonify({
            'message': 'Error en el servidor',
            'status': 'ERROR',
            'error': str(e)
        }), 500

# ================================================================
# MANEJO DE ERRORES MEJORADO
# ================================================================

@app.errorhandler(404)
def not_found(error):
    """Maneja errores 404 con más información"""
    requested_url = request.url
    print(f"❌ Error 404: Página no encontrada - {requested_url}")
    
    # Si es una solicitud de archivo HTML, intentar sugerir alternativas
    if '.html' in requested_url:
        print(f"🔍 Intentando encontrar alternativas para: {requested_url}")
        
        # Obtener información de archivos disponibles
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            vista_path = os.path.join(base_dir, '..', 'vista')
            
            if os.path.exists(vista_path):
                available_files = os.listdir(vista_path)
                html_files = [f for f in available_files if f.endswith('.html')]
                
                return jsonify({
                    'error': True,
                    'message': 'Página no encontrada',
                    'status': 404,
                    'requested_url': requested_url,
                    'suggestion': 'Verifica que el archivo exists en la carpeta vista/',
                    'available_html_files': html_files,
                    'vista_path': vista_path
                }), 404
        except:
            pass
    
    return jsonify({
        'error': True,
        'message': 'Página no encontrada',
        'status': 404,
        'requested_url': requested_url
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Maneja errores 500"""
    print(f"❌ Error interno del servidor: {error}")
    return jsonify({
        'error': True,
        'message': 'Error interno del servidor',
        'status': 500,
        'details': str(error)
    }), 500

# ================================================================
# MIDDLEWARE PARA LOGS DE SESIÓN
# ================================================================

@app.before_request
def log_request_info():
    """Log información de cada request (solo para debugging)"""
    # Solo loguear requests importantes, no archivos estáticos
    if request.endpoint and not any(static in request.path for static in ['/css/', '/js/', '/img/', '/assent/']):
        print(f"🔍 Request: {request.method} {request.path} | Session: {'✅' if 'user_id' in session else '❌'} | User: {session.get('user_name', 'Anónimo')}")

# ================================================================
# FUNCIONES ADICIONALES DE UTILIDAD
# ================================================================

def require_login(f):
    """Decorador para rutas que requieren autenticación"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': True, 'message': 'Autenticación requerida'}), 401
            else:
                return redirect('/vista/login-trabajador.html')
        return f(*args, **kwargs)
    return decorated_function

def require_role(required_role):
    """Decorador para rutas que requieren un rol específico"""
    from functools import wraps
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                if request.is_json:
                    return jsonify({'error': True, 'message': 'Autenticación requerida'}), 401
                else:
                    return redirect('/vista/login-trabajador.html')
            
            if session.get('user_role') != required_role:
                if request.is_json:
                    return jsonify({'error': True, 'message': 'Permisos insuficientes'}), 403
                else:
                    # Redireccionar a la página apropiada según el rol actual
                    current_role = session.get('user_role', 'Trabajador')
                    if current_role == 'Agricultor':
                        return redirect('/vista/dashboard-agricultor.html')
                    elif current_role == 'Administrador':
                        return redirect('/vista/dashboard-admin.html')
                    else:
                        return redirect('/vista/index-trabajador.html')
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ================================================================
# RUTAS PROTEGIDAS DE EJEMPLO (usar los decoradores)
# ================================================================

@app.route('/api/user/profile', methods=['GET'])
@require_login
def get_user_profile():
    """Obtiene el perfil completo del usuario"""
    try:
        user_id = session['user_id']
        
        # Obtener datos completos del usuario desde la base de datos
        user = execute_query(
            """SELECT ID_Usuario, Nombre, Apellido, Correo, Telefono, Rol, 
                      Estado, Fecha_Registro 
               FROM Usuario WHERE ID_Usuario = %s""",
            (user_id,),
            fetch_one=True
        )
        
        if not user:
            return jsonify({'error': True, 'message': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'error': False,
            'user': {
                'id': user['ID_Usuario'],
                'nombre': user['Nombre'],
                'apellido': user['Apellido'],
                'correo': user['Correo'],
                'telefono': user.get('Telefono', ''),
                'rol': user['Rol'],
                'estado': user['Estado'],
                'fecha_registro': user['Fecha_Registro'].isoformat() if user['Fecha_Registro'] else None
            }
        })
        
    except Exception as e:
        print(f"❌ Error obteniendo perfil: {str(e)}")
        return jsonify({'error': True, 'message': str(e)}), 500

@app.route('/api/admin/users', methods=['GET'])
@require_role('Administrador')
def get_all_users():
    """Obtiene todos los usuarios (solo administradores)"""
    try:
        users = execute_query(
            """SELECT ID_Usuario, Nombre, Apellido, Correo, Telefono, Rol, 
                      Estado, Fecha_Registro 
               FROM Usuario ORDER BY Fecha_Registro DESC"""
        )
        
        return jsonify({
            'error': False,
            'users': users
        })
        
    except Exception as e:
        print(f"❌ Error obteniendo usuarios: {str(e)}")
        return jsonify({'error': True, 'message': str(e)}), 500

# ================================================================
# RUTAS ADICIONALES PARA PERFIL - AGREGAR AL FINAL DE TU APP.PY
# ================================================================

# Configuración para subida de archivos (agregar después de app.secret_key)
# Configuración para subida de archivos
base_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(base_dir, '..', 'static', 'uploads')
PROFILE_PHOTOS_FOLDER = os.path.join(UPLOAD_FOLDER, 'profile_photos')
DOCUMENTS_FOLDER = os.path.join(UPLOAD_FOLDER, 'documents')
ALLOWED_EXTENSIONS_IMAGES = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS_DOCS = {'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Crear la estructura completa de carpetas
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, '..', 'static')
    uploads_dir = os.path.join(static_dir, 'uploads')
    profile_dir = os.path.join(uploads_dir, 'profile_photos')
    docs_dir = os.path.join(uploads_dir, 'documents')
    
    # Crear todas las carpetas
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(uploads_dir, exist_ok=True)
    os.makedirs(profile_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)
    
    print(f"✅ Estructura de carpetas creada:")
    print(f"   📁 {static_dir}")
    print(f"   📁 {uploads_dir}")
    print(f"   📸 {profile_dir}")
    print(f"   📄 {docs_dir}")
    
except Exception as e:
    print(f"❌ Error creando estructura: {e}")

# ⭐ CREAR DIRECTORIOS SI NO EXISTEN - AGREGAR ESTAS LÍNEAS ⭐
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROFILE_PHOTOS_FOLDER, exist_ok=True)
os.makedirs(DOCUMENTS_FOLDER, exist_ok=True)

print(f"✅ Directorios de upload creados:")
print(f"   📁 {UPLOAD_FOLDER}")
print(f"   📸 {PROFILE_PHOTOS_FOLDER}")
print(f"   📄 {DOCUMENTS_FOLDER}")

# Función auxiliar para validar archivos
def allowed_file(filename, allowed_extensions=ALLOWED_EXTENSIONS_IMAGES):
    """Valida si un archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_unique_filename(filename):
    """Generar nombre de archivo único"""
    file_extension = filename.rsplit('.', 1)[1].lower()
    unique_name = str(uuid.uuid4()) + '.' + file_extension
    return unique_name

# ================================================================
# RUTAS PARA PERFIL DE TRABAJADOR
# ================================================================

@app.route('/perfil-trabajador')
@app.route('/perfil-trabajador.html')
def perfil_trabajador():
    """Mostrar página de perfil del trabajador"""
    if 'user_id' not in session:
        return redirect('/vista/login-trabajador.html')
    return redirect('/vista/perfil-trabajador.html')

@app.route('/static/<path:filename>')
def serve_static_file(filename):
    """Servir archivos estáticos incluyendo uploads"""
    try:
        # Crear directorio static si no existe
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')
        static_dir = os.path.abspath(static_dir)
        
        if not os.path.exists(static_dir):
            os.makedirs(static_dir, exist_ok=True)
        
        return send_from_directory(static_dir, filename)
    except Exception as e:
        print(f"Error sirviendo archivo estático: {str(e)}")
        return "Archivo no encontrado", 404


# ================================================================
# ACTUALIZAR LA FUNCIÓN get_user_session EXISTENTE
# ================================================================

@app.route('/get_user_session')
def get_user_session_updated():
    """Obtiene los datos de la sesión actual del usuario - VERSIÓN ACTUALIZADA"""
    try:
        if 'user_id' in session:
            user_id = session['user_id']
            
            # Obtener datos actualizados del usuario desde la base de datos
            user_data = execute_query(
                """SELECT ID_Usuario, Nombre, Apellido, Correo, Telefono, 
                          URL_Foto, Red_Social, Rol, Estado, Fecha_Registro
                   FROM Usuario WHERE ID_Usuario = %s""",
                (user_id,),
                fetch_one=True
            )
            
            if not user_data:
                return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
            
            # Actualizar datos de sesión con información fresca de la BD
            session['first_name'] = user_data['Nombre']
            session['last_name'] = user_data['Apellido']
            session['email'] = user_data['Correo']
            session['user_name'] = f"{user_data['Nombre']} {user_data['Apellido']}"
            session['telefono'] = user_data.get('Telefono', '')
            
            print(f"Obteniendo datos de sesión para usuario ID: {user_id}")
            
            return jsonify({
                'success': True,
                'user': {
                    'user_id': user_data['ID_Usuario'],
                    'full_name': f"{user_data['Nombre']} {user_data['Apellido']}",
                    'nombre': user_data['Nombre'],
                    'apellido': user_data['Apellido'],
                    'first_name': user_data['Nombre'],
                    'last_name': user_data['Apellido'],
                    'email': user_data['Correo'],
                    'telefono': user_data.get('Telefono', ''),
                    'url_foto': user_data.get('URL_Foto'),
                    'red_social': user_data.get('Red_Social', ''),
                    'rol': user_data['Rol'],
                    'role': user_data['Rol'],  # Alias para compatibilidad
                    'estado': user_data['Estado'],
                    'fecha_registro': user_data['Fecha_Registro'].isoformat() if user_data['Fecha_Registro'] else None,
                    'username': user_data['Correo']  # Para compatibilidad
                }
            })
        else:
            print("No hay sesión activa")
            return jsonify({'success': False, 'error': 'No hay sesión activa'}), 401
            
    except Exception as e:
        print(f"Error obteniendo sesión: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500



# ================================================================
# RUTAS PARA MANEJO DE FOTOS DE PERFIL
# ================================================================

@app.route('/api/upload-profile-photo', methods=['POST'])
@require_login
def upload_profile_photo():
    """Subir foto de perfil del usuario"""
    try:
        user_id = session['user_id']
        
        if 'profilePhoto' not in request.files:
            return jsonify({'success': False, 'message': 'No se seleccionó ningún archivo'}), 400
        
        file = request.files['profilePhoto']
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No se seleccionó ningún archivo'}), 400
        
        # Usar la nueva función allowed_file
        if not allowed_file(file.filename, ALLOWED_EXTENSIONS_IMAGES):
            return jsonify({
                'success': False, 
                'message': 'Formato de archivo no válido. Use PNG, JPG, JPEG o GIF'
            }), 400
        
        # Validar tamaño
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'success': False, 
                'message': 'El archivo es muy grande. Tamaño máximo: 5MB'
            }), 400
        
        # Generar nombre único para el archivo
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"profile_{user_id}_{uuid.uuid4().hex[:8]}.{file_extension}"
        
        # Guardar en la carpeta correcta
        file_path = os.path.join(PROFILE_PHOTOS_FOLDER, unique_filename)
        file.save(file_path)
        
        # URL relativa para la base de datos
        photo_url = f"/static/uploads/profile_photos/{unique_filename}"
        
        # Actualizar URL_Foto en la tabla Usuario (tu tabla existente)
        execute_query(
            "UPDATE Usuario SET URL_Foto = %s WHERE ID_Usuario = %s",
            (photo_url, user_id)
        )
        
        # Registrar en tabla Anexo para historial (tu tabla existente)
        execute_query(
            """INSERT INTO Anexo (ID_Usuario, Tipo_Archivo, URL_Archivo, Descripcion) 
               VALUES (%s, 'Imagen', %s, 'Foto de perfil')""",
            (user_id, photo_url)
        )
        
        print(f"Foto de perfil actualizada para usuario {user_id}: {photo_url}")
        
        return jsonify({
            'success': True,
            'message': 'Foto de perfil actualizada correctamente',
            'photoUrl': photo_url
        })
        
    except Exception as e:
        print(f"Error subiendo foto de perfil: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ================================================================
# Función para actualizar perfil usando tu tabla Usuario
# ================================================================

@app.route('/api/update-profile', methods=['POST'])
@require_login
def update_profile():
    """Actualizar perfil usando tabla Usuario existente"""
    try:
        user_id = session['user_id']
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No se recibieron datos'}), 400
        
        # Obtener datos del formulario
        nombre = data.get('nombre', '').strip()
        apellido = data.get('apellido', '').strip() 
        telefono = data.get('telefono', '').strip()
        red_social = data.get('red_social', '').strip()
        
        # Validaciones básicas
        if not nombre:
            return jsonify({'success': False, 'message': 'El nombre es requerido'}), 400
        
        # Actualizar en tu tabla Usuario existente
        execute_query(
            """UPDATE Usuario SET 
               Nombre = %s, Apellido = %s, Telefono = %s, Red_Social = %s
               WHERE ID_Usuario = %s""",
            (nombre, apellido, telefono, red_social, user_id)
        )
        
        # Actualizar datos en la sesión
        session['first_name'] = nombre
        session['last_name'] = apellido
        session['user_name'] = f"{nombre} {apellido}"
        session['telefono'] = telefono
        
        return jsonify({
            'success': True,
            'message': 'Perfil actualizado correctamente'
        })
        
    except Exception as e:
        print(f"Error actualizando perfil: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ================================================================
# RUTAS PARA CONFIGURACIÓN DEL TRABAJADOR
# ================================================================

@app.route('/static/uploads/<path:filename>')
def serve_uploaded_file(filename):
    """Servir archivos subidos desde la carpeta de uploads"""
    try:
        # Obtener la ruta absoluta de la carpeta de uploads
        base_dir = os.path.dirname(os.path.abspath(__file__))
        uploads_path = os.path.join(base_dir, '..', 'static', 'uploads')
        uploads_path = os.path.abspath(uploads_path)
        
        # Verificar que el archivo existe
        file_path = os.path.join(uploads_path, filename)
        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {file_path}")
            return "Archivo no encontrado", 404
        
        print(f"✅ Sirviendo archivo: {file_path}")
        return send_from_directory(uploads_path, filename)
        
    except Exception as e:
        print(f"❌ Error sirviendo archivo: {str(e)}")
        return f"Error sirviendo archivo: {str(e)}", 500

# ================================================================
# la función para subir documentos usando tu tabla Anexo
# ================================================================

@app.route('/api/upload-document', methods=['POST'])
@require_login
def upload_document():
    """Subir documento usando tabla Anexo existente"""
    try:
        user_id = session['user_id']
        
        if 'document' not in request.files:
            return jsonify({'success': False, 'message': 'No se seleccionó ningún archivo'}), 400
        
        file = request.files['document']
        doc_type = request.form.get('docType', 'Documento')
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No se seleccionó ningún archivo'}), 400
        
        # Verificar tipo de archivo
        if not allowed_file(file.filename, ALLOWED_EXTENSIONS_DOCS):
            return jsonify({'success': False, 'message': 'Formato de archivo no válido'}), 400
        
        # Verificar tamaño
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'success': False, 'message': 'Archivo muy grande. Máximo 5MB'}), 400
        
        # Generar nombre único
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"doc_{user_id}_{uuid.uuid4().hex[:8]}.{file_extension}"
        
        # Guardar archivo
        file_path = os.path.abspath(os.path.join(DOCUMENTS_FOLDER, unique_filename))
        file.save(file_path)
        
        # URL relativa
        doc_url = f"/static/uploads/documents/{unique_filename}"
        
        # Guardar en tabla Anexo (tu tabla existente)
        execute_query(
            """INSERT INTO Anexo (ID_Usuario, Tipo_Archivo, URL_Archivo, Descripcion) 
               VALUES (%s, 'Documento', %s, %s)""",
            (user_id, doc_url, f"{doc_type} - {file.filename}")
        )
        
        print(f"Documento subido: {doc_url}")
        
        return jsonify({
            'success': True,
            'message': 'Documento subido correctamente',
            'documentUrl': doc_url,
            'fileName': file.filename
        })
        
    except Exception as e:
        print(f"Error subiendo documento: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ================================================================
#  función para obtener documentos subidos
# ================================================================

@app.route('/api/get-documents', methods=['GET'])
@require_login
def get_documents():
    """Obtener documentos del usuario desde tabla Anexo"""
    try:
        user_id = session['user_id']
        
        documents = execute_query(
            """SELECT ID_Anexo, Tipo_Archivo, URL_Archivo, Descripcion, Fecha_Subida
               FROM Anexo 
               WHERE ID_Usuario = %s AND Tipo_Archivo = 'Documento'
               ORDER BY Fecha_Subida DESC""",
            (user_id,)
        )
        
        return jsonify({
            'success': True,
            'documents': documents or []
        })
        
    except Exception as e:
        print(f"Error obteniendo documentos: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ================================================================
# RUTA PARA OBTENER PERFIL COMPLETO DE OTRO USUARIO
# ================================================================

@app.route('/api/get-user-profile/<int:user_id>')
def get_user_profile_complete(user_id):
    """Obtener perfil completo de un usuario (para visualización)"""
    try:
        # Verificar que el usuario solicitado existe y está activo
        user = execute_query(
            """SELECT ID_Usuario, Nombre, Apellido, Correo, Telefono, URL_Foto, 
                      Red_Social, Rol, Estado, Fecha_Registro
               FROM Usuario 
               WHERE ID_Usuario = %s AND Estado = 'Activo'""",
            (user_id,),
            fetch_one=True
        )
        
        if not user:
            return jsonify({
                'success': False, 
                'message': 'Usuario no encontrado o inactivo'
            }), 404
        
        # Información adicional según el rol
        additional_info = {}
        
        if user['Rol'] == 'Trabajador':
            # Obtener habilidades
            habilidades = execute_query(
                "SELECT Nombre, Clasificacion FROM Habilidad WHERE ID_Trabajador = %s",
                (user_id,)
            ) or []
            
            # Obtener experiencias
            experiencias = execute_query(
                """SELECT Fecha_Inicio, Fecha_Fin, Ubicacion, Observacion 
                   FROM Experiencia WHERE ID_Trabajador = %s 
                   ORDER BY Fecha_Inicio DESC""",
                (user_id,)
            ) or []
            
            additional_info = {
                'habilidades': habilidades,
                'experiencias': experiencias
            }
            
        elif user['Rol'] == 'Agricultor':
            # Obtener predios
            predios = execute_query(
                """SELECT Nombre_Finca, Ubicacion_Latitud, Ubicacion_Longitud, 
                          Descripcion FROM Predio WHERE ID_Usuario = %s""",
                (user_id,)
            ) or []
            
            # Obtener ofertas activas
            ofertas = execute_query(
                """SELECT Titulo, Descripcion, Pago_Ofrecido, Fecha_Publicacion 
                   FROM Oferta_Trabajo 
                   WHERE ID_Agricultor = %s AND Estado = 'Abierta' 
                   ORDER BY Fecha_Publicacion DESC LIMIT 5""",
                (user_id,)
            ) or []
            
            additional_info = {
                'predios': predios,
                'ofertas_activas': ofertas
            }
        
        # Calcular calificación promedio
        calificacion_info = execute_query(
            """SELECT AVG(CAST(Puntuacion AS UNSIGNED)) as promedio, 
                      COUNT(*) as total_calificaciones
               FROM Calificacion 
               WHERE ID_Usuario_Receptor = %s""",
            (user_id,),
            fetch_one=True
        )
        
        calificacion_promedio = 0
        total_calificaciones = 0
        
        if calificacion_info:
            calificacion_promedio = float(calificacion_info['promedio']) if calificacion_info['promedio'] else 0
            total_calificaciones = calificacion_info['total_calificaciones'] or 0
        
        return jsonify({
            'success': True,
            'user': {
                'id': user['ID_Usuario'],
                'nombre_completo': f"{user['Nombre']} {user['Apellido']}",
                'nombre': user['Nombre'],
                'apellido': user['Apellido'],
                'correo': user['Correo'],
                'telefono': user.get('Telefono', ''),
                'rol': user['Rol'],
                'foto_url': user.get('URL_Foto'),
                'red_social': user.get('Red_Social', ''),
                'fecha_registro': user['Fecha_Registro'].isoformat() if user['Fecha_Registro'] else None,
                'calificacion_promedio': calificacion_promedio,
                'total_calificaciones': total_calificaciones,
                **additional_info
            }
        })
        
    except Exception as e:
        print(f"Error obteniendo perfil de usuario: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ================================================================
# RUTA DE PRUEBA PARA CREAR SESIÓN (TEMPORAL - PARA TESTING)
# ================================================================

@app.route('/test-session')
def test_session():
    """Crear sesión de prueba - ELIMINAR EN PRODUCCIÓN"""
    # Buscar el primer usuario activo en la base de datos
    user = execute_query(
        "SELECT * FROM Usuario WHERE Estado = 'Activo' LIMIT 1",
        fetch_one=True
    )
    
    if user:
        session['user_id'] = user['ID_Usuario']
        session['username'] = user['Correo']
        session['first_name'] = user['Nombre']
        session['last_name'] = user['Apellido']
        session['email'] = user['Correo']
        session['user_role'] = user['Rol']
        session['user_name'] = f"{user['Nombre']} {user['Apellido']}"
        session['telefono'] = user.get('Telefono', '')
        
        return f"""
        <h2>Sesión de prueba creada</h2>
        <p><strong>Usuario:</strong> {user['Nombre']} {user['Apellido']}</p>
        <p><strong>Email:</strong> {user['Correo']}</p>
        <p><strong>Rol:</strong> {user['Rol']}</p>
        <p><strong>ID:</strong> {user['ID_Usuario']}</p>
        <br>
        <a href="/vista/perfil-trabajador.html" style="background: #28a745; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;">
            Ir al Perfil
        </a>
        """
    else:
        return "No hay usuarios en la base de datos. Registra un usuario primero."

# ================================================================
# RUTAS PARA CONFIGURACIÓN DEL TRABAJADOR - SIN TABLA ADICIONAL
# ================================================================

@app.route('/api/change-password', methods=['POST'])
@require_login
def change_password():
   """Cambiar contraseña del usuario"""
   try:
       data = request.get_json()
       current_password = data.get('currentPassword')
       new_password = data.get('newPassword')
       
       if not current_password or not new_password:
           return jsonify({'success': False, 'message': 'Faltan datos requeridos'}), 400
       
       # Obtener usuario actual
       user = execute_query(
           "SELECT Contrasena FROM Usuario WHERE ID_Usuario = %s",
           (session['user_id'],),
           fetch_one=True
       )
       
       if not user:
           return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
       
       # Verificar contraseña actual
       if not verify_password(current_password, user['Contrasena']):
           return jsonify({'success': False, 'message': 'Contraseña actual incorrecta'}), 400
       
       # Hashear nueva contraseña
       hashed_new_password = hash_password(new_password)
       
       # Actualizar en base de datos
       execute_query(
           "UPDATE Usuario SET Contrasena = %s WHERE ID_Usuario = %s",
           (hashed_new_password, session['user_id'])
       )
       
       print(f"Contraseña actualizada para usuario ID: {session['user_id']}")
       
       return jsonify({
           'success': True,
           'message': 'Contraseña actualizada correctamente'
       })
       
   except Exception as e:
       print(f"Error cambiando contraseña: {str(e)}")
       return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/update-notification-settings', methods=['POST'])
@require_login
def update_notification_settings():
   """Actualizar configuración de notificaciones usando tabla Usuario"""
   try:
       import json
       
       data = request.get_json()
       user_id = session['user_id']
       
       # Obtener configuraciones actuales
       current_user = execute_query(
           "SELECT Configuraciones FROM Usuario WHERE ID_Usuario = %s",
           (user_id,),
           fetch_one=True
       )
       
       # Parsear configuraciones existentes o crear nuevas
       if current_user and current_user.get('Configuraciones'):
           try:
               configuraciones = json.loads(current_user['Configuraciones'])
           except:
               configuraciones = {}
       else:
           configuraciones = {}
       
       # Actualizar configuración de notificaciones
       configuraciones['notificaciones'] = {
           'emailNotifications': data.get('emailNotifications', True),
           'emailUpdates': data.get('emailUpdates', True),
           'whatsappNotifications': data.get('whatsappNotifications', False),
           'whatsappUrgent': data.get('whatsappUrgent', False)
       }
       
       # Actualizar teléfono y configuraciones
       whatsapp_number = data.get('whatsappNumber', '').strip()
       
       execute_query(
           """UPDATE Usuario 
              SET Telefono = %s, Configuraciones = %s
              WHERE ID_Usuario = %s""",
           (whatsapp_number if whatsapp_number else None, 
            json.dumps(configuraciones), 
            user_id)
       )
       
       print(f"Configuración de notificaciones actualizada para usuario ID: {user_id}")
       
       return jsonify({
           'success': True,
           'message': 'Configuración de notificaciones guardada'
       })
       
   except Exception as e:
       print(f"Error actualizando notificaciones: {str(e)}")
       return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/update-preferences', methods=['POST'])
@require_login
def update_preferences():
   """Actualizar preferencias del usuario usando tabla Usuario"""
   try:
       import json
       
       data = request.get_json()
       user_id = session['user_id']
       
       # Obtener configuraciones actuales
       current_user = execute_query(
           "SELECT Configuraciones FROM Usuario WHERE ID_Usuario = %s",
           (user_id,),
           fetch_one=True
       )
       
       # Parsear configuraciones existentes o crear nuevas
       if current_user and current_user.get('Configuraciones'):
           try:
               configuraciones = json.loads(current_user['Configuraciones'])
           except:
               configuraciones = {}
       else:
           configuraciones = {}
       
       # Actualizar preferencias
       configuraciones['preferencias'] = {
           'language': data.get('language', 'es'),
           'theme': data.get('theme', 'light'),
           'timezone': data.get('timezone', 'America/Bogota')
       }
       
       # Guardar en base de datos
       execute_query(
           """UPDATE Usuario 
              SET Configuraciones = %s
              WHERE ID_Usuario = %s""",
           (json.dumps(configuraciones), user_id)
       )
       
       print(f"Preferencias actualizadas para usuario ID: {user_id}")
       
       return jsonify({
           'success': True,
           'message': 'Preferencias guardadas correctamente'
       })
       
   except Exception as e:
       print(f"Error actualizando preferencias: {str(e)}")
       return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/delete-account', methods=['DELETE'])
@require_login
def delete_account():
   """Eliminar cuenta del usuario"""
   try:
       data = request.get_json()
       password = data.get('password')
       user_id = session['user_id']
       
       if not password:
           return jsonify({'success': False, 'message': 'Contraseña requerida'}), 400
       
       # Verificar contraseña
       user = execute_query(
           "SELECT Contrasena FROM Usuario WHERE ID_Usuario = %s",
           (user_id,),
           fetch_one=True
       )
       
       if not user or not verify_password(password, user['Contrasena']):
           return jsonify({'success': False, 'message': 'Contraseña incorrecta'}), 400
       
       # Eliminar registros relacionados (en orden de dependencias)
       tables_to_clean = [
           ('Calificacion', ['ID_Usuario_Emisor', 'ID_Usuario_Receptor']),
           ('Mensaje', ['ID_Emisor', 'ID_Receptor']),
           ('Acuerdo_Laboral', ['ID_Trabajador']),
           ('Postulacion', ['ID_Trabajador']),
           ('Anexo', ['ID_Usuario']),
           ('Habilidad', ['ID_Trabajador']),
           ('Experiencia', ['ID_Trabajador']),
           ('Oferta_Trabajo', ['ID_Agricultor']),
           ('Predio', ['ID_Usuario'])
       ]
       
       for table_name, columns in tables_to_clean:
           try:
               if len(columns) == 1:
                   # Una sola columna de referencia
                   execute_query(f"DELETE FROM {table_name} WHERE {columns[0]} = %s", (user_id,))
               else:
                   # Múltiples columnas de referencia
                   conditions = ' OR '.join([f"{col} = %s" for col in columns])
                   params = [user_id] * len(columns)
                   execute_query(f"DELETE FROM {table_name} WHERE {conditions}", params)
                   
           except Exception as table_error:
               print(f"Error eliminando de {table_name}: {str(table_error)}")
               # Continuar con las otras tablas aunque falle una
               continue
       
       # Finalmente, eliminar el usuario
       execute_query("DELETE FROM Usuario WHERE ID_Usuario = %s", (user_id,))
       
       # Limpiar sesión
       session.clear()
       
       print(f"Cuenta eliminada completamente para usuario ID: {user_id}")
       
       return jsonify({
           'success': True,
           'message': 'Cuenta eliminada correctamente'
       })
       
   except Exception as e:
       print(f"Error eliminando cuenta: {str(e)}")
       return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/get-user-settings', methods=['GET'])
@require_login
def get_user_settings():
   """Obtener configuraciones del usuario desde tabla Usuario"""
   try:
       import json
       
       user_id = session['user_id']
       
       # Obtener configuraciones del usuario
       user = execute_query(
           "SELECT Configuraciones, Telefono FROM Usuario WHERE ID_Usuario = %s",
           (user_id,),
           fetch_one=True
       )
       
       if user and user.get('Configuraciones'):
           try:
               configuraciones = json.loads(user['Configuraciones'])
               
               return jsonify({
                   'success': True,
                   'settings': {
                       'notifications': configuraciones.get('notificaciones', {
                           'emailNotifications': True,
                           'emailUpdates': True,
                           'whatsappNotifications': False,
                           'whatsappUrgent': False
                       }),
                       'preferences': configuraciones.get('preferencias', {
                           'language': 'es',
                           'theme': 'light',
                           'timezone': 'America/Bogota'
                       }),
                       'whatsappNumber': user.get('Telefono', '')
                   }
               })
           except:
               # Si hay error parseando JSON, devolver configuración por defecto
               pass
       
       # Devolver configuración por defecto
       return jsonify({
           'success': True,
           'settings': {
               'notifications': {
                   'emailNotifications': True,
                   'emailUpdates': True,
                   'whatsappNotifications': False,
                   'whatsappUrgent': False
               },
               'preferences': {
                   'language': 'es',
                   'theme': 'light',
                   'timezone': 'America/Bogota'
               },
               'whatsappNumber': user.get('Telefono', '') if user else ''
           }
       })
           
   except Exception as e:
       print(f"Error obteniendo configuraciones: {str(e)}")
       return jsonify({'success': False, 'message': str(e)}), 500

# ================================================================
# SIMULACIÓN DE DATOS DE REDES SOCIALES
# ================================================================

# Usuarios simulados de Google (para demostración)
GOOGLE_USERS_DEMO = {
    "demo1": {
        "id": "google_123456",
        "email": "usuario.demo1@gmail.com",
        "given_name": "Juan",
        "family_name": "Pérez",
        "picture": "/static/uploads/profile_photos/default_google.jpg"
    },
    "demo2": {
        "id": "google_789012",
        "email": "maria.demo2@gmail.com",
        "given_name": "María",
        "family_name": "García",
        "picture": "/static/uploads/profile_photos/default_google2.jpg"
    }
}

# Usuarios simulados de Facebook (para demostración)
FACEBOOK_USERS_DEMO = {
    "demo1": {
        "id": "facebook_345678",
        "email": "usuario.demo1@outlook.com",
        "first_name": "Carlos",
        "last_name": "López",
        "picture": "/static/uploads/profile_photos/default_facebook.jpg"
    },
    "demo2": {
        "id": "facebook_901234",
        "email": "ana.demo2@hotmail.com",
        "first_name": "Ana",
        "last_name": "Martínez",
        "picture": "/static/uploads/profile_photos/default_facebook2.jpg"
    }
}

# ================================================================
# FUNCIONES AUXILIARES
# ================================================================

def generate_demo_password(email, provider):
    """Genera contraseña para usuarios demo"""
    combined = f"{email}_{provider}_{uuid.uuid4()}"
    return hashlib.sha256(combined.encode()).hexdigest()[:50]

def create_demo_user(user_data, provider, rol='Trabajador'):
    """Crea un usuario desde datos simulados"""
    try:
        # Hash de contraseña temporal
        from app import hash_password
        temp_password = hash_password(f"{user_data['email']}_social_{provider}")
        
        # Obtener nombres según el proveedor
        if provider == 'google':
            nombre = user_data.get('given_name', '')
            apellido = user_data.get('family_name', '')
        else:  # facebook
            nombre = user_data.get('first_name', '')
            apellido = user_data.get('last_name', '')
        
        # URL de foto por defecto
        foto_url = user_data.get('picture', f'/static/uploads/profile_photos/default_{provider}.jpg')
        
        # Insertar en base de datos
        user_id = execute_query(
            """INSERT INTO Usuario (Nombre, Apellido, Correo, Contrasena, URL_Foto, 
                                   Red_Social, Rol, Estado) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, 'Activo')""",
            (
                nombre,
                apellido,
                user_data['email'],
                temp_password,
                foto_url,
                f"{provider}:{user_data['id']}",
                rol
            )
        )
        
        print(f"Usuario demo creado desde {provider}: {user_data['email']}")
        return user_id
        
    except Exception as e:
        print(f"Error creando usuario demo: {str(e)}")
        return None

# ================================================================
# RUTAS PARA SIMULACIÓN DE GOOGLE
# ================================================================

@app.route('/auth/google/demo')
def google_demo():
    """Página de selección de usuario demo de Google"""
    try:
        rol = request.args.get('rol', 'Trabajador')
        session['oauth_rol'] = rol
        
        # Generar página HTML simple para seleccionar usuario demo
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Demo Google - AgroMatch</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0;
                }}
                .demo-container {{
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    max-width: 500px;
                    width: 90%;
                    text-align: center;
                }}
                .demo-header {{
                    margin-bottom: 30px;
                }}
                .demo-header h2 {{
                    color: #333;
                    margin-bottom: 10px;
                }}
                .demo-header p {{
                    color: #666;
                    margin-bottom: 5px;
                }}
                .role-badge {{
                    background: #4CAF50;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-size: 14px;
                    font-weight: 600;
                }}
                .user-list {{
                    margin: 30px 0;
                }}
                .demo-user {{
                    display: flex;
                    align-items: center;
                    padding: 15px;
                    margin: 10px 0;
                    background: #f8f9fa;
                    border-radius: 10px;
                    border: 2px solid transparent;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }}
                .demo-user:hover {{
                    border-color: #4285f4;
                    background: #e3f2fd;
                }}
                .user-avatar {{
                    width: 50px;
                    height: 50px;
                    background: #4285f4;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    font-size: 18px;
                    margin-right: 15px;
                }}
                .user-info {{
                    flex: 1;
                    text-align: left;
                }}
                .user-name {{
                    font-weight: 600;
                    color: #333;
                    margin-bottom: 3px;
                }}
                .user-email {{
                    color: #666;
                    font-size: 14px;
                }}
                .cancel-btn {{
                    background: #6c757d;
                    color: white;
                    border: none;
                    padding: 12px 25px;
                    border-radius: 8px;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    margin-top: 20px;
                    transition: background 0.3s ease;
                }}
                .cancel-btn:hover {{
                    background: #5a6268;
                }}
                .google-logo {{
                    color: #4285f4;
                    font-size: 24px;
                    margin-right: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="demo-container">
                <div class="demo-header">
                    <h2><i class="fab fa-google google-logo"></i>Simulación Google OAuth</h2>
                    <p>Registro como: <span class="role-badge">{rol}</span></p>
                    <p>Selecciona un usuario demo para continuar</p>
                </div>
                
                <div class="user-list">
        """
        
        # Agregar usuarios demo
        for demo_id, user_data in GOOGLE_USERS_DEMO.items():
            initials = f"{user_data['given_name'][0]}{user_data['family_name'][0]}"
            html_content += f"""
                    <div class="demo-user" onclick="selectGoogleUser('{demo_id}')">
                        <div class="user-avatar">{initials}</div>
                        <div class="user-info">
                            <div class="user-name">{user_data['given_name']} {user_data['family_name']}</div>
                            <div class="user-email">{user_data['email']}</div>
                        </div>
                    </div>
            """
        
        html_content += """
                </div>
                
                <a href="javascript:history.back()" class="cancel-btn">Cancelar</a>
            </div>
            
            <script>
                function selectGoogleUser(demoId) {
                    window.location.href = `/auth/google/demo/callback?demo_user=${demoId}`;
                }
            </script>
        </body>
        </html>
        """
        
        return html_content
        
    except Exception as e:
        print(f"Error en Google demo: {str(e)}")
        return redirect('/vista/registro-trabajador.html?message=Error en simulación de Google&type=error')

@app.route('/auth/google/demo/callback')
def google_demo_callback():
    """Procesar selección de usuario demo de Google"""
    try:
        demo_user_id = request.args.get('demo_user')
        rol = session.get('oauth_rol', 'Trabajador')
        
        if not demo_user_id or demo_user_id not in GOOGLE_USERS_DEMO:
            return redirect('/vista/registro-trabajador.html?message=Usuario demo no válido&type=error')
        
        user_data = GOOGLE_USERS_DEMO[demo_user_id]
        
        # Verificar si el usuario ya existe
        existing_user = execute_query(
            "SELECT * FROM Usuario WHERE Correo = %s",
            (user_data['email'],),
            fetch_one=True
        )
        
        if existing_user:
            user_id = existing_user['ID_Usuario']
            print(f"Usuario demo existente: {existing_user['Nombre']}")
        else:
            user_id = create_demo_user(user_data, 'google', rol)
            if not user_id:
                return redirect('/vista/registro-trabajador.html?message=Error creando usuario demo&type=error')
        
        # Obtener datos actualizados del usuario
        user = execute_query(
            "SELECT * FROM Usuario WHERE ID_Usuario = %s",
            (user_id,),
            fetch_one=True
        )
        
        # Crear sesión
        session['user_id'] = user['ID_Usuario']
        session['username'] = user['Correo']
        session['first_name'] = user['Nombre']
        session['last_name'] = user['Apellido']
        session['email'] = user['Correo']
        session['user_role'] = user['Rol']
        session['user_name'] = f"{user['Nombre']} {user['Apellido']}"
        session['telefono'] = user.get('Telefono', '')
        
        session.pop('oauth_rol', None)
        
        # Redireccionar según el rol
        if user['Rol'] == 'Agricultor':
            redirect_url = '/vista/index-agricultor.html'
        else:
            redirect_url = '/vista/index-trabajador.html'
        
        return redirect(redirect_url)
        
    except Exception as e:
        print(f"Error en Google demo callback: {str(e)}")
        return redirect('/vista/registro-trabajador.html?message=Error procesando usuario demo&type=error')

# ================================================================
# RUTAS PARA SIMULACIÓN DE FACEBOOK
# ================================================================

@app.route('/auth/facebook/demo')
def facebook_demo():
    """Página de selección de usuario demo de Facebook"""
    try:
        rol = request.args.get('rol', 'Trabajador')
        session['oauth_rol'] = rol
        
        # Similar al de Google pero con estilo de Facebook
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Demo Facebook - AgroMatch</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #4267B2 0%, #365899 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0;
                }}
                .demo-container {{
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    max-width: 500px;
                    width: 90%;
                    text-align: center;
                }}
                .demo-header {{
                    margin-bottom: 30px;
                }}
                .demo-header h2 {{
                    color: #333;
                    margin-bottom: 10px;
                }}
                .demo-header p {{
                    color: #666;
                    margin-bottom: 5px;
                }}
                .role-badge {{
                    background: #4CAF50;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-size: 14px;
                    font-weight: 600;
                }}
                .user-list {{
                    margin: 30px 0;
                }}
                .demo-user {{
                    display: flex;
                    align-items: center;
                    padding: 15px;
                    margin: 10px 0;
                    background: #f8f9fa;
                    border-radius: 10px;
                    border: 2px solid transparent;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }}
                .demo-user:hover {{
                    border-color: #4267B2;
                    background: #e3f2fd;
                }}
                .user-avatar {{
                    width: 50px;
                    height: 50px;
                    background: #4267B2;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    font-size: 18px;
                    margin-right: 15px;
                }}
                .user-info {{
                    flex: 1;
                    text-align: left;
                }}
                .user-name {{
                    font-weight: 600;
                    color: #333;
                    margin-bottom: 3px;
                }}
                .user-email {{
                    color: #666;
                    font-size: 14px;
                }}
                .cancel-btn {{
                    background: #6c757d;
                    color: white;
                    border: none;
                    padding: 12px 25px;
                    border-radius: 8px;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    margin-top: 20px;
                    transition: background 0.3s ease;
                }}
                .cancel-btn:hover {{
                    background: #5a6268;
                }}
                .facebook-logo {{
                    color: #4267B2;
                    font-size: 24px;
                    margin-right: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="demo-container">
                <div class="demo-header">
                    <h2><i class="fab fa-facebook facebook-logo"></i>Simulación Facebook OAuth</h2>
                    <p>Registro como: <span class="role-badge">{rol}</span></p>
                    <p>Selecciona un usuario demo para continuar</p>
                </div>
                
                <div class="user-list">
        """
        
        # Agregar usuarios demo
        for demo_id, user_data in FACEBOOK_USERS_DEMO.items():
            initials = f"{user_data['first_name'][0]}{user_data['last_name'][0]}"
            html_content += f"""
                    <div class="demo-user" onclick="selectFacebookUser('{demo_id}')">
                        <div class="user-avatar">{initials}</div>
                        <div class="user-info">
                            <div class="user-name">{user_data['first_name']} {user_data['last_name']}</div>
                            <div class="user-email">{user_data['email']}</div>
                        </div>
                    </div>
            """
        
        html_content += """
                </div>
                
                <a href="javascript:history.back()" class="cancel-btn">Cancelar</a>
            </div>
            
            <script>
                function selectFacebookUser(demoId) {
                    window.location.href = `/auth/facebook/demo/callback?demo_user=${demoId}`;
                }
            </script>
        </body>
        </html>
        """
        
        return html_content
        
    except Exception as e:
        print(f"Error en Facebook demo: {str(e)}")
        return redirect('/vista/registro-trabajador.html?message=Error en simulación de Facebook&type=error')

@app.route('/auth/facebook/demo/callback')
def facebook_demo_callback():
    """Procesar selección de usuario demo de Facebook"""
    try:
        demo_user_id = request.args.get('demo_user')
        rol = session.get('oauth_rol', 'Trabajador')
        
        if not demo_user_id or demo_user_id not in FACEBOOK_USERS_DEMO:
            return redirect('/vista/registro-trabajador.html?message=Usuario demo no válido&type=error')
        
        user_data = FACEBOOK_USERS_DEMO[demo_user_id]
        
        # Verificar si el usuario ya existe
        existing_user = execute_query(
            "SELECT * FROM Usuario WHERE Correo = %s",
            (user_data['email'],),
            fetch_one=True
        )
        
        if existing_user:
            user_id = existing_user['ID_Usuario']
            print(f"Usuario demo existente: {existing_user['Nombre']}")
        else:
            user_id = create_demo_user(user_data, 'facebook', rol)
            if not user_id:
                return redirect('/vista/registro-trabajador.html?message=Error creando usuario demo&type=error')
        
        # Obtener datos actualizados del usuario
        user = execute_query(
            "SELECT * FROM Usuario WHERE ID_Usuario = %s",
            (user_id,),
            fetch_one=True
        )
        
        # Crear sesión
        session['user_id'] = user['ID_Usuario']
        session['username'] = user['Correo']
        session['first_name'] = user['Nombre']
        session['last_name'] = user['Apellido']
        session['email'] = user['Correo']
        session['user_role'] = user['Rol']
        session['user_name'] = f"{user['Nombre']} {user['Apellido']}"
        session['telefono'] = user.get('Telefono', '')
        
        session.pop('oauth_rol', None)
        
        # Redireccionar según el rol
        if user['Rol'] == 'Agricultor':
            redirect_url = '/vista/index-agricultor.html'
        else:
            redirect_url = '/vista/index-trabajador.html'
        
        return redirect(redirect_url)
        
    except Exception as e:
        print(f"Error en Facebook demo callback: {str(e)}")
        return redirect('/vista/registro-trabajador.html?message=Error procesando usuario demo&type=error')

# ================================================================
# SIMULACIÓN DE AUTENTICACIÓN REAL
# ================================================================

def extract_info_from_email(email, provider):
    """Extrae información básica del email para crear el usuario"""
    try:
        # Extraer nombre del email (parte antes del @)
        username = email.split('@')[0]
        
        # Limpiar números y caracteres especiales
        clean_name = re.sub(r'[0-9._-]', ' ', username).strip()
        
        # Dividir en nombre y apellido
        name_parts = clean_name.split()
        
        if len(name_parts) >= 2:
            nombre = name_parts[0].capitalize()
            apellido = ' '.join(name_parts[1:]).title()
        elif len(name_parts) == 1:
            nombre = name_parts[0].capitalize()
            apellido = "Usuario"
        else:
            nombre = "Usuario"
            apellido = provider.capitalize()
        
        return {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'username': username,
            'provider': provider
        }
        
    except Exception as e:
        print(f"Error extrayendo info del email: {str(e)}")
        return None

def create_social_user_real(email, provider, rol='Trabajador'):
    """Crea un usuario real desde email de red social"""
    try:
        # Extraer información del email
        user_info = extract_info_from_email(email, provider)
        if not user_info:
            return None
        
        # Generar contraseña temporal hasheada
        from app import hash_password
        temp_password = hash_password(f"{email}_social_{provider}_{uuid.uuid4()}")
        
        # URL de foto por defecto según el proveedor
        if provider == 'google':
            foto_url = "/static/uploads/profile_photos/default_google_user.jpg"
        else:
            foto_url = "/static/uploads/profile_photos/default_facebook_user.jpg"
        
        # Insertar en base de datos
        user_id = execute_query(
            """INSERT INTO Usuario (Nombre, Apellido, Correo, Contrasena, URL_Foto, 
                                   Red_Social, Rol, Estado) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, 'Activo')""",
            (
                user_info['nombre'],
                user_info['apellido'], 
                email,
                temp_password,
                foto_url,
                f"{provider}:{user_info['username']}",
                rol
            )
        )
        
        print(f"Usuario real creado desde {provider}: {email}")
        return user_id
        
    except Exception as e:
        print(f"Error creando usuario social real: {str(e)}")
        return None

# ================================================================
# FORMULARIO PARA INGRESO CON GOOGLE
# ================================================================

@app.route('/auth/google/login')
def google_auth_form():
    """Formulario para ingresar email de Google - VERSIÓN CORREGIDA"""
    try:
        # Obtener rol si viene desde registro, si no, es login
        rol = request.args.get('rol', None)
        
        if rol:
            # Es registro con rol específico
            session['oauth_rol'] = rol
            action_text = f"Registro como {rol}"
            process_url = "/auth/google/process"
            info_text = "Se creará tu cuenta automáticamente"
        else:
            # Es login sin rol específico
            action_text = "Iniciar Sesión"
            process_url = "/auth/google/login-process"
            info_text = "Si no tienes cuenta, te ayudaremos a crearla"
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Google - AgroMatch</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #4285f4 0%, #34a853 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0;
                    padding: 20px;
                }}
                .auth-container {{
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                    max-width: 450px;
                    width: 100%;
                    text-align: center;
                }}
                .google-logo {{
                    font-size: 48px;
                    background: linear-gradient(45deg, #4285f4, #34a853, #fbbc05, #ea4335);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin-bottom: 20px;
                }}
                .auth-header h2 {{
                    color: #202124;
                    font-size: 24px;
                    margin-bottom: 10px;
                }}
                .auth-header p {{
                    color: #5f6368;
                    font-size: 16px;
                    margin-bottom: 30px;
                }}
                .form-group {{
                    margin-bottom: 20px;
                    text-align: left;
                }}
                .form-group label {{
                    display: block;
                    color: #3c4043;
                    font-size: 14px;
                    font-weight: 500;
                    margin-bottom: 8px;
                }}
                .form-group input {{
                    width: 100%;
                    padding: 16px;
                    border: 1px solid #dadce0;
                    border-radius: 8px;
                    font-size: 16px;
                    box-sizing: border-box;
                    transition: border-color 0.3s ease;
                }}
                .form-group input:focus {{
                    outline: none;
                    border-color: #1a73e8;
                    box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.2);
                }}
                .btn-continue {{
                    width: 100%;
                    background: #1a73e8;
                    color: white;
                    border: none;
                    padding: 16px;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: 500;
                    cursor: pointer;
                    margin-bottom: 16px;
                    transition: background 0.3s ease;
                }}
                .btn-continue:hover {{
                    background: #1557b0;
                }}
                .btn-continue:disabled {{
                    background: #dadce0;
                    cursor: not-allowed;
                }}
                .btn-cancel {{
                    width: 100%;
                    background: transparent;
                    color: #1a73e8;
                    border: 1px solid #dadce0;
                    padding: 16px;
                    border-radius: 8px;
                    text-decoration: none;
                    display: inline-block;
                    transition: background 0.3s ease;
                }}
                .btn-cancel:hover {{
                    background: #f8f9fa;
                }}
                .info-note {{
                    background: #e3f2fd;
                    border: 1px solid #1976d2;
                    border-radius: 8px;
                    padding: 12px;
                    margin: 20px 0;
                    font-size: 13px;
                    color: #0d47a1;
                }}
                .help-text {{
                    font-size: 12px;
                    color: #5f6368;
                    margin-top: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="auth-container">
                <div class="auth-header">
                    <div class="google-logo">
                        <i class="fab fa-google"></i>
                    </div>
                    <h2>Continuar con Google</h2>
                    <p>{action_text}</p>
                </div>

                <form id="googleForm" action="{process_url}" method="POST">
                    {"<input type='hidden' name='rol' value='" + str(rol) + "'>" if rol else ""}
                    
                    <div class="form-group">
                        <label for="google_email">Tu correo de Gmail</label>
                        <input 
                            type="email" 
                            id="google_email" 
                            name="google_email" 
                            placeholder="ejemplo@gmail.com"
                            required>
                        <div class="help-text">Ingresa tu dirección de Gmail real</div>
                    </div>

                    <div class="info-note">
                        <i class="fas fa-info-circle"></i> 
                        {info_text}
                    </div>

                    <button type="submit" class="btn-continue" id="continueBtn">
                        <i class="fas fa-arrow-right"></i> Continuar
                    </button>
                </form>

                <a href="javascript:history.back()" class="btn-cancel">
                    <i class="fas fa-arrow-left"></i> Volver
                </a>
            </div>

            <script>
                // Validación en tiempo real
                document.getElementById('google_email').addEventListener('input', function() {{
                    const email = this.value;
                    const btn = document.getElementById('continueBtn');
                    
                    if (email.includes('@gmail.com') || email.includes('@googlemail.com')) {{
                        this.style.borderColor = '#34a853';
                        btn.disabled = false;
                    }} else if (email.includes('@')) {{
                        this.style.borderColor = '#ea4335';
                        btn.disabled = true;
                    }} else {{
                        this.style.borderColor = '#dadce0';
                        btn.disabled = email.length === 0;
                    }}
                }});

                // Validación del formulario
                document.getElementById('googleForm').addEventListener('submit', function(e) {{
                    const email = document.getElementById('google_email').value;
                    
                    if (!email.includes('@gmail.com') && !email.includes('@googlemail.com')) {{
                        e.preventDefault();
                        alert('Por favor ingresa un correo válido de Gmail (@gmail.com)');
                        return false;
                    }}
                }});
            </script>
        </body>
        </html>
        """
        
        return html_content
        
    except Exception as e:
        print(f"Error en formulario de Google: {str(e)}")
        return redirect('/vista/login-trabajador.html?message=Error cargando Google&type=error')

@app.route('/auth/facebook/login')
def facebook_auth_form():
    """Formulario para ingresar email de Facebook - VERSIÓN CORREGIDA"""
    try:
        # Obtener rol si viene desde registro, si no, es login
        rol = request.args.get('rol', None)
        
        if rol:
            # Es registro con rol específico
            session['oauth_rol'] = rol
            action_text = f"Registro como {rol}"
            process_url = "/auth/facebook/process"
            info_text = "Se creará tu cuenta automáticamente"
        else:
            # Es login sin rol específico
            action_text = "Iniciar Sesión"
            process_url = "/auth/facebook/login-process"
            info_text = "Si no tienes cuenta, te ayudaremos a crearla"
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facebook - AgroMatch</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #4267B2 0%, #365899 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0;
                    padding: 20px;
                }}
                .auth-container {{
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                    max-width: 450px;
                    width: 100%;
                    text-align: center;
                }}
                .facebook-logo {{
                    font-size: 48px;
                    color: #4267B2;
                    margin-bottom: 20px;
                }}
                .auth-header h2 {{
                    color: #1c1e21;
                    font-size: 24px;
                    margin-bottom: 10px;
                }}
                .auth-header p {{
                    color: #606770;
                    font-size: 16px;
                    margin-bottom: 30px;
                }}
                .form-group {{
                    margin-bottom: 20px;
                    text-align: left;
                }}
                .form-group label {{
                    display: block;
                    color: #1c1e21;
                    font-size: 14px;
                    font-weight: 500;
                    margin-bottom: 8px;
                }}
                .form-group input {{
                    width: 100%;
                    padding: 16px;
                    border: 1px solid #dddfe2;
                    border-radius: 8px;
                    font-size: 16px;
                    box-sizing: border-box;
                    transition: border-color 0.3s ease;
                }}
                .form-group input:focus {{
                    outline: none;
                    border-color: #4267B2;
                    box-shadow: 0 0 0 2px rgba(66, 103, 178, 0.2);
                }}
                .btn-continue {{
                    width: 100%;
                    background: #4267B2;
                    color: white;
                    border: none;
                    padding: 16px;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    margin-bottom: 16px;
                    transition: background 0.3s ease;
                }}
                .btn-continue:hover {{
                    background: #365899;
                }}
                .btn-continue:disabled {{
                    background: #e4e6ea;
                    cursor: not-allowed;
                }}
                .btn-cancel {{
                    width: 100%;
                    background: transparent;
                    color: #4267B2;
                    border: 1px solid #dddfe2;
                    padding: 16px;
                    border-radius: 8px;
                    text-decoration: none;
                    display: inline-block;
                    transition: background 0.3s ease;
                }}
                .btn-cancel:hover {{
                    background: #f5f6f7;
                }}
                .info-note {{
                    background: #e7f3ff;
                    border: 1px solid #4267B2;
                    border-radius: 8px;
                    padding: 12px;
                    margin: 20px 0;
                    font-size: 13px;
                    color: #4267B2;
                }}
                .help-text {{
                    font-size: 12px;
                    color: #606770;
                    margin-top: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="auth-container">
                <div class="auth-header">
                    <div class="facebook-logo">
                        <i class="fab fa-facebook"></i>
                    </div>
                    <h2>Continuar con Facebook</h2>
                    <p>{action_text}</p>
                </div>

                <form id="facebookForm" action="{process_url}" method="POST">
                    {"<input type='hidden' name='rol' value='" + str(rol) + "'>" if rol else ""}
                    
                    <div class="form-group">
                        <label for="facebook_email">Tu correo asociado a Facebook</label>
                        <input 
                            type="email" 
                            id="facebook_email" 
                            name="facebook_email" 
                            placeholder="ejemplo@hotmail.com o @outlook.com"
                            required>
                        <div class="help-text">Hotmail, Outlook, Live o MSN</div>
                    </div>

                    <div class="info-note">
                        <i class="fas fa-info-circle"></i> 
                        {info_text}
                    </div>

                    <button type="submit" class="btn-continue" id="continueBtn">
                        <i class="fas fa-arrow-right"></i> Continuar
                    </button>
                </form>

                <a href="javascript:history.back()" class="btn-cancel">
                    <i class="fas fa-arrow-left"></i> Volver
                </a>
            </div>

            <script>
                // Validación en tiempo real
                document.getElementById('facebook_email').addEventListener('input', function() {{
                    const email = this.value;
                    const btn = document.getElementById('continueBtn');
                    const validDomains = ['@hotmail.com', '@outlook.com', '@live.com', '@msn.com'];
                    
                    if (validDomains.some(domain => email.includes(domain))) {{
                        this.style.borderColor = '#42b883';
                        btn.disabled = false;
                    }} else if (email.includes('@')) {{
                        this.style.borderColor = '#e74c3c';
                        btn.disabled = true;
                    }} else {{
                        this.style.borderColor = '#dddfe2';
                        btn.disabled = email.length === 0;
                    }}
                }});

                // Validación del formulario
                document.getElementById('facebookForm').addEventListener('submit', function(e) {{
                    const email = document.getElementById('facebook_email').value;
                    const validDomains = ['@hotmail.com', '@outlook.com', '@live.com', '@msn.com'];
                    
                    if (!validDomains.some(domain => email.includes(domain))) {{
                        e.preventDefault();
                        alert('Por favor ingresa un correo válido asociado a Facebook (Hotmail, Outlook, Live, MSN)');
                        return false;
                    }}
                }});
            </script>
        </body>
        </html>
        """
        
        return html_content
        
    except Exception as e:
        print(f"Error en formulario de Facebook: {str(e)}")
        return redirect('/vista/login-trabajador.html?message=Error cargando Facebook&type=error')

# ================================================================
# RUTAS DE PROCESAMIENTO (MANTENER LAS EXISTENTES)
# ================================================================

print("✅ Rutas de Google y Facebook corregidas y cargadas")


# ================================================================
# RUTAS PARA ELIMINACIÓN DE CUENTA CON REDES SOCIALES
# Agregar al final de tu app.py, antes de if __name__ == '__main__':
# ================================================================

@app.route('/auth/google/delete-account', methods=['POST'])
@require_login
def delete_account_with_google():
    """Eliminar cuenta verificando que fue creada con Google"""
    try:
        user_id = session['user_id']
        
        # Verificar que el usuario actual existe y tiene Google asociado
        user = execute_query(
            "SELECT * FROM Usuario WHERE ID_Usuario = %s",
            (user_id,),
            fetch_one=True
        )
        
        if not user:
            return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
        
        # Verificar que la cuenta fue creada con Google
        red_social = user.get('Red_Social', '')
        if not red_social or not red_social.startswith('google:'):
            return jsonify({
                'success': False, 
                'message': 'Esta cuenta no fue creada con Google'
            }), 400
        
        print(f"Eliminando cuenta con Google para usuario: {user['Nombre']} {user['Apellido']}")
        
        # Eliminar registros relacionados (en orden de dependencias)
        tables_to_clean = [
            ('Calificacion', ['ID_Usuario_Emisor', 'ID_Usuario_Receptor']),
            ('Mensaje', ['ID_Emisor', 'ID_Receptor']),
            ('Acuerdo_Laboral', ['ID_Trabajador']),
            ('Postulacion', ['ID_Trabajador']),
            ('Anexo', ['ID_Usuario']),
            ('Habilidad', ['ID_Trabajador']),
            ('Experiencia', ['ID_Trabajador']),
            ('Oferta_Trabajo', ['ID_Agricultor']),
            ('Predio', ['ID_Usuario'])
        ]
        
        for table_name, columns in tables_to_clean:
            try:
                if len(columns) == 1:
                    execute_query(f"DELETE FROM {table_name} WHERE {columns[0]} = %s", (user_id,))
                else:
                    conditions = ' OR '.join([f"{col} = %s" for col in columns])
                    params = [user_id] * len(columns)
                    execute_query(f"DELETE FROM {table_name} WHERE {conditions}", params)
                    
            except Exception as table_error:
                print(f"Error eliminando de {table_name}: {str(table_error)}")
                continue
        
        # Eliminar el usuario
        execute_query("DELETE FROM Usuario WHERE ID_Usuario = %s", (user_id,))
        
        # Limpiar sesión
        session.clear()
        
        print(f"Cuenta eliminada exitosamente con Google para usuario ID: {user_id}")
        
        return jsonify({
            'success': True,
            'message': 'Cuenta eliminada correctamente con Google'
        })
        
    except Exception as e:
        print(f"Error eliminando cuenta con Google: {str(e)}")
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

@app.route('/auth/facebook/delete-account', methods=['POST'])
@require_login
def delete_account_with_facebook():
    """Eliminar cuenta verificando que fue creada con Facebook"""
    try:
        user_id = session['user_id']
        
        # Verificar que el usuario actual existe y tiene Facebook asociado
        user = execute_query(
            "SELECT * FROM Usuario WHERE ID_Usuario = %s",
            (user_id,),
            fetch_one=True
        )
        
        if not user:
            return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
        
        # Verificar que la cuenta fue creada con Facebook
        red_social = user.get('Red_Social', '')
        if not red_social or not red_social.startswith('facebook:'):
            return jsonify({
                'success': False, 
                'message': 'Esta cuenta no fue creada con Facebook'
            }), 400
        
        print(f"Eliminando cuenta con Facebook para usuario: {user['Nombre']} {user['Apellido']}")
        
        # Eliminar registros relacionados (mismo proceso que Google)
        tables_to_clean = [
            ('Calificacion', ['ID_Usuario_Emisor', 'ID_Usuario_Receptor']),
            ('Mensaje', ['ID_Emisor', 'ID_Receptor']),
            ('Acuerdo_Laboral', ['ID_Trabajador']),
            ('Postulacion', ['ID_Trabajador']),
            ('Anexo', ['ID_Usuario']),
            ('Habilidad', ['ID_Trabajador']),
            ('Experiencia', ['ID_Trabajador']),
            ('Oferta_Trabajo', ['ID_Agricultor']),
            ('Predio', ['ID_Usuario'])
        ]
        
        for table_name, columns in tables_to_clean:
            try:
                if len(columns) == 1:
                    execute_query(f"DELETE FROM {table_name} WHERE {columns[0]} = %s", (user_id,))
                else:
                    conditions = ' OR '.join([f"{col} = %s" for col in columns])
                    params = [user_id] * len(columns)
                    execute_query(f"DELETE FROM {table_name} WHERE {conditions}", params)
                    
            except Exception as table_error:
                print(f"Error eliminando de {table_name}: {str(table_error)}")
                continue
        
        # Eliminar el usuario
        execute_query("DELETE FROM Usuario WHERE ID_Usuario = %s", (user_id,))
        
        # Limpiar sesión
        session.clear()
        
        print(f"Cuenta eliminada exitosamente con Facebook para usuario ID: {user_id}")
        
        return jsonify({
            'success': True,
            'message': 'Cuenta eliminada correctamente con Facebook'
        })
        
    except Exception as e:
        print(f"Error eliminando cuenta con Facebook: {str(e)}")
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

print("✅ Rutas de eliminación social cargadas correctamente")


# ENDPOINTS FALTANTES - Agregar al final de tu app.py antes de if __name__ == '__main__':

# 1. Endpoint para obtener documentos del usuario
@app.route('/api/user-documents', methods=['GET'])
@require_login
def get_user_documents():
    try:
        user_id = session['user_id']
        
        # Usar tu tabla Anexo existente
        documentos = execute_query(
            """SELECT ID_Anexo, Tipo_Archivo, URL_Archivo, Descripcion, Fecha_Subida
               FROM Anexo 
               WHERE ID_Usuario = %s 
               ORDER BY Fecha_Subida DESC""",
            (user_id,)
        )
        
        documents_list = []
        if documentos:
            for doc in documentos:
                # Extraer nombre del archivo de la URL
                archivo_nombre = os.path.basename(doc['URL_Archivo']) if doc['URL_Archivo'] else 'Sin nombre'
                
                documents_list.append({
                    'id': doc['ID_Anexo'],
                    'tipo_documento': doc['Tipo_Archivo'],
                    'nombre_archivo': archivo_nombre,
                    'url_documento': doc['URL_Archivo'],
                    'fecha_subida': doc['Fecha_Subida'].strftime('%Y-%m-%d %H:%M:%S') if doc['Fecha_Subida'] else None,
                    'estado': 'Subido',
                    'descripcion': doc['Descripcion']
                })
        
        return jsonify({
            'success': True,
            'documents': documents_list
        })
        
    except Exception as e:
        print(f"Error al obtener documentos: {e}")
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

# 2. Endpoint para obtener empleadores disponibles para calificar
@app.route('/api/user-employers', methods=['GET'])
@require_login
def get_user_employers():
    try:
        user_id = session['user_id']
        
        # Obtener agricultores con los que ha trabajado
        empleadores = execute_query("""
            SELECT DISTINCT u.ID_Usuario, u.Nombre, u.Apellido, u.Correo
            FROM Usuario u
            INNER JOIN Oferta_Trabajo ot ON u.ID_Usuario = ot.ID_Agricultor
            INNER JOIN Acuerdo_Laboral al ON ot.ID_Oferta = al.ID_Oferta
            WHERE al.ID_Trabajador = %s 
            AND al.Estado = 'Finalizado'
            AND u.Rol = 'Agricultor'
            ORDER BY u.Nombre, u.Apellido
        """, (user_id,))
        
        employers_list = []
        if empleadores:
            for emp in empleadores:
                employers_list.append({
                    'id': emp['ID_Usuario'],
                    'nombre': f"{emp['Nombre']} {emp['Apellido']}",
                    'empresa': emp['Nombre'],
                    'email': emp['Correo']
                })
        
        return jsonify({
            'success': True,
            'employers': employers_list
        })
        
    except Exception as e:
        print(f"Error al obtener empleadores: {e}")
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

# 3. Endpoint para enviar calificación
@app.route('/api/submit-rating', methods=['POST'])
@require_login
def submit_rating():
    try:
        data = request.get_json()
        user_id = session['user_id']
        employer_id = data.get('employerId')
        rating = data.get('rating')
        comment = data.get('comment')
        
        # Validar datos
        if not employer_id or not rating or not comment:
            return jsonify({'success': False, 'message': 'Todos los campos son requeridos'})
        
        if not (1 <= int(rating) <= 5):
            return jsonify({'success': False, 'message': 'La calificación debe ser entre 1 y 5'})
        
        # Buscar acuerdo laboral finalizado
        acuerdo = execute_query("""
            SELECT al.ID_Acuerdo
            FROM Acuerdo_Laboral al
            INNER JOIN Oferta_Trabajo ot ON al.ID_Oferta = ot.ID_Oferta
            WHERE al.ID_Trabajador = %s 
            AND ot.ID_Agricultor = %s
            AND al.Estado = 'Finalizado'
            ORDER BY al.ID_Acuerdo DESC
            LIMIT 1
        """, (user_id, employer_id), fetch_one=True)
        
        if not acuerdo:
            return jsonify({'success': False, 'message': 'No se encontró un trabajo finalizado con este empleador'})
        
        # Verificar que no haya calificado ya
        existing = execute_query("""
            SELECT ID_Calificacion FROM Calificacion 
            WHERE ID_Usuario_Emisor = %s AND ID_Usuario_Receptor = %s AND ID_Acuerdo = %s
        """, (user_id, employer_id, acuerdo['ID_Acuerdo']), fetch_one=True)
        
        if existing:
            return jsonify({'success': False, 'message': 'Ya has calificado a este empleador'})
        
        # Insertar calificación
        execute_query("""
            INSERT INTO Calificacion 
            (ID_Acuerdo, ID_Usuario_Emisor, ID_Usuario_Receptor, Puntuacion, Comentario)
            VALUES (%s, %s, %s, %s, %s)
        """, (acuerdo['ID_Acuerdo'], user_id, employer_id, str(rating), comment))
        
        return jsonify({'success': True, 'message': 'Calificación enviada correctamente'})
        
    except Exception as e:
        print(f"Error al enviar calificación: {e}")
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

# 4. Endpoint para obtener calificaciones enviadas
@app.route('/api/user-ratings', methods=['GET'])
@require_login
def get_user_ratings():
    try:
        user_id = session['user_id']
        
        calificaciones = execute_query("""
            SELECT c.Puntuacion, c.Comentario, c.Fecha,
                   u.Nombre, u.Apellido
            FROM Calificacion c
            INNER JOIN Usuario u ON c.ID_Usuario_Receptor = u.ID_Usuario
            WHERE c.ID_Usuario_Emisor = %s
            ORDER BY c.Fecha DESC
        """, (user_id,))
        
        ratings_list = []
        if calificaciones:
            for rating in calificaciones:
                ratings_list.append({
                    'calificacion': int(rating['Puntuacion']),
                    'comentario': rating['Comentario'],
                    'fecha': rating['Fecha'].strftime('%Y-%m-%d %H:%M:%S') if rating['Fecha'] else None,
                    'empleador_nombre': f"{rating['Nombre']} {rating['Apellido']}",
                    'empresa': rating['Nombre']
                })
        
        return jsonify({
            'success': True,
            'ratings': ratings_list
        })
        
    except Exception as e:
        print(f"Error al obtener calificaciones: {e}")
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

# 5. Mejorar el endpoint existente de update-profile
@app.route('/api/update-profile', methods=['POST'])
@require_login
def update_profile_mejorado():
    try:
        data = request.get_json()
        user_id = session['user_id']
        
        # Datos básicos
        nombre = data.get('nombre', '').strip()
        apellido = data.get('apellido', '').strip()
        telefono = data.get('telefono', '').strip()
        red_social = data.get('red_social', '').strip()
        
        if not nombre or not apellido:
            return jsonify({'success': False, 'message': 'Nombre y apellido son requeridos'})
        
        # Actualizar datos básicos
        execute_query("""
            UPDATE Usuario 
            SET Nombre = %s, Apellido = %s, Telefono = %s, Red_Social = %s
            WHERE ID_Usuario = %s
        """, (nombre, apellido, telefono, red_social, user_id))
        
        # Datos profesionales (guardar en JSON de Configuraciones)
        configuraciones = {}
        campos_profesionales = ['area_trabajo', 'especializacion', 'anos_experiencia', 'nivel_educativo', 'ubicacion']
        
        for campo in campos_profesionales:
            if campo in data and data[campo]:
                configuraciones[campo] = data[campo]
        
        if configuraciones:
            import json
            execute_query("""
                UPDATE Usuario 
                SET Configuraciones = %s
                WHERE ID_Usuario = %s
            """, (json.dumps(configuraciones), user_id))
        
        return jsonify({'success': True, 'message': 'Perfil actualizado correctamente'})
        
    except Exception as e:
        print(f"Error al actualizar perfil: {e}")
        return jsonify({'success': False, 'message': 'Error interno del servidor'}), 500

# 6. Actualizar get_user_session para incluir campos profesionales
# Reemplaza tu función get_user_session existente con esta versión:
@app.route('/get_user_session')
def get_user_session_actualizado():
    try:
        if 'user_id' in session:
            user_id = session['user_id']
            
            user_data = execute_query(
                """SELECT ID_Usuario, Nombre, Apellido, Correo, Telefono, 
                          URL_Foto, Red_Social, Rol, Estado, Fecha_Registro, Configuraciones
                   FROM Usuario WHERE ID_Usuario = %s""",
                (user_id,),
                fetch_one=True
            )
            
            if not user_data:
                return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
            
            # Parsear configuraciones JSON
            import json
            configuraciones = {}
            if user_data.get('Configuraciones'):
                try:
                    configuraciones = json.loads(user_data['Configuraciones'])
                except:
                    configuraciones = {}
            
            # Estadísticas
            stats = execute_query("""
                SELECT 
                    COUNT(al.ID_Acuerdo) as trabajos_completados,
                    AVG(CAST(c.Puntuacion AS DECIMAL)) as calificacion_promedio
                FROM Usuario u
                LEFT JOIN Acuerdo_Laboral al ON u.ID_Usuario = al.ID_Trabajador AND al.Estado = 'Finalizado'
                LEFT JOIN Calificacion c ON u.ID_Usuario = c.ID_Usuario_Receptor
                WHERE u.ID_Usuario = %s
            """, (user_id,), fetch_one=True)
            
            return jsonify({
                'success': True,
                'user': {
                    'id': user_data['ID_Usuario'],
                    'user_name': f"{user_data['Nombre']} {user_data['Apellido']}",
                    'full_name': f"{user_data['Nombre']} {user_data['Apellido']}",
                    'nombre': user_data['Nombre'],
                    'apellido': user_data['Apellido'],
                    'email': user_data['Correo'],
                    'telefono': user_data.get('Telefono', ''),
                    'url_foto': user_data.get('URL_Foto'),
                    'red_social': user_data.get('Red_Social', ''),
                    'rol': user_data['Rol'],
                    'estado': user_data['Estado'],
                    'fecha_registro': user_data['Fecha_Registro'],
                    
                    # Campos profesionales desde configuraciones
                    'area_trabajo': configuraciones.get('area_trabajo', ''),
                    'especializacion': configuraciones.get('especializacion', ''),
                    'anos_experiencia': configuraciones.get('anos_experiencia', 0),
                    'nivel_educativo': configuraciones.get('nivel_educativo', ''),
                    'ubicacion': configuraciones.get('ubicacion', ''),
                    
                    # Estadísticas
                    'trabajos_completados': stats['trabajos_completados'] if stats else 0,
                    'calificacion_promedio': float(stats['calificacion_promedio']) if stats and stats['calificacion_promedio'] else 0.0
                }
            })
        else:
            return jsonify({'success': False, 'message': 'No hay sesión activa'}), 401
            
    except Exception as e:
        print(f"Error obteniendo sesión: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ================================================================
# RUTAS DE PROCESAMIENTO FALTANTES - AGREGAR A APP.PY
# Estas son las rutas que procesan el login sin rol específico
# ================================================================

@app.route('/auth/google/login-process', methods=['POST'])
def google_login_process():
    """Procesar login con Google (desde página de login - sin rol específico)"""
    try:
        google_email = request.form.get('google_email', '').strip().lower()
        
        print(f"Procesando login con Google para: {google_email}")
        
        # Validar email de Google
        if not google_email or not (google_email.endswith('@gmail.com') or google_email.endswith('@googlemail.com')):
            return redirect('/vista/login-trabajador.html?message=Por favor ingresa un correo válido de Gmail&type=error')
        
        # Buscar si el usuario ya existe
        existing_user = execute_query(
            "SELECT * FROM Usuario WHERE Correo = %s",
            (google_email,),
            fetch_one=True
        )
        
        if not existing_user:
            # Usuario no existe, redirigir a selección de rol para registro
            return redirect(f'/vista/seleccion-rol.html?email={quote(google_email)}&provider=google&message=Cuenta no encontrada. Selecciona tu rol para registrarte&type=info')
        
        # Usuario existe, crear sesión
        user = existing_user
        session['user_id'] = user['ID_Usuario']
        session['username'] = user['Correo']
        session['first_name'] = user['Nombre']
        session['last_name'] = user['Apellido']
        session['email'] = user['Correo']
        session['user_role'] = user['Rol']
        session['user_name'] = f"{user['Nombre']} {user['Apellido']}"
        session['telefono'] = user.get('Telefono', '')
        
        print(f"Login exitoso con Google: {user['Nombre']} - Rol: {user['Rol']}")
        
        # Redireccionar según el rol
        if user['Rol'] == 'Agricultor':
            return redirect('/vista/index-agricultor.html')
        else:
            return redirect('/vista/index-trabajador.html')
        
    except Exception as e:
        print(f"Error en login Google: {str(e)}")
        return redirect('/vista/login-trabajador.html?message=Error procesando Google&type=error')

@app.route('/auth/facebook/login-process', methods=['POST'])
def facebook_login_process():
    """Procesar login con Facebook (desde página de login - sin rol específico)"""
    try:
        facebook_email = request.form.get('facebook_email', '').strip().lower()
        
        print(f"Procesando login con Facebook para: {facebook_email}")
        
        # Validar email de Facebook
        valid_domains = ['@hotmail.com', '@outlook.com', '@live.com', '@msn.com']
        if not facebook_email or not any(facebook_email.endswith(domain) for domain in valid_domains):
            return redirect('/vista/login-trabajador.html?message=Por favor ingresa un correo válido asociado a Facebook&type=error')
        
        # Buscar si el usuario ya existe
        existing_user = execute_query(
            "SELECT * FROM Usuario WHERE Correo = %s",
            (facebook_email,),
            fetch_one=True
        )
        
        if not existing_user:
            # Usuario no existe, redirigir a selección de rol para registro
            return redirect(f'/vista/seleccion-rol.html?email={quote(facebook_email)}&provider=facebook&message=Cuenta no encontrada. Selecciona tu rol para registrarte&type=info')
        
        # Usuario existe, crear sesión
        user = existing_user
        session['user_id'] = user['ID_Usuario']
        session['username'] = user['Correo']
        session['first_name'] = user['Nombre']
        session['last_name'] = user['Apellido']
        session['email'] = user['Correo']
        session['user_role'] = user['Rol']
        session['user_name'] = f"{user['Nombre']} {user['Apellido']}"
        session['telefono'] = user.get('Telefono', '')
        
        print(f"Login exitoso con Facebook: {user['Nombre']} - Rol: {user['Rol']}")
        
        # Redireccionar según el rol
        if user['Rol'] == 'Agricultor':
            return redirect('/vista/index-agricultor.html')
        else:
            return redirect('/vista/index-trabajador.html')
        
    except Exception as e:
        print(f"Error en login Facebook: {str(e)}")
        return redirect('/vista/login-trabajador.html?message=Error procesando Facebook&type=error')

@app.route('/auth/google/process', methods=['POST'])
def google_register_process():
    """Procesar registro con Google (desde páginas de registro - con rol específico)"""
    try:
        google_email = request.form.get('google_email', '').strip().lower()
        rol = request.form.get('rol', 'Trabajador')
        
        print(f"Procesando registro con Google para: {google_email} como {rol}")
        
        # Validar email de Google
        if not google_email or not (google_email.endswith('@gmail.com') or google_email.endswith('@googlemail.com')):
            redirect_url = '/vista/registro-agricultor.html' if rol == 'Agricultor' else '/vista/registro-trabajador.html'
            return redirect(f'{redirect_url}?message=Por favor ingresa un correo válido de Gmail&type=error')
        
        # Verificar si el usuario ya existe
        existing_user = execute_query(
            "SELECT * FROM Usuario WHERE Correo = %s",
            (google_email,),
            fetch_one=True
        )
        
        if existing_user:
            # Usuario existe, iniciar sesión
            user = existing_user
            print(f"Usuario existente encontrado: {existing_user['Nombre']}")
        else:
            # Crear nuevo usuario
            user_id = create_social_user_real(google_email, 'google', rol)
            if not user_id:
                redirect_url = '/vista/registro-agricultor.html' if rol == 'Agricultor' else '/vista/registro-trabajador.html'
                return redirect(f'{redirect_url}?message=Error creando usuario con Google&type=error')
            
            user = execute_query(
                "SELECT * FROM Usuario WHERE ID_Usuario = %s",
                (user_id,),
                fetch_one=True
            )
        
        # Crear sesión
        session['user_id'] = user['ID_Usuario']
        session['username'] = user['Correo']
        session['first_name'] = user['Nombre']
        session['last_name'] = user['Apellido']
        session['email'] = user['Correo']
        session['user_role'] = user['Rol']
        session['user_name'] = f"{user['Nombre']} {user['Apellido']}"
        session['telefono'] = user.get('Telefono', '')
        
        session.pop('oauth_rol', None)
        
        print(f"Registro/Login exitoso con Google: {user['Nombre']} - Rol: {user['Rol']}")
        
        # Redireccionar según el rol
        if user['Rol'] == 'Agricultor':
            return redirect('/vista/index-agricultor.html')
        else:
            return redirect('/vista/index-trabajador.html')
        
    except Exception as e:
        print(f"Error procesando registro Google: {str(e)}")
        return redirect('/vista/registro-trabajador.html?message=Error con Google&type=error')

@app.route('/auth/facebook/process', methods=['POST'])
def facebook_register_process():
    """Procesar registro con Facebook (desde páginas de registro - con rol específico)"""
    try:
        facebook_email = request.form.get('facebook_email', '').strip().lower()
        rol = request.form.get('rol', 'Trabajador')
        
        print(f"Procesando registro con Facebook para: {facebook_email} como {rol}")
        
        # Validar email de Facebook
        valid_domains = ['@hotmail.com', '@outlook.com', '@live.com', '@msn.com']
        if not facebook_email or not any(facebook_email.endswith(domain) for domain in valid_domains):
            redirect_url = '/vista/registro-agricultor.html' if rol == 'Agricultor' else '/vista/registro-trabajador.html'
            return redirect(f'{redirect_url}?message=Por favor ingresa un correo válido asociado a Facebook&type=error')
        
        # Verificar si el usuario ya existe
        existing_user = execute_query(
            "SELECT * FROM Usuario WHERE Correo = %s",
            (facebook_email,),
            fetch_one=True
        )
        
        if existing_user:
            # Usuario existe, iniciar sesión
            user = existing_user
            print(f"Usuario existente encontrado: {existing_user['Nombre']}")
        else:
            # Crear nuevo usuario
            user_id = create_social_user_real(facebook_email, 'facebook', rol)
            if not user_id:
                redirect_url = '/vista/registro-agricultor.html' if rol == 'Agricultor' else '/vista/registro-trabajador.html'
                return redirect(f'{redirect_url}?message=Error creando usuario con Facebook&type=error')
            
            user = execute_query(
                "SELECT * FROM Usuario WHERE ID_Usuario = %s",
                (user_id,),
                fetch_one=True
            )
        
        # Crear sesión
        session['user_id'] = user['ID_Usuario']
        session['username'] = user['Correo']
        session['first_name'] = user['Nombre']
        session['last_name'] = user['Apellido']
        session['email'] = user['Correo']
        session['user_role'] = user['Rol']
        session['user_name'] = f"{user['Nombre']} {user['Apellido']}"
        session['telefono'] = user.get('Telefono', '')
        
        session.pop('oauth_rol', None)
        
        print(f"Registro/Login exitoso con Facebook: {user['Nombre']} - Rol: {user['Rol']}")
        
        # Redireccionar según el rol
        if user['Rol'] == 'Agricultor':
            return redirect('/vista/index-agricultor.html')
        else:
            return redirect('/vista/index-trabajador.html')
        
    except Exception as e:
        print(f"Error procesando registro Facebook: {str(e)}")
        return redirect('/vista/registro-trabajador.html?message=Error con Facebook&type=error')

# También necesitas la función auxiliar si no la tienes:
def create_social_user_real(email, provider, rol='Trabajador'):
    """Crea un usuario real desde email de red social"""
    try:
        # Extraer información del email
        user_info = extract_info_from_email(email, provider)
        if not user_info:
            return None
        
        # Generar contraseña temporal hasheada
        temp_password = hash_password(f"{email}_social_{provider}_{uuid.uuid4()}")
        
        # URL de foto por defecto según el proveedor
        if provider == 'google':
            foto_url = "/static/uploads/profile_photos/default_google_user.jpg"
        else:
            foto_url = "/static/uploads/profile_photos/default_facebook_user.jpg"
        
        # Insertar en base de datos
        user_id = execute_query(
            """INSERT INTO Usuario (Nombre, Apellido, Correo, Contrasena, URL_Foto, 
                                   Red_Social, Rol, Estado) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, 'Activo')""",
            (
                user_info['nombre'],
                user_info['apellido'], 
                email,
                temp_password,
                foto_url,
                f"{provider}:{user_info['username']}",
                rol
            )
        )
        
        print(f"Usuario real creado desde {provider}: {email} - Rol: {rol}")
        return user_id
        
    except Exception as e:
        print(f"Error creando usuario social real: {str(e)}")
        return None

def extract_info_from_email(email, provider):
    """Extrae información básica del email para crear el usuario"""
    try:
        import re
        # Extraer nombre del email (parte antes del @)
        username = email.split('@')[0]
        
        # Limpiar números y caracteres especiales
        clean_name = re.sub(r'[0-9._-]', ' ', username).strip()
        
        # Dividir en nombre y apellido
        name_parts = clean_name.split()
        
        if len(name_parts) >= 2:
            nombre = name_parts[0].capitalize()
            apellido = ' '.join(name_parts[1:]).title()
        elif len(name_parts) == 1:
            nombre = name_parts[0].capitalize()
            apellido = "Usuario"
        else:
            nombre = "Usuario"
            apellido = provider.capitalize()
        
        return {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'username': username,
            'provider': provider
        }
        
    except Exception as e:
        print(f"Error extrayendo info del email: {str(e)}")
        return None

print("✅ Rutas de procesamiento social agregadas correctamente")


# ================================================================
# RUTAS PARA ARCHIVOS HTML DE LA CARPETA VISTA
# ================================================================

@app.route('/vista/favoritos.html')
def favoritos_html():
    """Página de favoritos"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        return send_from_directory(vista_path, 'favoritos.html')
    except Exception as e:
        print(f"Error sirviendo favoritos.html: {e}")
        return "Archivo no encontrado", 404

@app.route('/vista/historial-empleos.html')
def historial_empleos_html():
    """Página de historial de empleos"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        return send_from_directory(vista_path, 'historial-empleos.html')
    except Exception as e:
        print(f"Error sirviendo historial-empleos.html: {e}")
        return "Archivo no encontrado", 404

@app.route('/vista/postulaciones.html')
def postulaciones_html():
    """Página de postulaciones"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        return send_from_directory(vista_path, 'postulaciones.html')
    except Exception as e:
        print(f"Error sirviendo postulaciones.html: {e}")
        return "Archivo no encontrado", 404

@app.route('/vista/configuracion-trabajador.html')
def configuracion_trabajador_html():
    """Página de configuración del trabajador"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        return send_from_directory(vista_path, 'configuracion-trabajador.html')
    except Exception as e:
        print(f"Error sirviendo configuracion-trabajador.html: {e}")
        return "Archivo no encontrado", 404

@app.route('/vista/estadisticas-trabajador.html')
def estadisticas_trabajador_html():
    """Página de estadísticas del trabajador"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        return send_from_directory(vista_path, 'estadisticas-trabajador.html')
    except Exception as e:
        print(f"Error sirviendo estadisticas-trabajador.html: {e}")
        return "Archivo no encontrado", 404

@app.route('/vista/index-agricultor.html')
def index_agricultor_html():
    """Dashboard principal del agricultor"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        return send_from_directory(vista_path, 'index-agricultor.html')
    except Exception as e:
        print(f"Error sirviendo index-agricultor.html: {e}")
        return "Archivo no encontrado", 404

@app.route('/vista/index-trabajador.html')
def index_trabajador_html():
    """Dashboard principal del trabajador"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        return send_from_directory(vista_path, 'index-trabajador.html')
    except Exception as e:
        print(f"Error sirviendo index-trabajador.html: {e}")
        return "Archivo no encontrado", 404

@app.route('/vista/login-trabajador.html')
def login_trabajador_html():
    """Página de login"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        return send_from_directory(vista_path, 'login-trabajador.html')
    except Exception as e:
        print(f"Error sirviendo login-trabajador.html: {e}")
        return "Archivo no encontrado", 404

@app.route('/vista/perfil-trabajador.html')
def perfil_trabajador_html():
    """Página de perfil del trabajador"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        return send_from_directory(vista_path, 'perfil-trabajador.html')
    except Exception as e:
        print(f"Error sirviendo perfil-trabajador.html: {e}")
        return "Archivo no encontrado", 404

@app.route('/vista/registro-trabajador.html')
def registro_trabajador_html():
    """Página de registro del trabajador"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        return send_from_directory(vista_path, 'registro-trabajador.html')
    except Exception as e:
        print(f"Error sirviendo registro-trabajador.html: {e}")
        return "Archivo no encontrado", 404

@app.route('/vista/seleccion-rol.html')
def seleccion_rol_html():
    """Página de selección de rol"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        vista_path = os.path.join(base_dir, '..', 'vista')
        vista_path = os.path.abspath(vista_path)
        return send_from_directory(vista_path, 'seleccion-rol.html')
    except Exception as e:
        print(f"Error sirviendo seleccion-rol.html: {e}")
        return "Archivo no encontrado", 404

# ================================================================
# RUTAS PARA ARCHIVOS CSS DE ASSENT/CSS
# ================================================================

@app.route('/assent/css/favoritos.css')
def favoritos_css():
    """CSS para página de favoritos"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(base_dir, '..', 'assent', 'css')
        css_path = os.path.abspath(css_path)
        response = send_from_directory(css_path, 'favoritos.css')
        response.headers['Content-Type'] = 'text/css'
        return response
    except Exception as e:
        print(f"Error sirviendo favoritos.css: {e}")
        return "CSS no encontrado", 404

@app.route('/assent/css/historial-empleos.css')
def historial_empleos_css():
    """CSS para página de historial de empleos"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(base_dir, '..', 'assent', 'css')
        css_path = os.path.abspath(css_path)
        response = send_from_directory(css_path, 'historial-empleos.css')
        response.headers['Content-Type'] = 'text/css'
        return response
    except Exception as e:
        print(f"Error sirviendo historial-empleos.css: {e}")
        return "CSS no encontrado", 404

@app.route('/assent/css/postulaciones.css')
def postulaciones_css():
    """CSS para página de postulaciones"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(base_dir, '..', 'assent', 'css')
        css_path = os.path.abspath(css_path)
        response = send_from_directory(css_path, 'postulaciones.css')
        response.headers['Content-Type'] = 'text/css'
        return response
    except Exception as e:
        print(f"Error sirviendo postulaciones.css: {e}")
        return "CSS no encontrado", 404

# ================================================================
# RUTAS PARA ARCHIVOS JAVASCRIPT DE JS/
# ================================================================

@app.route('/js/favoritos.js')
def favoritos_js():
    """JavaScript para página de favoritos"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        js_path = os.path.join(base_dir, '..', 'js')
        js_path = os.path.abspath(js_path)
        response = send_from_directory(js_path, 'favoritos.js')
        response.headers['Content-Type'] = 'application/javascript'
        return response
    except Exception as e:
        print(f"Error sirviendo favoritos.js: {e}")
        return "JS no encontrado", 404

@app.route('/js/historial-empleos.js')
def historial_empleos_js():
    """JavaScript para página de historial de empleos"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        js_path = os.path.join(base_dir, '..', 'js')
        js_path = os.path.abspath(js_path)
        response = send_from_directory(js_path, 'historial-empleos.js')
        response.headers['Content-Type'] = 'application/javascript'
        return response
    except Exception as e:
        print(f"Error sirviendo historial-empleos.js: {e}")
        return "JS no encontrado", 404

@app.route('/js/postulaciones.js')
def postulaciones_js():
    """JavaScript para página de postulaciones"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        js_path = os.path.join(base_dir, '..', 'js')
        js_path = os.path.abspath(js_path)
        response = send_from_directory(js_path, 'postulaciones.js')
        response.headers['Content-Type'] = 'application/javascript'
        return response
    except Exception as e:
        print(f"Error sirviendo postulaciones.js: {e}")
        return "JS no encontrado", 404

# ================================================================
# APIS PARA FAVORITOS, HISTORIAL Y POSTULACIONES
# ================================================================

@app.route('/api/favoritos', methods=['GET', 'POST'])
@require_login
def handle_favoritos():
    """API para manejar trabajos favoritos usando tabla Postulacion"""
    user_id = session['user_id']
    
    if request.method == 'GET':
        try:
            favoritos = execute_query("""
                SELECT p.ID_Oferta, ot.Titulo, p.Fecha_Postulacion,
                       ot.Descripcion, ot.Pago_Ofrecido, ot.Estado,
                       CONCAT(u.Nombre, ' ', u.Apellido) as Agricultor,
                       pr.Nombre_Finca as Ubicacion
                FROM Postulacion p
                JOIN Oferta_Trabajo ot ON p.ID_Oferta = ot.ID_Oferta
                JOIN Usuario u ON ot.ID_Agricultor = u.ID_Usuario
                LEFT JOIN Predio pr ON u.ID_Usuario = pr.ID_Usuario
                WHERE p.ID_Trabajador = %s AND p.Estado = 'Favorito'
                ORDER BY p.Fecha_Postulacion DESC
            """, (user_id,))
            
            favoritos_list = []
            if favoritos:
                for fav in favoritos:
                    favoritos_list.append({
                        'job_id': fav['ID_Oferta'],
                        'titulo': fav['Titulo'],
                        'descripcion': fav['Descripcion'],
                        'pago': float(fav['Pago_Ofrecido']),
                        'agricultor': fav['Agricultor'],
                        'ubicacion': fav['Ubicacion'] if fav['Ubicacion'] else 'No especificada',
                        'estado': fav['Estado'],
                        'fecha_agregado': fav['Fecha_Postulacion'].isoformat() if fav['Fecha_Postulacion'] else None
                    })
            
            return jsonify({
                'success': True,
                'favoritos': favoritos_list
            })
            
        except Exception as e:
            print(f"Error obteniendo favoritos: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            job_id = data.get('job_id')
            action = data.get('action')
            
            if not job_id or not action:
                return jsonify({'success': False, 'error': 'Datos incompletos'}), 400
            
            if action == 'add':
                # Verificar si ya existe postulación para esta oferta
                existing = execute_query("""
                    SELECT ID_Postulacion, Estado FROM Postulacion 
                    WHERE ID_Trabajador = %s AND ID_Oferta = %s
                """, (user_id, job_id), fetch_one=True)
                
                if existing:
                    # Actualizar estado a Favorito
                    execute_query("""
                        UPDATE Postulacion 
                        SET Estado = 'Favorito', Fecha_Postulacion = CURRENT_TIMESTAMP
                        WHERE ID_Postulacion = %s
                    """, (existing['ID_Postulacion'],))
                else:
                    # Crear nueva entrada como favorito
                    execute_query("""
                        INSERT INTO Postulacion (ID_Oferta, ID_Trabajador, Estado, Fecha_Postulacion)
                        VALUES (%s, %s, 'Favorito', CURRENT_TIMESTAMP)
                    """, (job_id, user_id))
                
                message = "Trabajo agregado a favoritos"
                    
            elif action == 'remove':
                # Eliminar favorito
                execute_query("""
                    DELETE FROM Postulacion 
                    WHERE ID_Trabajador = %s AND ID_Oferta = %s AND Estado = 'Favorito'
                """, (user_id, job_id))
                
                message = "Trabajo removido de favoritos"
            
            return jsonify({
                'success': True,
                'message': message
            })
            
        except Exception as e:
            print(f"Error manejando favoritos: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/historial-empleos', methods=['GET'])
@require_login
def get_historial_empleos():
    """API para obtener historial de empleos del trabajador"""
    try:
        user_id = session['user_id']
        user_role = session.get('user_role')
        
        if user_role != 'Trabajador':
            return jsonify({'success': False, 'error': 'Acceso denegado'}), 403
        
        # Consulta para obtener historial de empleos
        empleos = execute_query("""
            SELECT 
                al.ID_Acuerdo,
                ot.Titulo,
                CONCAT(u.Nombre, ' ', u.Apellido) as Empleador,
                u.ID_Usuario as Empleador_ID,
                al.Fecha_Inicio,
                al.Fecha_Fin,
                al.Pago_Final,
                al.Estado,
                ot.Descripcion,
                c.Puntuacion,
                c.Comentario,
                ot.Pago_Ofrecido,
                p.Nombre_Finca as Ubicacion
            FROM Acuerdo_Laboral al
            JOIN Oferta_Trabajo ot ON al.ID_Oferta = ot.ID_Oferta
            JOIN Usuario u ON ot.ID_Agricultor = u.ID_Usuario
            LEFT JOIN Predio p ON u.ID_Usuario = p.ID_Usuario
            LEFT JOIN Calificacion c ON al.ID_Acuerdo = c.ID_Acuerdo AND c.ID_Usuario_Receptor = %s
            WHERE al.ID_Trabajador = %s
            ORDER BY al.Fecha_Inicio DESC
        """, (user_id, user_id))
        
        empleos_list = []
        if empleos:
            for empleo in empleos:
                # Calcular duración
                if empleo['Fecha_Fin']:
                    duracion_dias = (empleo['Fecha_Fin'] - empleo['Fecha_Inicio']).days + 1
                    duracion = f"{duracion_dias} días"
                else:
                    duracion = "En curso"
                
                # Determinar tipo de trabajo
                descripcion = empleo['Descripcion'].lower()
                if 'cosecha' in descripcion or 'recolección' in descripcion:
                    tipo = 'Cosecha'
                elif 'siembra' in descripcion:
                    tipo = 'Siembra'
                elif 'mantenimiento' in descripcion or 'poda' in descripcion:
                    tipo = 'Mantenimiento'
                else:
                    tipo = 'Otro'
                
                empleo_data = {
                    'id': empleo['ID_Acuerdo'],
                    'titulo': empleo['Titulo'],
                    'empleador': empleo['Empleador'],
                    'empleadorId': empleo['Empleador_ID'],
                    'fechaInicio': empleo['Fecha_Inicio'].strftime('%Y-%m-%d') if empleo['Fecha_Inicio'] else None,
                    'fechaFin': empleo['Fecha_Fin'].strftime('%Y-%m-%d') if empleo['Fecha_Fin'] else None,
                    'duracion': duracion,
                    'estado': empleo['Estado'],
                    'pago': float(empleo['Pago_Final']) if empleo['Pago_Final'] else float(empleo['Pago_Ofrecido']),
                    'ubicacion': empleo['Ubicacion'] if empleo['Ubicacion'] else 'Colombia',
                    'calificacion': empleo['Puntuacion'],
                    'comentario': empleo['Comentario'],
                    'descripcion': empleo['Descripcion'],
                    'tipo': tipo
                }
                empleos_list.append(empleo_data)
        
        return jsonify({
            'success': True,
            'empleos': empleos_list
        })
        
    except Exception as e:
        print(f"Error obteniendo historial: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/postulaciones', methods=['GET'])
@require_login
def get_postulaciones():
    """API para obtener postulaciones del trabajador"""
    try:
        user_id = session['user_id']
        user_role = session.get('user_role')
        
        if user_role != 'Trabajador':
            return jsonify({'success': False, 'error': 'Acceso denegado'}), 403
        
        # Consulta para obtener postulaciones
        postulaciones = execute_query("""
            SELECT 
                p.ID_Postulacion,
                ot.Titulo,
                CONCAT(u.Nombre, ' ', u.Apellido) as Agricultor,
                u.ID_Usuario as Agricultor_ID,
                p.Fecha_Postulacion,
                p.Estado,
                ot.Pago_Ofrecido,
                pr.Nombre_Finca as Ubicacion,
                ot.Descripcion,
                ot.Fecha_Publicacion,
                ot.ID_Oferta,
                (SELECT COUNT(*) FROM Mensaje m 
                 WHERE (m.ID_Emisor = %s AND m.ID_Receptor = u.ID_Usuario) 
                    OR (m.ID_Emisor = u.ID_Usuario AND m.ID_Receptor = %s)) as Mensajes
            FROM Postulacion p
            JOIN Oferta_Trabajo ot ON p.ID_Oferta = ot.ID_Oferta
            JOIN Usuario u ON ot.ID_Agricultor = u.ID_Usuario
            LEFT JOIN Predio pr ON u.ID_Usuario = pr.ID_Usuario
            WHERE p.ID_Trabajador = %s AND p.Estado != 'Favorito'
            ORDER BY p.Fecha_Postulacion DESC
        """, (user_id, user_id, user_id))
        
        postulaciones_list = []
        if postulaciones:
            for post in postulaciones:
                # Simular duración basada en tipo de trabajo
                descripcion = post['Descripcion'].lower()
                if 'cosecha' in descripcion:
                    duracion = "3-5 días"
                elif 'siembra' in descripcion:
                    duracion = "2-4 días"
                elif 'mantenimiento' in descripcion:
                    duracion = "1-2 días"
                else:
                    duracion = "1-3 días"
                
                # Fecha de inicio estimada
                fecha_inicio = post['Fecha_Publicacion'] + timedelta(days=7)
                
                postulacion_data = {
                    'id': post['ID_Postulacion'],
                    'titulo': post['Titulo'],
                    'agricultor': post['Agricultor'],
                    'agricultorId': post['Agricultor_ID'],
                    'fechaPostulacion': post['Fecha_Postulacion'].isoformat(),
                    'estado': post['Estado'],
                    'pago': float(post['Pago_Ofrecido']),
                    'ubicacion': post['Ubicacion'] if post['Ubicacion'] else 'Colombia',
                    'descripcion': post['Descripcion'],
                    'duracion': duracion,
                    'fechaInicio': fecha_inicio.strftime('%Y-%m-%d'),
                    'ultimaActualizacion': post['Fecha_Postulacion'].isoformat(),
                    'mensajes': post['Mensajes'],
                    'prioridad': 'alta' if post['Pago_Ofrecido'] > 50000 else 'media' if post['Pago_Ofrecido'] > 40000 else 'baja',
                    'oferta_id': post['ID_Oferta']
                }
                
                # Información adicional según estado
                if post['Estado'] == 'Rechazada':
                    postulacion_data['motivoRechazo'] = 'Perfil no coincide con los requisitos'
                
                postulaciones_list.append(postulacion_data)
        
        return jsonify({
            'success': True,
            'postulaciones': postulaciones_list
        })
        
    except Exception as e:
        print(f"Error obteniendo postulaciones: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

print("✅ Todas las rutas para favoritos, historial, postulaciones y archivos estáticos cargadas correctamente")


# ================================================================
# RUTA PARA CANCELAR POSTULACIONES
# ================================================================

@app.route('/api/postulaciones/<int:postulacion_id>/cancelar', methods=['POST'])
@require_login
def cancelar_postulacion(postulacion_id):
    """API para cancelar una postulación específica"""
    try:
        user_id = session['user_id']
        user_role = session.get('user_role')
        
        if user_role != 'Trabajador':
            return jsonify({'success': False, 'error': 'Acceso denegado'}), 403
        
        # Verificar que la postulación existe y pertenece al trabajador
        postulacion = execute_query("""
            SELECT p.ID_Postulacion, p.Estado, ot.Titulo
            FROM Postulacion p
            JOIN Oferta_Trabajo ot ON p.ID_Oferta = ot.ID_Oferta
            WHERE p.ID_Postulacion = %s AND p.ID_Trabajador = %s
        """, (postulacion_id, user_id), fetch_one=True)
        
        if not postulacion:
            return jsonify({
                'success': False, 
                'error': 'Postulación no encontrada o no tienes permisos para cancelarla'
            }), 404
        
        # Verificar que se puede cancelar (solo las pendientes)
        if postulacion['Estado'] != 'Pendiente':
            return jsonify({
                'success': False,
                'error': f'No se puede cancelar una postulación con estado: {postulacion["Estado"]}'
            }), 400
        
        # Eliminar la postulación de la base de datos
        execute_query("""
            DELETE FROM Postulacion 
            WHERE ID_Postulacion = %s AND ID_Trabajador = %s
        """, (postulacion_id, user_id))
        
        return jsonify({
            'success': True,
            'message': f'Postulación para "{postulacion["Titulo"]}" cancelada exitosamente'
        })
        
    except Exception as e:
        print(f"Error cancelando postulación: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ================================================================
# MEJORA EN LA API DE POSTULACIONES EXISTENTE
# ================================================================

# Reemplaza la función get_postulaciones existente con esta versión mejorada:
@app.route('/api/postulaciones', methods=['GET'])
@require_login
def get_postulaciones_mejorada():
    """API para obtener postulaciones del trabajador (versión mejorada)"""
    try:
        user_id = session['user_id']
        user_role = session.get('user_role')
        
        if user_role != 'Trabajador':
            return jsonify({'success': False, 'error': 'Acceso denegado'}), 403
        
        # Consulta mejorada para obtener postulaciones con más información
        postulaciones = execute_query("""
            SELECT 
                p.ID_Postulacion,
                p.ID_Oferta,
                ot.Titulo,
                CONCAT(u.Nombre, ' ', u.Apellido) as Agricultor,
                u.ID_Usuario as Agricultor_ID,
                p.Fecha_Postulacion,
                p.Estado,
                ot.Pago_Ofrecido,
                COALESCE(pr.Nombre_Finca, CONCAT(u.Nombre, ' - ', SUBSTRING(u.Correo, 1, LOCATE('@', u.Correo) - 1))) as Ubicacion,
                ot.Descripcion,
                ot.Fecha_Publicacion,
                (SELECT COUNT(*) FROM Mensaje m 
                 WHERE (m.ID_Emisor = %s AND m.ID_Receptor = u.ID_Usuario) 
                    OR (m.ID_Emisor = u.ID_Usuario AND m.ID_Receptor = %s)) as Mensajes,
                -- Calcular duración estimada basada en descripción
                CASE 
                    WHEN LOWER(ot.Descripcion) LIKE '%%cosecha%%' OR LOWER(ot.Descripcion) LIKE '%%recolección%%' THEN '3-5 días'
                    WHEN LOWER(ot.Descripcion) LIKE '%%siembra%%' THEN '2-4 días'
                    WHEN LOWER(ot.Descripcion) LIKE '%%mantenimiento%%' OR LOWER(ot.Descripcion) LIKE '%%poda%%' THEN '1-2 días'
                    WHEN LOWER(ot.Descripcion) LIKE '%%fumigación%%' THEN '1-3 días'
                    ELSE '1-3 días'
                END as Duracion_Estimada,
                -- Calcular prioridad basada en pago
                CASE 
                    WHEN ot.Pago_Ofrecido >= 50000 THEN 'alta'
                    WHEN ot.Pago_Ofrecido >= 40000 THEN 'media'
                    ELSE 'baja'
                END as Prioridad
            FROM Postulacion p
            JOIN Oferta_Trabajo ot ON p.ID_Oferta = ot.ID_Oferta
            JOIN Usuario u ON ot.ID_Agricultor = u.ID_Usuario
            LEFT JOIN Predio pr ON u.ID_Usuario = pr.ID_Usuario
            WHERE p.ID_Trabajador = %s AND p.Estado != 'Favorito'
            ORDER BY p.Fecha_Postulacion DESC
        """, (user_id, user_id, user_id))
        
        postulaciones_list = []
        if postulaciones:
            for post in postulaciones:
                # Fecha de inicio estimada (7 días después de la publicación)
                fecha_inicio = None
                if post['Fecha_Publicacion']:
                    fecha_inicio_dt = post['Fecha_Publicacion'] + timedelta(days=7)
                    fecha_inicio = fecha_inicio_dt.strftime('%Y-%m-%d')
                
                postulacion_data = {
                    'id': post['ID_Postulacion'],
                    'titulo': post['Titulo'],
                    'agricultor': post['Agricultor'],
                    'agricultorId': post['Agricultor_ID'],
                    'fechaPostulacion': post['Fecha_Postulacion'].isoformat() if post['Fecha_Postulacion'] else None,
                    'estado': post['Estado'],
                    'pago': float(post['Pago_Ofrecido']) if post['Pago_Ofrecido'] else 0,
                    'ubicacion': post['Ubicacion'],
                    'descripcion': post['Descripcion'] or 'Descripción no disponible',
                    'duracion': post['Duracion_Estimada'],
                    'fechaInicio': fecha_inicio,
                    'ultimaActualizacion': post['Fecha_Postulacion'].isoformat() if post['Fecha_Postulacion'] else None,
                    'mensajes': post['Mensajes'] or 0,
                    'prioridad': post['Prioridad'],
                    'oferta_id': post['ID_Oferta']
                }
                
                # Información adicional según estado
                if post['Estado'] == 'Rechazada':
                    postulacion_data['motivoRechazo'] = 'El agricultor seleccionó otro candidato'
                
                postulaciones_list.append(postulacion_data)
        
        return jsonify({
            'success': True,
            'postulaciones': postulaciones_list,
            'total': len(postulaciones_list)
        })
        
    except Exception as e:
        print(f"Error obteniendo postulaciones: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ================================================================
# RUTA PARA CREAR NUEVA POSTULACIÓN
# ================================================================

@app.route('/api/postulaciones', methods=['POST'])
@require_login
def crear_postulacion():
    """API para crear una nueva postulación a un trabajo"""
    try:
        user_id = session['user_id']
        user_role = session.get('user_role')
        
        if user_role != 'Trabajador':
            return jsonify({'success': False, 'error': 'Solo los trabajadores pueden postularse'}), 403
        
        data = request.get_json()
        oferta_id = data.get('oferta_id')
        
        if not oferta_id:
            return jsonify({'success': False, 'error': 'ID de oferta requerido'}), 400
        
        # Verificar que la oferta existe y está abierta
        oferta = execute_query("""
            SELECT ID_Oferta, Titulo, Estado, ID_Agricultor 
            FROM Oferta_Trabajo 
            WHERE ID_Oferta = %s
        """, (oferta_id,), fetch_one=True)
        
        if not oferta:
            return jsonify({'success': False, 'error': 'Oferta de trabajo no encontrada'}), 404
        
        if oferta['Estado'] != 'Abierta':
            return jsonify({'success': False, 'error': 'Esta oferta ya no está disponible'}), 400
        
        # Verificar que el trabajador no se postule a su propia oferta (en caso de que sea agricultor también)
        if oferta['ID_Agricultor'] == user_id:
            return jsonify({'success': False, 'error': 'No puedes postularte a tu propia oferta'}), 400
        
        # Verificar que no existe ya una postulación
        postulacion_existente = execute_query("""
            SELECT ID_Postulacion FROM Postulacion 
            WHERE ID_Oferta = %s AND ID_Trabajador = %s
        """, (oferta_id, user_id), fetch_one=True)
        
        if postulacion_existente:
            return jsonify({'success': False, 'error': 'Ya te has postulado a esta oferta'}), 400
        
        # Crear la postulación
        execute_query("""
            INSERT INTO Postulacion (ID_Oferta, ID_Trabajador, Estado, Fecha_Postulacion)
            VALUES (%s, %s, 'Pendiente', CURRENT_TIMESTAMP)
        """, (oferta_id, user_id))
        
        return jsonify({
            'success': True,
            'message': f'Te has postulado exitosamente para "{oferta["Titulo"]}"'
        })
        
    except Exception as e:
        print(f"Error creando postulación: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

print("✅ Rutas para cancelar postulaciones y API mejorada agregadas correctamente")

# ================================================================
# RUTAS PARA POSTULACIONES Y FAVORITOS DESDE EL DASHBOARD
# ================================================================

@app.route('/api/trabajos-disponibles', methods=['GET'])
@require_login
def get_trabajos_disponibles():
    """API para obtener trabajos disponibles en el dashboard"""
    try:
        user_id = session['user_id']
        user_role = session.get('user_role')
        
        if user_role != 'Trabajador':
            return jsonify({'success': False, 'error': 'Acceso denegado'}), 403
        
        # Obtener trabajos disponibles que no sean del propio usuario y que estén abiertos
        trabajos = execute_query("""
            SELECT 
                ot.ID_Oferta,
                ot.Titulo,
                ot.Descripcion,
                ot.Pago_Ofrecido,
                ot.Estado as Estado_Oferta,
                ot.Fecha_Publicacion,
                CONCAT(u.Nombre, ' ', u.Apellido) as Empleador,
                COALESCE(pr.Nombre_Finca, CONCAT(u.Nombre, ' - Finca')) as Ubicacion,
                u.ID_Usuario as Empleador_ID,
                -- Verificar si el trabajador ya se postuló
                (SELECT COUNT(*) FROM Postulacion p 
                 WHERE p.ID_Oferta = ot.ID_Oferta AND p.ID_Trabajador = %s) as Ya_Postulado,
                -- Verificar si está en favoritos
                (SELECT COUNT(*) FROM Postulacion p 
                 WHERE p.ID_Oferta = ot.ID_Oferta AND p.ID_Trabajador = %s AND p.Estado = 'Favorito') as Es_Favorito
            FROM Oferta_Trabajo ot
            JOIN Usuario u ON ot.ID_Agricultor = u.ID_Usuario
            LEFT JOIN Predio pr ON u.ID_Usuario = pr.ID_Usuario
            WHERE ot.ID_Agricultor != %s 
              AND ot.Estado = 'Abierta'
              AND ot.Fecha_Publicacion >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            ORDER BY ot.Fecha_Publicacion DESC
            LIMIT 20
        """, (user_id, user_id, user_id))
        
        trabajos_list = []
        if trabajos:
            for trabajo in trabajos:
                # Determinar el tipo basado en la descripción
                descripcion_lower = trabajo['Descripcion'].lower()
                if 'cosecha' in descripcion_lower or 'recolección' in descripcion_lower:
                    tipo = 'cosecha'
                elif 'siembra' in descripcion_lower:
                    tipo = 'siembra'
                elif 'mantenimiento' in descripcion_lower or 'poda' in descripcion_lower:
                    tipo = 'mantenimiento'
                elif 'recolección' in descripcion_lower:
                    tipo = 'recoleccion'
                else:
                    tipo = 'otros'
                
                # Calcular duración estimada
                if 'cosecha' in descripcion_lower or 'café' in descripcion_lower:
                    duracion = '3-5 días'
                elif 'siembra' in descripcion_lower:
                    duracion = '2-4 días'
                elif 'mantenimiento' in descripcion_lower:
                    duracion = '1-2 días'
                else:
                    duracion = '1-3 días'
                
                trabajo_data = {
                    'id': trabajo['ID_Oferta'],
                    'titulo': trabajo['Titulo'],
                    'descripcion': trabajo['Descripcion'],
                    'pago': float(trabajo['Pago_Ofrecido']) if trabajo['Pago_Ofrecido'] else 0,
                    'empleador': trabajo['Empleador'],
                    'empleador_id': trabajo['Empleador_ID'],
                    'ubicacion': trabajo['Ubicacion'],
                    'fecha_publicacion': trabajo['Fecha_Publicacion'].isoformat() if trabajo['Fecha_Publicacion'] else None,
                    'tipo': tipo,
                    'duracion': duracion,
                    'ya_postulado': bool(trabajo['Ya_Postulado']),
                    'es_favorito': bool(trabajo['Es_Favorito'])
                }
                trabajos_list.append(trabajo_data)
        
        return jsonify({
            'success': True,
            'trabajos': trabajos_list,
            'total': len(trabajos_list)
        })
        
    except Exception as e:
        print(f"Error obteniendo trabajos disponibles: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/postular-trabajo', methods=['POST'])
@require_login
def postular_trabajo():
    """API para postularse a un trabajo desde el dashboard"""
    try:
        user_id = session['user_id']
        user_role = session.get('user_role')
        
        if user_role != 'Trabajador':
            return jsonify({'success': False, 'error': 'Solo los trabajadores pueden postularse'}), 403
        
        data = request.get_json()
        oferta_id = data.get('oferta_id')
        
        if not oferta_id:
            return jsonify({'success': False, 'error': 'ID de oferta requerido'}), 400
        
        # Verificar que la oferta existe y está disponible
        oferta = execute_query("""
            SELECT 
                ot.ID_Oferta, 
                ot.Titulo, 
                ot.Estado, 
                ot.ID_Agricultor,
                CONCAT(u.Nombre, ' ', u.Apellido) as Empleador
            FROM Oferta_Trabajo ot
            JOIN Usuario u ON ot.ID_Agricultor = u.ID_Usuario
            WHERE ot.ID_Oferta = %s
        """, (oferta_id,), fetch_one=True)
        
        if not oferta:
            return jsonify({'success': False, 'error': 'Oferta de trabajo no encontrada'}), 404
        
        if oferta['Estado'] != 'Abierta':
            return jsonify({'success': False, 'error': 'Esta oferta ya no está disponible'}), 400
        
        # Verificar que no se postule a su propia oferta
        if oferta['ID_Agricultor'] == user_id:
            return jsonify({'success': False, 'error': 'No puedes postularte a tu propia oferta'}), 400
        
        # Verificar si ya existe una postulación (no favorito)
        postulacion_existente = execute_query("""
            SELECT ID_Postulacion FROM Postulacion 
            WHERE ID_Oferta = %s AND ID_Trabajador = %s AND Estado != 'Favorito'
        """, (oferta_id, user_id), fetch_one=True)
        
        if postulacion_existente:
            return jsonify({'success': False, 'error': 'Ya te has postulado a esta oferta'}), 400
        
        # Verificar si existe como favorito, en ese caso actualizar el estado
        favorito_existente = execute_query("""
            SELECT ID_Postulacion FROM Postulacion 
            WHERE ID_Oferta = %s AND ID_Trabajador = %s AND Estado = 'Favorito'
        """, (oferta_id, user_id), fetch_one=True)
        
        if favorito_existente:
            # Actualizar de favorito a postulación pendiente
            execute_query("""
                UPDATE Postulacion 
                SET Estado = 'Pendiente', Fecha_Postulacion = CURRENT_TIMESTAMP
                WHERE ID_Postulacion = %s
            """, (favorito_existente['ID_Postulacion'],))
        else:
            # Crear nueva postulación
            execute_query("""
                INSERT INTO Postulacion (ID_Oferta, ID_Trabajador, Estado, Fecha_Postulacion)
                VALUES (%s, %s, 'Pendiente', CURRENT_TIMESTAMP)
            """, (oferta_id, user_id))
        
        return jsonify({
            'success': True,
            'message': f'Te has postulado exitosamente para "{oferta["Titulo"]}" con {oferta["Empleador"]}',
            'oferta_titulo': oferta['Titulo'],
            'empleador': oferta['Empleador']
        })
        
    except Exception as e:
        print(f"Error creando postulación: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/toggle-favorito', methods=['POST'])
@require_login
def toggle_favorito():
    """API para agregar/quitar favoritos desde el dashboard"""
    try:
        user_id = session['user_id']
        user_role = session.get('user_role')
        
        if user_role != 'Trabajador':
            return jsonify({'success': False, 'error': 'Acceso denegado'}), 403
        
        data = request.get_json()
        oferta_id = data.get('job_id')  # Mantener compatibilidad con el frontend
        action = data.get('action')
        
        if not oferta_id or not action:
            return jsonify({'success': False, 'error': 'Datos incompletos'}), 400
        
        # Verificar que la oferta existe
        oferta = execute_query("""
            SELECT 
                ot.ID_Oferta, 
                ot.Titulo, 
                ot.Estado,
                CONCAT(u.Nombre, ' ', u.Apellido) as Empleador
            FROM Oferta_Trabajo ot
            JOIN Usuario u ON ot.ID_Agricultor = u.ID_Usuario
            WHERE ot.ID_Oferta = %s
        """, (oferta_id,), fetch_one=True)
        
        if not oferta:
            return jsonify({'success': False, 'error': 'Oferta no encontrada'}), 404
        
        # Verificar si ya existe algún tipo de postulación
        postulacion_existente = execute_query("""
            SELECT ID_Postulacion, Estado FROM Postulacion 
            WHERE ID_Oferta = %s AND ID_Trabajador = %s
        """, (oferta_id, user_id), fetch_one=True)
        
        if action == 'add':
            if postulacion_existente:
                if postulacion_existente['Estado'] == 'Favorito':
                    # Ya es favorito
                    return jsonify({'success': False, 'error': 'Ya está en favoritos'}), 400
                else:
                    # Ya hay postulación activa, no se puede agregar como favorito
                    return jsonify({'success': False, 'error': 'Ya tienes una postulación activa para este trabajo'}), 400
            else:
                # Crear nueva entrada como favorito
                execute_query("""
                    INSERT INTO Postulacion (ID_Oferta, ID_Trabajador, Estado, Fecha_Postulacion)
                    VALUES (%s, %s, 'Favorito', CURRENT_TIMESTAMP)
                """, (oferta_id, user_id))
                
                message = f'"{oferta["Titulo"]}" agregado a favoritos'
        
        elif action == 'remove':
            if postulacion_existente and postulacion_existente['Estado'] == 'Favorito':
                # Eliminar favorito
                execute_query("""
                    DELETE FROM Postulacion 
                    WHERE ID_Postulacion = %s
                """, (postulacion_existente['ID_Postulacion'],))
                
                message = f'"{oferta["Titulo"]}" removido de favoritos'
            else:
                return jsonify({'success': False, 'error': 'No está en favoritos'}), 400
        
        else:
            return jsonify({'success': False, 'error': 'Acción no válida'}), 400
        
        return jsonify({
            'success': True,
            'message': message,
            'oferta_titulo': oferta['Titulo']
        })
        
    except Exception as e:
        print(f"Error manejando favorito: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/dashboard-stats', methods=['GET'])
@require_login
def get_dashboard_stats():
    """API para obtener estadísticas del dashboard"""
    try:
        user_id = session['user_id']
        user_role = session.get('user_role')
        
        if user_role != 'Trabajador':
            return jsonify({'success': False, 'error': 'Acceso denegado'}), 403
        
        # Contar trabajos cercanos (ofertas disponibles)
        trabajos_cercanos = execute_query("""
            SELECT COUNT(*) as total
            FROM Oferta_Trabajo ot
            WHERE ot.ID_Agricultor != %s 
              AND ot.Estado = 'Abierta'
              AND ot.Fecha_Publicacion >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        """, (user_id,), fetch_one=True)
        
        # Contar postulaciones pendientes
        postulaciones_pendientes = execute_query("""
            SELECT COUNT(*) as total
            FROM Postulacion p
            WHERE p.ID_Trabajador = %s 
              AND p.Estado = 'Pendiente'
        """, (user_id,), fetch_one=True)
        
        # Contar trabajos en progreso (acuerdos activos)
        trabajos_progreso = execute_query("""
            SELECT COUNT(*) as total
            FROM Acuerdo_Laboral al
            WHERE al.ID_Trabajador = %s 
              AND al.Estado = 'Activo'
        """, (user_id,), fetch_one=True)
        
        # Contar favoritos
        favoritos = execute_query("""
            SELECT COUNT(*) as total
            FROM Postulacion p
            WHERE p.ID_Trabajador = %s 
              AND p.Estado = 'Favorito'
        """, (user_id,), fetch_one=True)
        
        return jsonify({
            'success': True,
            'stats': {
                'trabajos_cercanos': trabajos_cercanos['total'] if trabajos_cercanos else 0,
                'postulaciones': postulaciones_pendientes['total'] if postulaciones_pendientes else 0,
                'en_progreso': trabajos_progreso['total'] if trabajos_progreso else 0,
                'favoritos': favoritos['total'] if favoritos else 0
            }
        })
        
    except Exception as e:
        print(f"Error obteniendo estadísticas: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

print("✅ Rutas para postulaciones y favoritos desde dashboard agregadas correctamente")

# ================================================================
# INICIO DEL SERVIDOR   
# ================================================================
if __name__ == '__main__':
    print("=" * 70)
    print("🌱 INICIANDO SERVIDOR AGROMATCH - VERSIÓN DASHBOARD SEPARADO")
    print("=" * 70)
    
    # Verificar estructura de archivos al inicio
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"📁 Directorio base: {base_dir}")
        
        # Verificar carpetas importantes
        folders_to_check = ['../vista', '../assent/css', '../js', '../img']
        
        for folder in folders_to_check:
            folder_path = os.path.join(base_dir, folder)
            folder_path = os.path.abspath(folder_path)
            
            if os.path.exists(folder_path):
                files_count = len(os.listdir(folder_path))
                print(f"✅ {folder}: {folder_path} ({files_count} archivos)")
            else:
                print(f"❌ {folder}: {folder_path} (NO EXISTE)")
        
        # Verificar específicamente los archivos del dashboard
        print("\n📊 Verificando archivos del dashboard:")
        dashboard_files = {
            'HTML': '../vista/dashboard-agricultor.html',
            'CSS': '../vista/styles.css',
            'JS': '../vista/script.js'
        }
        
        for file_type, file_path in dashboard_files.items():
            full_path = os.path.join(base_dir, file_path)
            full_path = os.path.abspath(full_path)
            
            if os.path.exists(full_path):
                print(f"✅ {file_type}: {full_path}")
            else:
                print(f"❌ {file_type}: {full_path} (NO EXISTE)")
        
    except Exception as e:
        print(f"⚠️ Error verificando estructura: {e}")
    
    print("\n" + "=" * 70)
    print("📍 URLs principales:")
    print("🧪 http://localhost:5000/test")
    print("🔍 http://localhost:5000/check_files")
    print("🔐 http://localhost:5000/check_session")
    print("✅ http://localhost:5000/validate_session")
    print("👤 http://localhost:5000/get_user_session")
    print("🏠 http://localhost:5000/")
    print("👷 http://localhost:5000/vista/login-trabajador.html")
    print("🌾 http://localhost:5000/vista/login-trabajador.html")
    print("📝 http://localhost:5000/vista/registro-trabajador.html")
    print("📝 http://localhost:5000/vista/registro-agricultor.html")
    print("\n🎯 NUEVO DASHBOARD SEPARADO:")
    print("🌱 http://localhost:5000/vista/dashboard-agricultor.html")
    print("📄 http://localhost:5000/styles.css")
    print("⚙️ http://localhost:5000/script.js")
    print("👷 http://localhost:5000/vista/index-trabajador.html")
    print("📄 http://localhost:5000/index-trabajador.css")
    print("⚙️ http://localhost:5000/index-trabajador.js")
    print("=" * 70)
    print("🔧 Funcionalidades del dashboard:")
    print("• Archivos HTML, CSS y JS separados")
    print("• Menú de usuario completo con dropdown")
    print("• Modal de confirmación para logout")
    print("• Integración completa con backend Python")
    print("• Validación de sesiones en tiempo real")
    print("• Responsive design")
    print("=" * 70)
    print("💡 Para probar:")
    print("1. Registra un usuario como 'Agricultor'")
    print("2. Inicia sesión")
    print("3. Accede al dashboard del agricultor")
    print("4. Prueba el menú de usuario (clic en avatar)")
    print("5. Prueba el logout con confirmación")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)