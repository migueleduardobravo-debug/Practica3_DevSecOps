"""Companies routes — post-remediation."""
import logging
from flask import jsonify, request, session, redirect
from db import get_db
from server import app

logger = logging.getLogger(_name_)


@app.route("/companies", methods=["GET"])
def list_companies():
    if "username" not in session:
        return redirect("/login")
    conn = get_db()
    try:
        companies = conn.execute("SELECT * FROM companies").fetchall()
        return jsonify([dict(c) for c in companies])
    except Exception as e:
        # CWE-209 fix: detalles internos al log, mensaje generico al usuario
        logger.error("Error listing companies: %s", e, exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        conn.close()


@app.route("/companies", methods=["POST"])
def create_company():
    if "username" not in session:
        return redirect("/login")
    data = request.get_json() or {}
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "name and email are required"}), 400
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO companies (name, email) VALUES (?, ?)",
            (data["name"], data["email"])
        )
        conn.commit()
        return jsonify({"status": "created"}), 201
    except Exception as e:
        logger.error("Error creating company: %s", e, exc_info=True)
        return jsonify({"error": "Could not create company"}), 500
    finally:
        conn.close()
