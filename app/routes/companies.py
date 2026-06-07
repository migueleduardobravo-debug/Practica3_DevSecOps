"""Companies routes — VULNERABLE VERSION (pre-remediation)."""
from flask import jsonify, request, session, redirect
from db import get_db
from server import app


@app.route("/companies", methods=["GET"])
def list_companies():
    if "username" not in session:
        return redirect("/login")
    conn = get_db()
    try:
        companies = conn.execute("SELECT * FROM companies").fetchall()
        return jsonify([dict(c) for c in companies])
    except Exception as e:
        # CWE-209: expone detalles internos de la BD al usuario
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@app.route("/companies", methods=["POST"])
def create_company():
    if "username" not in session:
        return redirect("/login")
    data = request.get_json() or {}
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO companies (name, email) VALUES (?, ?)",
            (data.get("name"), data.get("email"))
        )
        conn.commit()
        return jsonify({"status": "created"}), 201
    except Exception as e:
        # CWE-209: expone IntegrityError con estructura interna
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
