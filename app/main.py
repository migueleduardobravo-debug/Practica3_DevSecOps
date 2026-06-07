import os
from server import app
from routes import auth, companies
from init_db import init_db

# CWE-489 fix: DEBUG controlado por variable de entorno (12-Factor App)
# Produccion (Render): FLASK_DEBUG=0 -> debug=False
# Desarrollo local: FLASK_DEBUG=1 -> debug=True
DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

if __name__ == "__main__":
    init_db()
    app.run(debug=DEBUG, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))  # nosec B104
