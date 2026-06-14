from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Base de datos temporal para guardar las dudas de los interesados
prospectos = [
    {"nombre": "Diana Martínez", "mensaje": "¿Tienen turno vespertino para la carrera de Ofimática?"},
    {"nombre": "Kevin Torres", "mensaje": "¿Cuáles son los requisitos para la preinscripción?"}
]

# Diseño Visual enfocado en Promoción Institucional (HTML + CSS + JS Puro)
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admisiones 2026 - CBTis 204</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #f7f9fc; color: #333; }
        header { background-color: #800020; color: white; padding: 30px 20px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.15); }
        header h1 { font-size: 28px; margin-bottom: 5px; letter-spacing: 1px; }
        header p { font-size: 16px; opacity: 0.9; }
        .container { max-width: 850px; margin: 30px auto; padding: 0 20px; }
        .card { background: white; padding: 25px; margin-bottom: 25px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        h2 { color: #800020; margin-bottom: 15px; border-bottom: 2px solid #800020; padding-bottom: 5px; font-size: 20px; }
        p { line-height: 1.6; margin-bottom: 10px; }
        
        /* Lista de Carreras */
        .carreras-list { list-style: none; margin-top: 10px; }
        .carreras-list li { background: #f1f5f9; padding: 10px 15px; margin-bottom: 8px; border-left: 5px solid #b38f4f; border-radius: 4px; font-weight: 500; }
        
        /* Formulario e Interactividad */
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
        input[type="text"], input[type="number"], textarea, select { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 6px; font-size: 15px; }
        button { background-color: #800020; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; font-size: 16px; width: 100%; font-weight: bold; transition: background 0.3s; }
        button:hover { background-color: #5a0016; }
        
        /* Diagnóstico */
        #resultadoTest { margin-top: 15px; padding: 15px; border-radius: 6px; display: none; text-align: center; font-weight: bold; line-height: 1.5; }
        .perfil-alto { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .perfil-medio { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
        
        /* Mensajes */
        .comentario-item { background: #f8f9fa; padding: 12px; margin-bottom: 12px; border-left: 4px solid #800020; border-radius: 6px; }
        .comentario-item strong { color: #800020; display: block; margin-bottom: 3px; }
        footer { text-align: center; padding: 25px; color: #666; font-size: 14px; margin-top: 40px; border-top: 1px solid #e2e8f0; }
    </style>
</head>
<body>

    <header>
        <h1>¡Únete al CBTis 204!</h1>
        <p>Tu futuro profesional comienza aquí | Portal Oficial de Admisiones e Informes</p>
    </header>

    <div class="container">
        <div class="card">
            <h2>¿Por qué elegir el CBTis 204?</h2>
            <p>Somos una institución de educación media superior comprometida con la excelencia académica y tecnológica. Ofrecemos bachillerato técnico que te prepara para trabajar o continuar tus estudios universitarios.</p>
            <h3 style="margin: 15px 0 10px 0; color: #b38f4f;">Nuestras Carreras Técnicas:</h3>
            <ul class="carreras-list">
                <li>💻 Técnico en Ofimática (Gestión y Sistemas Interconectados)</li>
                <li>🛠️ Técnico en Mantenimiento Industrial</li>
                <li>📊 Técnico en Contabilidad</li>
            </ul>
        </div>

        <div class="card">
            <h2>Simulador de Perfil Técnico</h2>
            <p style="font-size: 14px; color: #666; margin-bottom: 15px;">¿Te interesa la tecnología o la administración? Selecciona tu nivel de interés para ver si la carrera de Ofimática es ideal para ti.</p>
            <div class="form-group">
                <label for="interesComputo">¿Qué tanto te gusta usar computadoras y software? (1 al 10):</label>
                <input type="number" id="interesComputo" min="1" max="10" placeholder="Ej. 9">
            </div>
            <div class="form-group">
                <label for="interesAdmin">¿Te interesa la organización de oficinas y proyectos? (1 al 10):</label>
                <input type="number" id="interesAdmin" min="1" max="10" placeholder="Ej. 8">
            </div>
            <button onclick="evaluarPerfil()">Verificar mi Afinidad</button>
            <div id="resultadoTest"></div>
        </div>

        <div class="card">
            <h2>Módulo de Atención y Dudas</h2>
            <p style="font-size: 14px; color: #666; margin-bottom: 15px;">¿Tienes dudas sobre los costos, fichas o planteles? Déjanos tu pregunta y nuestro director de proyecto te responderá en breve.</p>
            <form id="formProspecto">
                <div class="form-group">
                    <label for="nombre">Nombre Completo del Aspirante:</label>
                    <input type="text" id="nombre" required placeholder="Ej. Carlos González">
                </div>
                <div class="form-group">
                    <label for="mensaje">¿Cuál es tu duda o comentario?:</label>
                    <textarea id="mensaje" rows="3" required placeholder="Escribe aquí tu pregunta detallada..."></textarea>
                </div>
                <button type="submit">Enviar Pregunta al Plantel</button>
            </form>

            <h3 style="margin-top: 25px; margin-bottom: 12px; color: #444; font-size: 16px;">Preguntas Frecuentes de la Comunidad:</h3>
            <div id="listaDudas">
                {% for p in prospectos %}
                <div class="comentario-item">
                    <strong>Aspirante: {{ p.nombre }}</strong>
                    <span>{{ p.mensaje }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <footer>
        <p>&copy; 2026 CBTis 204 - Especialidad de Ofimática</p>
        <p style="font-size: 11px; margin-top: 5px; color: #999;">Proyecto Escolar de Interconexión de Servicios en la Nube desarrollado para el Profe Abner.</p>
    </footer>

    <script>
        // Lógica interactiva con JavaScript Puro
        function evaluarPerfil() {
            const comp = parseInt(document.getElementById('interesComputo').value);
            const admin = parseInt(document.getElementById('interesAdmin').value);
            
            if (isNaN(comp) || isNaN(admin) || comp < 1 || comp > 10 || admin < 1 || admin > 10) {
                alert('Por favor, ingresa números válidos entre 1 y 10.');
                return;
            }
            
            const promedio = (comp + admin) / 2;
            const resDiv = document.getElementById('resultadoTest');
            resDiv.style.display = 'block';
            
            if (promedio >= 7.0) {
                resDiv.className = 'perfil-alto';
                resDiv.innerHTML = '¡Excelente Perfil! Tienes una afinidad del ' + (promedio*10) + '% con la carrera de Ofimática. ¡Te esperamos en el CBTis 204!';
            } else {
                resDiv.className = 'perfil-medio';
                resDiv.innerHTML = 'Perfil General: Tienes habilidades útiles para cualquiera de nuestros bachilleratos técnicos. ¡Acepta el reto!';
            }
        }

        // Conexión dinámica con el backend en Python (Flask)
        document.getElementById('formProspecto').addEventListener('submit', async function(e) {
            e.preventDefault();
            const nombre = document.getElementById('nombre').value;
            const mensaje = document.getElementById('mensaje').value;

            const response = await fetch('/api/prospecto', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre, mensaje })
            });

            if (response.ok) {
                const data = await response.json();
                document.getElementById('nombre').value = '';
                document.getElementById('mensaje').value = '';
                
                const lista = document.getElementById('listaDudas');
                lista.innerHTML = '';
                data.forEach(p => {
                    const div = document.createElement('div');
                    div.className = 'comentario-item';
                    div.innerHTML = `<strong>Aspirante: \${p.nombre}</strong><span>\${p.mensaje}</span>`;
                    lista.appendChild(div);
                });
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT, prospectos=prospectos)

@app.route('/api/prospecto', methods=['POST'])
def agregar_prospecto():
    data = request.get_json()
    if data and 'nombre' in data and 'mensaje' in data:
        prospectos.insert(0, data)
    return jsonify(prospectos)

if __name__ == '__main__':
    app.run(debug=True)
