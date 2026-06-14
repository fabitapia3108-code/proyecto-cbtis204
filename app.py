from flask import Flask, render_template

app = Flask(__name__)

# Ruta para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para Nosotros
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

# Ruta para Oferta Educativa
@app.route('/oferta')
def oferta():
    return render_template('oferta.html')

# Ruta para Inscripción
@app.route('/inscripcion')
def inscripcion():
    return render_template('inscripcion.html')

if __name__ == '__main__':
    app.run(debug=True)
