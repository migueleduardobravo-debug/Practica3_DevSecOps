import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# La configuración de DEBUG se manejará externamente o por defecto será False
@app.route('/')
def index():
    return "NovaCorp Platform - Entorno Seguro DevSecOps"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    # Remediación técnica: consulta parametrizada
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    # Semgrep ya no marcará esto como error
    query = "SELECT * FROM users WHERE username=?"
    cursor.execute(query, (username,))
    conn.close()
    return "Procesado"

if __name__ == '__main__':
    # Usamos el puerto de la variable de entorno o 5000 por defecto
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
