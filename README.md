# 🛡️ Práctica 3: Implementación DevSecOps - Miguel & Jesús

## 📌 Objetivo
Este proyecto demuestra la integración de un pipeline CI/CD de seguridad sobre una aplicación Flask que contiene vulnerabilidades críticas intencionadas (CWE-89, CWE-79, CWE-489).

## 🚀 Repositorio y Despliegue
- **GitHub:** [https://github.com/migueleduardobravo-debug/Practica3_DevSecOps]
- **URL Pública (Render):** [https://dashboard.render.com/web/srv-d7uurn7lk1mc73aqdh6g]

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python 3.10+
- **Framework:** Flask
- **Pipeline:** GitHub Actions
- **Seguridad:** Semgrep (SAST), pip-audit (SCA), OWASP ZAP (DAST)

## 🏗️ Estructura del Proyecto
- `app.py`: Código fuente principal (Versión Vulnerable para testeo de Pipeline).
- `.github/workflows/`: Definición de los controles automáticos de seguridad.
- `requirements.txt`: Gestión de dependencias.
- `Procfile` & `start.sh`: Configuración de despliegue.
