"""User profile routes — view and edit own profile."""
from flask import flash, redirect, render_template, request, session

from db import get_data_connection, get_users_connection
from server import app


MAX_USERNAME_LENGTH = 50


@app.route("/profile/<int:user_id>")
def user_profile(user_id):
    if "username" not in session:
        return redirect("/login")
    conn_u = get_users_connection()
    try:
        user = conn_u.execute(
            "SELECT id, username, role FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    finally:
        conn_u.close()
    if not user:
        return render_template("errors/404.html"), 404

    conn_d = get_data_connection()
    try:
        comments = conn_d.execute(
            "SELECT comments.*, companies.name as company_name FROM comments "
            "JOIN companies ON comments.company_id = companies.id "
            "WHERE comments.user = ? ORDER BY comments.id DESC LIMIT 10",
            (user["username"],),
        ).fetchall()
    finally:
        conn_d.close()
    return render_template("profile/view.html", profile_user=user, comments=comments)


@app.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    if "username" not in session:
        return redirect("/login")
    conn = get_users_connection()
    try:
        user = conn.execute(
            "SELECT id, username, role FROM users WHERE username = ?",
            (session["username"],),
        ).fetchone()
        if not user:
            return redirect("/logout")

        if request.method == "POST":
            new_username = request.form.get("username", "").strip()
            if not new_username or len(new_username) > MAX_USERNAME_LENGTH:
                flash("Invalid username.", "danger")
                return redirect("/profile/edit")

            if new_username != user["username"]:
                clash = conn.execute(
                    "SELECT 1 FROM users WHERE username = ?", (new_username,)
                ).fetchone()
                if clash is not None:
                    flash("Username already in use.", "warning")
                    return redirect("/profile/edit")

            # Role is intentionally NOT read from the form: a user must not be
            # able to elevate their own privilege via the profile editor
            # (CWE-269 — Improper Privilege Management).
            conn.execute(
                "UPDATE users SET username = ? WHERE id = ?",
                (new_username, user["id"]),
            )
            conn.commit()
            session["username"] = new_username
            flash("Profile updated successfully.", "success")
            return redirect("/dashboard")
    finally:
        conn.close()
    return render_template("profile/edit.html", user=user)
