from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Esta es tu página de inicio con bienvenida e intro
    return render_template('index.html')

@app.route('/acerca-de')
def acerca_de():
    return render_template('acerca.html')

@app.route('/oferta-educativa')
def oferta():
    return render_template('oferta.html')

@app.route('/inscripcion')
def inscripcion():
    return render_template('inscripcion.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/aviso-privacidad')
def aviso():
    return render_template('aviso.html')
