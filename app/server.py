import os, secrets
from flask import Flask, render_template
from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFError

def _truthy(env_var, default):
    v = os.environ.get(env_var)
    return default if v is None else v.strip().lower() in {"1","true","yes","on"}

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=_truthy("SESSION_COOKIE_SECURE", True),
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=1800,
    MAX_CONTENT_LENGTH=1*1024*1024,
    WTF_CSRF_TIME_LIMIT=3600,
)
csrf = CSRFProtect(app)

@app.errorhandler(404)
def not_found(_e): return render_template("errors/404.html"), 404

@app.errorhandler(403)
def forbidden(_e): return render_template("errors/403.html"), 403

@app.errorhandler(CSRFError)
def csrf_error(e): return render_template("errors/403.html", reason=e.description), 400

@app.after_request
def set_security_headers(response):
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "font-src 'self' https://cdn.jsdelivr.net; frame-ancestors 'none'"
    )
    response.headers["Server"] = "Hidden"
    return response
