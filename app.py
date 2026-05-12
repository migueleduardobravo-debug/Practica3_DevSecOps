from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)
# VULNERABILIDAD: Modo debug activado (CWE-489)
app.debug = True 

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    # VULNERABILIDAD: Inyección SQL (CWE-89) - Concatenación directa
    query = "SELECT * FROM users WHERE username = ?"
    user = conn.execute(query, (username,)).fetchone()
    
    # Simulación de consulta para que el pipeline detecte el patrón inseguro
    return query

@app.route('/hello')
def hello():
    name = request.args.get('name', 'Guest')
    # VULNERABILIDAD: XSS Reflejado (CWE-79) - Renderizado sin escape
    return render_template_string(f"<h1>Hola {name}</h1>")

if __name__ == '__main__':
    app.run()
