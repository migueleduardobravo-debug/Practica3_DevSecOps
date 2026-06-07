import os
import sqlite3
from flask import Flask

app = Flask(__name__)
app.secret_key = "dev-secret-key-hardcoded"
app.config["SESSION_COOKIE_HTTPONLY"] = True
