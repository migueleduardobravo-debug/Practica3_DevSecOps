"""Admin routes for user management."""
from flask import flash, redirect, render_template, request, session

from db import get_data_connection, get_users_connection, hash_password
from server import app


ALLOWED_ROLES = {"user", "owner", "admin"}


def _validated_role(value):
    """Return `value` only if it is a known role, otherwise None."""
    if value in ALLOWED_ROLES:
        return value
    return None


@app.route("/admin/users")
def admin_users():
    if session.get("role") != "admin":
        return render_template("errors/403.html"), 403
    conn_u = get_users_connection()
    try:
        users = conn_u.execute("SELECT * FROM users").fetchall()
    finally:
        conn_u.close()

    conn_d = get_data_connection()
    try:
        companies = conn_d.execute("SELECT * FROM companies").fetchall()
    finally:
        conn_d.close()

    return render_template("admin/admin_users.html", users=users, companies=companies)


@app.route("/admin/users/add", methods=["POST"])
def add_user():
    if session.get("role") != "admin":
        return render_template("errors/403.html"), 403

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    role = _validated_role(request.form.get("role"))

    if not username or not password or role is None:
        flash("Invalid user data.", "danger")
        return redirect("/admin/users")

    company_id = None
    if role == "owner":
        try:
            company_id = int(request.form.get("company_id", ""))
        except (TypeError, ValueError):
            flash("Owner role requires a valid company.", "warning")
            return redirect("/admin/users")

    conn = get_users_connection()
    try:
        if company_id is not None:
            conn.execute(
                "INSERT INTO users (username, password, role, company_id) "
                "VALUES (?, ?, ?, ?)",
                (username, hash_password(password), role, company_id),
            )
        else:
            conn.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hash_password(password), role),
            )
        conn.commit()
    finally:
        conn.close()
    flash("User created successfully.", "success")
    return redirect("/admin/users")


@app.route("/admin/users/edit", methods=["POST"])
def edit_user():
    if session.get("role") != "admin":
        return render_template("errors/403.html"), 403

    username = request.form.get("username", "").strip()
    new_role = _validated_role(request.form.get("role"))
    if not username or new_role is None:
        flash("Invalid edit request.", "danger")
        return redirect("/admin/users")

    company_id = None
    if new_role == "owner":
        try:
            company_id = int(request.form.get("company_id", ""))
        except (TypeError, ValueError):
            flash("Owner role requires a valid company.", "warning")
            return redirect("/admin/users")

    conn = get_users_connection()
    try:
        if company_id is not None:
            conn.execute(
                "UPDATE users SET role = ?, company_id = ? WHERE username = ?",
                (new_role, company_id, username),
            )
        else:
            conn.execute(
                "UPDATE users SET role = ?, company_id = NULL WHERE username = ?",
                (new_role, username),
            )
        conn.commit()
    finally:
        conn.close()
    flash("User updated.", "success")
    return redirect("/admin/users")


@app.route("/admin/users/delete", methods=["POST"])
def delete_user():
    if session.get("role") != "admin":
        return render_template("errors/403.html"), 403
    username = request.form.get("username", "").strip()
    if not username:
        flash("Invalid delete request.", "danger")
        return redirect("/admin/users")
    if username == session.get("username"):
        flash("You cannot delete your own account while logged in.", "warning")
        return redirect("/admin/users")
    conn = get_users_connection()
    try:
        conn.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
    finally:
        conn.close()
    flash("User deleted.", "warning")
    return redirect("/admin/users")
