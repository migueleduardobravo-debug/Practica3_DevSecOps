#!/bin/bash
# Script de arranque para la aplicación Flask
pip install -r requirements.txt
gunicorn app:app
