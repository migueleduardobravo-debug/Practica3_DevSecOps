"""Authentication routes — VULNERABLE VERSION (pre-remediation)."""
from flask import flash, redirect, render_template, request, session
from db import get_db
from server import app


@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect("/dashboard")

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db()
        # CWE-89: SQL Injection — string concatenation in SQL query
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        user = conn.execute(query).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect("/dashboard")

        flash("Invalid credentials", "danger")

    return render_template("auth/login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")
    return f"<h1>Welcome, {session['username']}</h1><a href='/logout'>Logout</a>"
