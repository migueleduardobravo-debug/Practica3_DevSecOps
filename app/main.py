import os
from server import app
from routes import auth, companies, companies_admin, users_admin, profile
from db import ensure_users_db

DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

if __name__ == "__main__":
    ensure_users_db()
    app.run(debug=DEBUG, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))  # nosec B104
