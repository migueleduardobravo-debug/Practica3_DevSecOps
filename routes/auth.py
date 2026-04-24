from db import get_users_connection, hash_password
from flask import request, redirect, render_template, session, flash
from server import app
from urllib.parse import urlparse

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/dashboard')

    next_url = request.args.get('next') or '/dashboard'

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_users_connection()
        # Remediación SQLi con placeholders
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        user = conn.execute(query, (username, hash_password(password))).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(next_url)
        else:
            flash("Invalid credentials", "danger")
    
    return render_template('auth/login.html', next_url=next_url)
