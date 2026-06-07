# Práctica 3 DevSecOps — Pipeline CI/CD de Seguridad

**Equipo:** Miguel Bravo Figueroa & Jesús del Salto Díaz  
**Máster en Ciberseguridad — UNIE Universidad**  
**URL pública:** https://practica3-devsecops-p3.onrender.com  
**Repositorio:** https://github.com/migueleduardobravo-debug/Practica3_DevSecOps  

---

## Resumen del Modelado de Amenazas (Práctica 1 — STRIDE)

| Categoría STRIDE | Amenaza | Severidad |
|---|---|---|
| Tampering | Manipulación de consultas SQL para saltar autenticación | CRÍTICA |
| Information Disclosure | Exposición de trazas de error y versiones de librerías | ALTA |
| Spoofing | Suplantación de identidad por falta de validación de entradas | ALTA |
| Elevation of Privilege | Ejecución de código arbitrario mediante inyecciones | CRÍTICA |

---

## Pipeline CI/CD Implementado

El pipeline ejecuta automáticamente en cada push a `main`/`develop`:
- **SAST y SCA son bloqueantes**: si fallan, el deploy no ocurre.
- **DAST es informativo**: se ejecuta post-deploy para detectar fallos en runtime.

| Herramienta | Tipo | Función | Por qué bloqueante |
|---|---|---|---|
| Semgrep | SAST | Patrones inseguros en código | Detecta SQLi, XSS antes de producción |
| Bandit | SAST | Análisis específico Python | Detecta B608 (SQLi), B201 (DEBUG) |
| pip-audit | SCA | CVEs en dependencias | Dependencias vulnerables = riesgo directo |
| OWASP ZAP | DAST | Testing dinámico vs URL pública | Detecta fallos de configuración en runtime |

---

## Vulnerabilidades Corregidas

| # | Vulnerabilidad | Severidad | CWE | Herramienta | Autor | Estado |
|---|---|---|---|---|---|---|
| 1 | SQL Injection en login | CRÍTICA | CWE-89 | Bandit B608 | Miguel | ✅ Corregido |
| 2 | Dependencias con CVEs | ALTA | CWE-1104 | pip-audit | Miguel | ✅ Corregido |
| 3 | DEBUG hardcodeado | MEDIA | CWE-489 | Bandit B201 | Jesús | ✅ Corregido |
| 4 | Error handling inseguro | MEDIA | CWE-209 | Semgrep | Jesús | ✅ Corregido |
| 5 | Ausencia de HSTS | MEDIA | CWE-16 | OWASP ZAP | Jesús | ✅ Corregido |

### Vulnerabilidad no corregida (aceptada)

**B104 — Binding to all interfaces (`host="0.0.0.0"`)**  
**Decisión:** Falso positivo / Riesgo aceptado  
**Justificación:** Un servidor web debe escuchar en `0.0.0.0` para recibir tráfico externo. Es el comportamiento esperado y requerido para el despliegue en Render. Bandit lo marca como Medium pero no es una vulnerabilidad en este contexto.

---

## Evidencias de Ejecución

- Pipeline fallando (pre-remediación): run #18 en GitHub Actions
- Pipeline pasando (post-remediación): run #27 en GitHub Actions
- Artifacts descargables: `sast-report`, `sca-report`, `dast-report`

---

## Diagrama del Flujo DevSecOps
---

## Ejecución Local

```bash
git clone https://github.com/migueleduardobravo-debug/Practica3_DevSecOps.git
cd Practica3_DevSecOps/app
pip install -r requirements.txt
python init_db.py
python main.py
```

Acceder en: http://localhost:5000/login  
Credenciales de prueba: `admin` / `admin123`

---

## Reflexión Final

Esta práctica nos ha demostrado que DevSecOps no consiste en instalar herramientas de seguridad, sino en integrarlas de forma que proporcionen feedback útil sin detener innecesariamente el ciclo de desarrollo.

La arquitectura **Fail-Fast** que implementamos — donde SAST y SCA bloquean el pipeline antes del deploy — nos permitió detectar vulnerabilidades críticas (SQL Injection, dependencias con CVEs) antes de que llegaran a producción.

La diferencia más significativa respecto a un desarrollo tradicional es que la seguridad dejó de ser una fase final y se convirtió en una condición necesaria para cada despliegue.

**Declaración de uso de IA:** Se ha utilizado Claude (Anthropic) como asistente para la implementación del pipeline, configuración del entorno y resolución de errores técnicos. Todo el código ha sido revisado y comprendido por los autores.

---

## Docker (opcional)

El repositorio incluye un `Dockerfile` con buenas prácticas:
- Imagen base `python:3.11-slim`
- Usuario no-root (`appuser`)
- Sin dependencias innecesarias

```bash
docker build -t practica3-devsecops .
docker run -p 5000:5000 -e FLASK_DEBUG=0 -e SECRET_KEY=clave practica3-devsecops
```
