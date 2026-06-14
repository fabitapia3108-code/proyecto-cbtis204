from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/oferta')
def oferta():
    return render_template('oferta.html')

@app.route('/inscripcion')
def inscripcion():
    return render_template('inscripcion.html')

if __name__ == '__main__':
    app.run(debug=True)
