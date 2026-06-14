from flask import Flask, render_template

app = Flask(__name__)

# Esta es la ruta principal (Home)
@app.route('/')
def home():
    return render_template('index.html')

# Esto es lo que le permite a tu computadora ejecutar la página
if __name__ == '__main__':
    app.run(debug=True)
