import os
from server import app
from routes import auth, companies
from init_db import init_db

# CWE-489: Active Debug Code — DEBUG hardcoded to True
DEBUG = True

if __name__ == "__main__":
    init_db()
    app.run(debug=DEBUG, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
