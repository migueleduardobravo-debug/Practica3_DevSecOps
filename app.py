import os
from flask import Flask, render_template

app = Flask(__name__)
# Seguridad: Clave secreta desde variable de entorno para DevSecOps
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_only')

@app.route('/')
def index():
    return "NovaCorp Platform - Entorno Seguro DevSecOps"

if __name__ == '__main__':
    # Seguridad: Debug False en producción
    app.run(debug=False)
