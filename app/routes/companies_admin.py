"""Admin routes for company management."""
from flask import flash, redirect, render_template, request, session

from db import get_data_connection
from server import app


@app.route("/admin/companies")
def admin_list_companies():
    if session.get("role") != "admin":
        return render_template("errors/403.html"), 403
    conn = get_data_connection()
    try:
        companies = conn.execute("SELECT * FROM companies").fetchall()
    finally:
        conn.close()
    return render_template("admin/admin_companies.html", companies=companies)


@app.route("/admin/companies/add", methods=["GET", "POST"])
def admin_add_company():
    if session.get("role") != "admin":
        return render_template("errors/403.html"), 403
    if request.method == "POST":
        company_name = request.form.get("company_name", "").strip()
        owner = request.form.get("owner", "").strip()
        if not company_name or not owner:
            flash("Company name and owner are required.", "warning")
            return redirect("/admin/companies")
        conn = get_data_connection()
        try:
            conn.execute(
                "INSERT INTO companies (name, owner) VALUES (?, ?)",
                (company_name, owner),
            )
            conn.commit()
        finally:
            conn.close()
        flash("Company created successfully.", "success")
        return redirect("/admin/companies")
    return render_template("admin/admin_companies.html")


@app.route("/admin/companies/delete", methods=["POST"])
def delete_company():
    if session.get("role") != "admin":
        return render_template("errors/403.html"), 403
    try:
        company_id = int(request.form.get("company", ""))
    except (TypeError, ValueError):
        flash("Invalid company identifier.", "danger")
        return redirect("/admin/companies")

    conn = get_data_connection()
    try:
        conn.execute("DELETE FROM companies WHERE id = ?", (company_id,))
        conn.execute("DELETE FROM comments WHERE company_id = ?", (company_id,))
        conn.commit()
    finally:
        conn.close()
    flash("Company deleted.", "warning")
    return redirect("/admin/companies")
