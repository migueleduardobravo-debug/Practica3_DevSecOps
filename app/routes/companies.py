"""Public company and comment routes."""
from flask import flash, redirect, render_template, request, session

from db import get_data_connection, get_users_connection
from server import app


@app.route("/")
def index():
    return redirect("/login")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")
    conn = get_data_connection()
    try:
        total_companies = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
        total_comments = conn.execute("SELECT COUNT(*) FROM comments").fetchone()[0]
        recent_comments = conn.execute(
            "SELECT comments.*, companies.name as company_name FROM comments "
            "JOIN companies ON comments.company_id = companies.id "
            "ORDER BY comments.id DESC LIMIT 5"
        ).fetchall()
    finally:
        conn.close()

    user_ids = {}
    usernames = {c["user"] for c in recent_comments}
    if usernames:
        conn_u = get_users_connection()
        try:
            for uname in usernames:
                u = conn_u.execute(
                    "SELECT id FROM users WHERE username = ?", (uname,)
                ).fetchone()
                if u:
                    user_ids[uname] = u["id"]
        finally:
            conn_u.close()

    return render_template(
        "dashboard.html",
        total_companies=total_companies,
        total_comments=total_comments,
        recent_comments=recent_comments,
        user_ids=user_ids,
    )


@app.route("/companies")
def list_companies():
    if "username" not in session:
        return redirect("/login")
    conn = get_data_connection()
    try:
        search = request.args.get("q", "").strip()
        if search:
            # Parameterised LIKE — wildcards live in the parameter, not the SQL.
            companies = conn.execute(
                "SELECT * FROM companies WHERE name LIKE ?",
                (f"%{search}%",),
            ).fetchall()
        else:
            companies = conn.execute("SELECT * FROM companies").fetchall()

        companies_list = []
        for company in companies:
            row = dict(company)
            row["comment_count"] = conn.execute(
                "SELECT COUNT(*) FROM comments WHERE company_id = ?", (row["id"],)
            ).fetchone()[0]
            companies_list.append(row)
    finally:
        conn.close()
    return render_template("companies/home.html", companies=companies_list, search=search)


@app.route("/companies/<int:company_id>", methods=["GET", "POST"])
def company_detail(company_id):
    if "username" not in session:
        return redirect("/login")

    conn = get_data_connection()
    try:
        company = conn.execute(
            "SELECT * FROM companies WHERE id = ?", (company_id,)
        ).fetchone()

        if not company:
            return render_template("errors/404.html"), 404

        if request.method == "POST":
            comment = request.form.get("comment", "").strip()
            if not comment:
                flash("Comment cannot be empty.", "warning")
                return redirect(f"/companies/{company_id}")
            if len(comment) > 2000:
                flash("Comment exceeds the 2000 character limit.", "warning")
                return redirect(f"/companies/{company_id}")
            # Trust the session username, never the client-supplied value.
            user = session.get("username")
            conn.execute(
                "INSERT INTO comments (company_id, user, comment) VALUES (?, ?, ?)",
                (company_id, user, comment),
            )
            conn.commit()
            flash("Comment added successfully.", "success")
            return redirect(f"/companies/{company_id}")

        comments = conn.execute(
            "SELECT * FROM comments WHERE company_id = ?", (company_id,)
        ).fetchall()
    finally:
        conn.close()

    user_ids = {}
    usernames = {c["user"] for c in comments}
    if usernames:
        conn_u = get_users_connection()
        try:
            for uname in usernames:
                u = conn_u.execute(
                    "SELECT id FROM users WHERE username = ?", (uname,)
                ).fetchone()
                if u:
                    user_ids[uname] = u["id"]
        finally:
            conn_u.close()

    return render_template(
        "companies/company.html",
        company=company,
        comments=comments,
        user_ids=user_ids,
    )


@app.route("/companies/register", methods=["GET", "POST"])
def register_company():
    if session.get("role") != "admin":
        return render_template("errors/403.html"), 403
    if request.method == "POST":
        company_name = request.form.get("company_name", "").strip()
        description = request.form.get("description", "").strip()
        owner = request.form.get("owner", session.get("username")).strip()
        if not company_name:
            flash("Company name is required.", "warning")
            return redirect("/companies/register")
        conn = get_data_connection()
        try:
            conn.execute(
                "INSERT INTO companies (name, description, owner) VALUES (?, ?, ?)",
                (company_name, description, owner),
            )
            conn.commit()
        finally:
            conn.close()
        flash("Company registered successfully.", "success")
        return redirect("/companies")
    return render_template("companies/register_company.html")


@app.route("/companies/<int:company_id>/edit", methods=["GET", "POST"])
def edit_company(company_id):
    if "username" not in session:
        return redirect("/")
    conn = get_data_connection()
    try:
        company = conn.execute(
            "SELECT * FROM companies WHERE id = ?", (company_id,)
        ).fetchone()
        if not company:
            return render_template("errors/404.html"), 404
        if session.get("role") != "admin" and session.get("username") != company["owner"]:
            return render_template("errors/403.html"), 403

        if request.method == "POST":
            new_name = request.form.get("company_name", "").strip()
            new_description = request.form.get("description", "").strip()
            if not new_name:
                flash("Company name is required.", "warning")
                return redirect(f"/companies/{company_id}/edit")
            conn.execute(
                "UPDATE companies SET name = ?, description = ? WHERE id = ?",
                (new_name, new_description, company_id),
            )
            conn.commit()
            flash("Company updated successfully.", "success")
            return redirect("/companies")
    finally:
        conn.close()
    return render_template("companies/edit_company.html", company=company)
