from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Base de datos temporal en memoria para los comentarios de los alumnos
comentarios = [
    {"nombre": "Ana López", "mensaje": "¡Me encanta el nuevo diseño de la página!"},
    {"nombre": "Carlos Gómez", "mensaje": "¿Saben cuándo se entregan las boletas del segundo parcial?"}
]

# Diseño Visual integrado (HTML + CSS + JS)
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal Informativo - CBTis 204</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #f4f6f9; color: #333; }
        header { background-color: #800020; color: white; padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        header h1 { margin-bottom: 5px; font-size: 24px; }
        .container { max-width: 800px; margin: 30px auto; padding: 0 20px; }
        .card { background: white; padding: 20px; margin-bottom: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        h2 { color: #800020; margin-bottom: 15px; border-bottom: 2px solid #f4f6f9; padding-bottom: 5px; }
        
        /* Formulario y Herramienta */
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"], input[type="number"], textarea { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
        button { background-color: #800020; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; font-size: 16px; width: 100%; }
        button:hover { background-color: #5a0016; }
        
        /* Resultado */
        #resultado { margin-top: 15px; padding: 15px; border-radius: 4px; display: none; font-weight: bold; text-align: center; }
        .aprobado { background-color: #d4edda; color: #155724; }
        .reprobado { background-color: #f8d7da; color: #721c24; }
        
        /* Comentarios */
        .comentario-item { background: #f8f9fa; padding: 10px; margin-bottom: 10px; border-left: 4px solid #800020; border-radius: 4px; }
        .comentario-item strong { color: #800020; }
        footer { text-align: center; padding: 20px; color: #777; font-size: 14px; margin-top: 4px; }
    </style>
</head>
<body>

    <header>
        <h1>CONALEP / CBTis 204</h1>
        <p>Plataforma Web Interconectada - Control de Ofimática</p>
    </header>

    <div class="container">
        <div class="card">
            <h2>Bienvenidos al Portal Escolar</h2>
            <p>Esta plataforma ha sido diseñada utilizando Inteligencia Artificial como programador backend y el estudiante de Ofimática como Director de Proyecto. Conecta servicios web en la nube para mantener una disponibilidad de 24/7.</p>
        </div>

        <div class="card">
            <h2>Simulador de Estatus de Materia</h2>
            <div class="form-group">
                <label for="parcial1">Calificación Parcial 1:</label>
                <input type="number" id="parcial1" min="0" max="10" step="0.1" placeholder="Ej. 8.5">
            </div>
            <div class="form-group">
                <label for="parcial2">Calificación Parcial 2:</label>
                <input type="number" id="parcial2" min="0" max="10" step="0.1" placeholder="Ej. 7.0">
            </div>
            <div class="form-group">
                <label for="parcial3">Calificación Parcial 3:</label>
                <input type="number" id="parcial3" min="0" max="10" step="0.1" placeholder="Ej. 6.5">
            </div>
            <button onclick="calcularPromedio()">Calcular Estatus Final</button>
            <div id="resultado"></div>
        </div>

        <div class="card">
            <h2>Muro de Avisos y Sugerencias</h2>
            <form id="formComentario">
                <div class="form-group">
                    <label for="nombre">Tu Nombre:</label>
                    <input type="text" id="nombre" required placeholder="Ej. Juan Pérez">
                </div>
                <div class="form-group">
                    <label for="mensaje">Mensaje o Sugerencia:</label>
                    <textarea id="mensaje" rows="3" required placeholder="Escribe aquí tu duda o aportación para el CBTis..."></textarea>
                </div>
                <button type="submit">Publicar en el Muro</button>
            </form>

            <h3 style="margin-top: 20px; margin-bottom: 10px; color: #555;">Mensajes Recientes:</h3>
            <div id="listaComentarios">
                {% for c in comentarios %}
                <div class="comentario-item">
                    <strong>{{ c.nombre }}:</strong> {{ c.mensaje }}
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <footer>
        <p>&copy; 2026 CBTis 204 - Desarrollado en la Especialidad de Ofimática</p>
    </footer>

    <script>
        // Lógica interactiva con JavaScript Puro
        function calcularPromedio() {
            const p1 = parseFloat(document.getElementById('parcial1').value);
            const p2 = parseFloat(document.getElementById('parcial2').value);
            const p3 = parseFloat(document.getElementById('parcial3').value);
            
            if (isNaN(p1) || isNaN(p2) || isNaN(p3)) {
                alert('Por favor, ingresa las tres calificaciones.');
                return;
            }
            
            const promedio = (p1 + p2 + p3) / 3;
            const resDiv = document.getElementById('resultado');
            resDiv.style.display = 'block';
            
            if (promedio >= 6.0) {
                resDiv.className = 'aprobado';
                resDiv.innerHTML = '¡Aprobado! Tu promedio estimado es: ' + promedio.toFixed(1);
            } else {
                resDiv.className = 'reprobado';
                resDiv.innerHTML = 'Reprobado (Requiere Asesoría). Tu promedio estimado es: ' + promedio.toFixed(1);
            }
        }

        // Manejo del formulario para conectar con el backend en Python
        document.getElementById('formComentario').addEventListener('submit', async function(e) {
            e.preventDefault();
            const nombre = document.getElementById('nombre').value;
            const mensaje = document.getElementById('mensaje').value;

            const response = await fetch('/api/comentario', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombre, mensaje })
            });

            if (response.ok) {
                const data = await response.json();
                // Limpiar formulario
                document.getElementById('nombre').value = '';
                document.getElementById('mensaje').value = '';
                
                // Actualizar la lista en pantalla dinámicamente
                const lista = document.getElementById('listaComentarios');
                lista.innerHTML = '';
                data.forEach(c => {
                    const div = document.createElement('div');
                    div.className = 'comentario-item';
                    div.innerHTML = `<strong>\${c.nombre}:</strong> \${c.mensaje}`;
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
    return render_template_string(HTML_LAYOUT, comentarios=comentarios)

@app.route('/api/comentario', methods=['POST'])
def agregar_comentario():
    data = request.get_json()
    if data and 'nombre' in data and 'mensaje' in data:
        comentarios.insert(0, data) # Agrega el nuevo comentario al inicio
    return jsonify(comentarios)

if __name__ == '__main__':
    app.run(debug=True)
