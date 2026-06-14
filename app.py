from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- DISEÑO BASE (HTML/CSS) CON COLORES INSTITUCIONALES, REDES Y DIRECCIÓN REAL ---
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CBTis 204 - Sitio Oficial Promocional</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #f4f4f4; color: #333; line-height: 1.6; }
        
        /* Barra de Navegación (Negro y Guinda) */
        header { background-color: #111; color: #fff; padding: 15px 0; position: sticky; top: 0; z-index: 100; border-bottom: 4px solid #6A1B29; }
        .nav-container { width: 85%; margin: auto; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 24px; font-weight: bold; color: #fff; }
        .logo span { color: #6A1B29; }
        nav a { color: #ddd; text-decoration: none; margin-left: 20px; font-weight: 600; transition: 0.3s; padding: 5px 10px; border-radius: 4px; }
        nav a:hover, nav a.active { color: #fff; background-color: #6A1B29; }
        
        /* Secciones Principales */
        .container { width: 85%; margin: 30px auto; min-height: 65vh; }
        .card { background: #fff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 5px solid #6A1B29; margin-bottom: 30px; }
        
        h1, h2, h3 { color: #6A1B29; margin-bottom: 20px; }
        p { margin-bottom: 15px; font-size: 17px; text-align: justify; }
        
        /* Contenedor de Contacto */
        .contact-info { background-color: #f8f9fa; padding: 20px; border-radius: 6px; border: 1px solid #dee2e6; margin-top: 15px; }
        .contact-item { margin-bottom: 10px; font-size: 16px; }
        .contact-item strong { color: #111; }
        
        /* Estilos de Oferta Educativa */
        .grid-carreras { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }
        .carrera-card { background: #e9ecef; border: 1px solid #dee2e6; padding: 25px; border-radius: 6px; text-align: center; transition: 0.3s; }
        .carrera-card:hover { transform: translateY(-5px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); border-color: #6A1B29; }
        .carrera-card h3 { color: #111; margin-bottom: 10px; }
        .badge { background: #6A1B29; color: white; padding: 4px 10px; border-radius: 12px; font-size: 12px; display: inline-block; margin-top: 10px; }
        
        /* Formularios e Interactivos */
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select, textarea { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; }
        button { background-color: #6A1B29; color: white; border: none; padding: 12px 20px; border-radius: 4px; font-size: 16px; cursor: pointer; font-weight: bold; width: 100%; transition: 0.3s; }
        button:hover { background-color: #4A121A; }
        .resultado { background-color: #e2f0d9; color: #385723; padding: 20px; border-radius: 4px; margin-top: 15px; border-left: 4px solid #70ad47; }
        .resultado ul { margin-left: 20px; margin-top: 10px; }
        
        /* Pie de Página con Redes Sociales */
        footer { background-color: #111; color: #aaa; text-align: center; padding: 30px 0; margin-top: 40px; border-top: 4px solid #6A1B29; font-size: 14px; }
        .footer-content { width: 85%; margin: auto; display: flex; flex-direction: column; align-items: center; gap: 12px; }
        .social-links { display: flex; gap: 15px; margin-top: 5px; }
        .social-btn { background-color: #333; color: #fff; padding: 8px 18px; text-decoration: none; border-radius: 20px; font-weight: bold; font-size: 13px; transition: 0.3s; border: 1px solid #444; }
        .social-btn:hover { background-color: #6A1B29; border-color: #6A1B29; color: #fff; }
        .footer-text { margin: 2px 0; color: #888; }
    </style>
</head>
<body>

    <header>
        <div class="nav-container">
            <div class="logo">CBTis <span>204</span></div>
            <nav>
                <a href="/" class="{{ 'active' if page == 'inicio' else '' }}">Inicio</a>
                <a href="/nosotros" class="{{ 'active' if page == 'nosotros' else '' }}">Nosotros</a>
                <a href="/oferta" class="{{ 'active' if page == 'oferta' else '' }}">Oferta Educativa</a>
                <a href="/inscripcion" class="{{ 'active' if page == 'inscripcion' else '' }}">Inscripción</a>
            </nav>
        </div>
    </header>

    <div class="container">
        {% block content %}{% endblock %}
    </div>

    <footer>
        <div class="footer-content">
            <div class="social-links">
                <a href="https://www.facebook.com/Cbtis204/" target="_blank" class="social-btn">📘 Facebook Oficial</a>
                <a href="https://uemstis.sep.gob.mx/" target="_blank" class="social-btn">🌐 Portal UEMSTIS</a>
            </div>
            <p class="footer-text" style="color: #bbb; margin-top: 5px;">📍 Km 39 carr. Maravatio-Tlalpujahua, Tlalpujahua de Rayón, México, CP 61060</p>
            <p class="footer-text">📞 Teléfono: 711 158 0213 | ✉️ Correo: cbtis204.subdir@dgeti.sems.gob.mx</p>
            <p class="footer-text" style="margin-top: 10px; font-size: 12px;">&copy; 2026 CBTis 204. Desarrollado para el Proyecto Escolar. Todos los derechos reservados.</p>
        </div>
    </footer>

</body>
</html>
"""

# --- RUTA 1: INICIO (BIENVENIDA E INTRODUCCIÓN) ---
@app.route('/')
def inicio():
    content = """
    <div class="card">
        <h1>¡Bienvenidos al Sitio Oficial del CBTis 204!</h1>
        <p>Es un honor darles la más cordial bienvenida a nuestra plataforma digital informativa. El Centro de Bachillerato Tecnológico industrial y de servicios No. 204 es una institución comprometida firmemente con la excelencia académica, la innovación tecnológica y la formación integral de nuestros jóvenes estudiantes.</p>
        <p>Aquí encontrarás toda la información relevante sobre nuestro plantel, los procesos de nuevo ingreso, y las herramientas necesarias para conocer de cerca el gran futuro profesional que te espera dentro de nuestra comunidad escolar.</p>
        
        <div class="contact-info">
            <h3>📍 Información de Contacto y Ubicación</h3>
            <div class="contact-item"><strong>Plantel:</strong> Centro de Bachillerato Tecnológico industrial y de servicios No. 204 (CBTis 204)</div>
            <div class="contact-item"><strong>Dirección:</strong> Km 39 carr. Maravatio-Tlalpujahua, Tlalpujahua de Rayón, México, CP 61060</div>
            <div class="contact-item"><strong>Teléfono:</strong> 711 158 0213</div>
            <div class="contact-item"><strong>Correo Institucional:</strong> cbtis204.subdir@dgeti.sems.gob.mx</div>
        </div>
    </div>
    
    <div class="card" style="border-left-color: #333;">
        <h2>Buzón de Dudas para Alumnos y Padres</h2>
        <form action="/contacto" method="POST">
            <div class="form-group">
                <label>Nombre Completo:</label>
                <input type="text" name="nombre" placeholder="Ej. Juan Pérez" required>
            </div>
            <div class="form-group">
                <label>Correo Electrónico:</label>
                <input type="email" name="correo" placeholder="ejemplo@correo.com" required>
            </div>
            <div class="form-group">
                <label>Escribe tu duda o comentario:</label>
                <textarea name="mensaje" rows="4" placeholder="¿En qué podemos ayudarte?" required></textarea>
            </div>
            <button type="submit">Enviar Mensaje</button>
        </form>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, content=content, page='inicio')

# --- RUTA DE CONTACTO (PROCESAR FORMULARIO) ---
@app.route('/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre')
    content = f"""
    <div class="card">
        <h1>¡Mensaje Recibido con Éxito!</h1>
        <div class="resultado" style="background-color: #d4edda; color: #155724; border-left-color: #28a745;">
            Gracias por escribirnos, <strong>{nombre}</strong>. Tu duda ha sido registrada en el sistema escolar de manera exitosa. Nos pondremos en contacto contigo muy pronto a través del correo proporcionado.
        </div>
        <br>
        <a href="/" style="display:inline-block; background:#111; color:white; padding:10px 20px; text-decoration:none; border-radius:4px; font-weight:bold;">Volver al Inicio</a>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, content=content, page='inicio')

# --- RUTA 2: NOSOTROS (MISIÓN Y VISIÓN) ---
@app.route('/nosotros')
def nosotros():
    content = """
    <div class="card">
        <h1>Nuestra Identidad Institucional</h1>
        <p>En el CBTis 204 trabajamos día con día bajo firmes valores éticos y profesionales para guiar a las nuevas generaciones hacia el éxito en el campo laboral y académico superior.</p>
    </div>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div class="card" style="margin-bottom: 0;">
            <h2>🎯 Misión</h2>
            <p>Formar personas con conocimientos tecnológicos en las áreas industrial, comercial y de servicios a través de la preparación de bachilleres y profesionales tecnológicos, con el fin de contribuir al desarrollo del país.</p>
        </div>
        <div class="card" style="margin-bottom: 0; border-left-color: #333;">
            <h2>👁️ Visión</h2>
            <p>Ser una institución de educación media superior certificada, orientada al aprendizaje y desarrollo de conocimientos tecnológicos y humanistas.</p>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, content=content, page='nosotros')

# --- RUTA 3: OFERTA EDUCATIVA (CARRERAS TÉCNICAS) ---
@app.route('/oferta')
def oferta():
    content = """
    <div class="card">
        <h1>Oferta Educativa</h1>
        <p>Te ofrecemos carreras técnicas profesionales con alta demanda en el sector productivo actual. Al egresar, obtendrás tu Certificado de Bachillerato y tu Título y Cédula Profesional Técnica.</p>
        
        <div class="grid-carreras">
            <div class="carrera-card">
                <h3>Técnico en Ofimática</h3>
                <p>Aprende a gestionar sistemas de archivos digitales, diseñar documentos avanzados y administrar software de oficina.</p>
                <span class="badge">Área Comercial y Servicios</span>
            </div>
            <div class="carrera-card">
                <h3>Técnico en Contabilidad</h3>
                <p>Domina el registro de operaciones financieras, cálculo de impuestos y auditoría administrativa empresarial.</p>
                <span class="badge">Área Comercial</span>
            </div>
            <div class="carrera-card">
                <h3>Técnico en Electrónica</h3>
                <p>Especialízate en el diseño, mantenimiento y reparación de circuitos, sistemas eléctricos y automatización.</p>
                <span class="badge">Área Industrial</span>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, content=content, page='oferta')

# --- RUTA 4: ASISTENTE INTERACTIVO DE INSCRIPCIÓN (NUEVA LÓGICA DE BACKEND) ---
@app.route('/inscripcion', methods=['GET', 'POST'])
def inscripcion():
    resultado_html = None
    if request.method == 'POST':
        nombre_alumno = request.form.get('nombre_alumno')
        tipo_secundaria = request.form.get('tipo_secundaria')
        carrera_interes = request.form.get('carrera_interes')
        
        # Lógica de Python para armar la respuesta adaptada al proceso real
        documentos = [
            "Acta de Nacimiento (Original y 2 copias)",
            "Clave Única de Registro de Población (CURP) certificada",
            "6 Fotografías tamaño infantil (Blanco y negro, papel mate)",
            "Constancia de estudios o Certificado de Secundaria original"
        ]
        
        # Agregar requisitos especiales usando condiciones válidas de programación backend
        if tipo_secundaria == "privada":
            documentos.append("Copia de la clave de incorporación de la secundaria de procedencia.")
        else:
            documentos.append("Copia de la boleta del último grado de la secundaria pública.")
            
        # Generar salida estructurada
        resultado_html = f"""
        <div class="resultado">
            <h2 style="color: #276a1c;">¡Lugar Asegurado para el ciclo escolar!</h2>
            <p>Estimado(a) <strong>{nombre_alumno}</strong>, en el CBTis 204 el ingreso es directo mediante tu proceso de registro. Tu espacio en la especialidad de <strong>{carrera_interes}</strong> está disponible.</p>
            <p><strong>Por favor, acude al plantel con los siguientes documentos para formalizar tu inscripción:</strong></p>
            <ul>
        """
        for doc in documentos:
            resultado_html += f"<li>{doc}</li>"
            
        resultado_html += """
            </ul>
            <p style="margin-top: 15px; font-size: 14px; color: #555;">* El horario de recepción de documentos en las ventanillas de Control Escolar es de 8:00 AM a 2:00 PM.</p>
        </div>
        """

    content = f"""
    <div class="card">
        <h1>Asistente de Inscripción Directa</h1>
        <p>En nuestra institución tu educación está garantizada. Utiliza este asistente interactivo para registrar tus datos de procedencia y generar la lista oficial de requisitos para tu inscripción inmediata.</p>
        <br>
        <form action="/inscripcion" method="POST">
            <div class="form-group">
                <label>Nombre Completo del Aspirante:</label>
                <input type="text" name="nombre_alumno" placeholder="Nombre completo" required>
            </div>
            <div class="form-group">
                <label>Secundaria de Procedencia:</label>
                <select name="tipo_secundaria" required>
                    <option value="publica">Secundaria Pública (General / Técnica / Telesecundaria)</option>
                    <option value="privada">Secundaria Privada (Colegio Particular)</option>
                </select>
            </div>
            <div class="form-group">
                <label>Especialidad Técnica de Interés:</label>
                <select name="carrera_interes" required>
                    <option value="Técnico en Ofimática">Técnico en Ofimática</option>
                    <option value="Técnico en Contabilidad">Técnico en Contabilidad</option>
                    <option value="Técnico en Electrónica">Técnico en Electrónica</option>
                </select>
            </div>
            <button type="submit">Generar Requisitos de Inscripción</button>
        </form>
        
        { resultado_html if resultado_html else '' }
    </div>
    """
    return render_template_string(BASE_TEMPLATE, content=content, page='inscripcion')

if __name__ == '__main__':
    app.run(debug=True)
