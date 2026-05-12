import os
import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)
# Seguridad: Debug en False para producción
app.config['DEBUG'] = False

@app.route('/')
def index():
    return "NovaCorp Platform - Entorno Seguro DevSecOps"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    # Remediación CWE-89: Uso de parámetros ?
    conn = sqlite3.connect('users.db')
    query = "SELECT * FROM users WHERE username = ?"
    user = conn.execute(query, (username,)).fetchone()
    conn.close()
    return "Intento de login procesado de forma segura."

if __name__ == '__main__':
    app.run()
