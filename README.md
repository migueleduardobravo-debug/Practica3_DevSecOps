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

## 🛡️ Registro de Remediación y Justificación 
### Vulnerabilidades Corregidas

| Participante | Hallazgo | CWE | Herramienta | Remediación Técnica |
| :--- | :--- | :--- | :--- | :--- |
| **Miguel Bravo** | Inyección SQL | CWE-89 | Semgrep (SAST) | Implementación de consultas parametrizadas (Prepared Statements) para neutralizar entradas maliciosas. |
| **Jesús** | Componentes Vulnerables | CWE-1104 | pip-audit (SCA) | Actualización de dependencias a versiones estables (Flask 3.1.3, Gunicorn 22.0.0) para mitigar CVEs conocidos. |
| **Jesús** | XSS Reflejado | CWE-79 | Semgrep (SAST) | Saneamiento de la salida de datos mediante el uso de motores de plantillas seguros o funciones de escape. |

### Hallazgo No Corregido (Justificación)
- **Vulnerabilidad:** Falta de cabeceras de seguridad (HSTS / CSP).
- **Herramienta:** OWASP ZAP (DAST).
- **Justificación:** **Riesgo Aceptado / Fuera del alcance.** La implementación de HSTS requiere configuraciones a nivel de servidor/proxy que en la capa gratuita de Render están preconfiguradas y no son editables sin un plan superior. Se priorizó la seguridad a nivel de código fuente.
