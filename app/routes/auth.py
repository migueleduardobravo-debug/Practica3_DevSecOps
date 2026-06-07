"""Authentication routes — login/logout."""
from urllib.parse import urlparse

from flask import flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash

from db import get_users_connection
from server import app


def _safe_next_url(candidate):
    """Return `candidate` only if it is a relative URL pointing to our own host.

    Mitigates CWE-601 (Open Redirect). Any value containing scheme or netloc is
    rejected; only paths beginning with a single forward slash are accepted.
    """
    if not candidate:
        return "/dashboard"
    parsed = urlparse(candidate)
    if parsed.scheme or parsed.netloc:
        return "/dashboard"
    if not candidate.startswith("/") or candidate.startswith("//"):
        return "/dashboard"
    return candidate


@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect("/dashboard")

    next_url = _safe_next_url(request.args.get("next") or request.form.get("next"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        submitted_password = request.form.get("password", "")

        conn = get_users_connection()
        try:
            user = conn.execute(
                "SELECT id, username, password, role, company_id "
                "FROM users WHERE username = ?",
                (username,),
            ).fetchone()
        finally:
            conn.close()

        if user and check_password_hash(user["password"], submitted_password):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            session["company_id"] = user["company_id"]
            session.permanent = True
            return redirect(next_url)

        flash("Invalid username or password", "danger")
        return render_template("auth/login.html", next_url=next_url)

    return render_template("auth/login.html", next_url=next_url)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect("/login")
