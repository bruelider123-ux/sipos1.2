# CHANGELOG - SIPOS

## [Fase 1] - 2026-09-05 - Arquitectura y configuración

### Agregado
- Estructura completa de carpetas: `database/`, `models/`, `routes/`, `services/`, `ml/`, `templates/`, `static/{css,js,img}/`, `utils/`.
- `config.py`: configuración centralizada leída desde variables de entorno (`.env`).
- `.env.example`: plantilla de variables de entorno.
- `utils/database.py`: módulo centralizado de conexión a SQLite, con helper `execute_query()` para evitar repetir código de conexión en cada ruta.
- `app.py`: aplicación Flask con patrón *application factory* (`create_app()`), ruta `/` de verificación y ruta `/api/health`.
- `templates/base.html`: plantilla base con Bootstrap 5 y Chart.js vía CDN.
- `templates/fase1_ok.html`: pantalla temporal de verificación (se reemplaza en Fase 7 por el dashboard real).
- `static/css/style.css` y `static/js/app.js`: archivos iniciales, se completan en fases posteriores.
- `requirements.txt`, `.gitignore`, `README.md`.

### Decisiones técnicas
- Se usa `sqlite3` (stdlib) en lugar de `Flask-SQLAlchemy` por simplicidad y porque la consigna original lo permitía explícitamente. Ver nota en el README.

### Verificado
- El servidor Flask arranca correctamente (`python app.py`).
- La ruta `/` responde con estado 200 y muestra "Conexión a base de datos: ✅ Conectado correctamente".
- La ruta `/api/health` responde JSON válido.
- Se genera correctamente el archivo `database/sipos.db` (vacío, sin tablas — eso corresponde a la Fase 2).

### Pendiente para próximas fases
- Definición de tablas y modelos (Fase 2).
- `seed.py` con datos de prueba (Fase 2/4).
- Login y sesiones (Fase 3).
