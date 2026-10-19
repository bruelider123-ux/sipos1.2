# CHANGELOG - SIPOS

## [Fase 3] - 2026-09-09 - Autenticación

### Agregado
- `utils/helpers.py`: decorador `login_required` para proteger rutas, y `usuario_actual()` para obtener el usuario de la sesión.
- `routes/auth.py`: blueprint con `/login` (GET/POST) y `/logout`, usando sesiones nativas de Flask (cookies firmadas con `SECRET_KEY`).
- `templates/login.html`: pantalla de login con Bootstrap.
- `app.py`: registra el blueprint de auth, protege la ruta `/` con `@login_required`, y configura la duración de la sesión (`SESSION_LIFETIME_MINUTES` desde `.env`).
- `templates/base.html`: renderiza los mensajes flash (avisos de éxito/error) en cualquier página.
- `templates/fase1_ok.html`: ahora saluda al usuario logueado y muestra el botón "Cerrar sesión".

### Decisiones técnicas
- Se usan sesiones nativas de Flask (no una librería como Flask-Login) porque el sistema es de un solo usuario administrador por comercio en esta etapa, y las sesiones nativas ya cubren toda la necesidad: son simples, seguras (cookies firmadas) y no agregan una dependencia más.

### Verificado (prueba automática de punta a punta)
1. Acceder a `/` sin sesión → redirige a `/login`.
2. Login con contraseña incorrecta → muestra "Usuario o contraseña incorrectos".
3. Login con `admin` / `admin123` → redirige a `/`.
4. Con sesión activa, `/` saluda "Hola, Administrador (admin)".
5. `/logout` → redirige a `/login`.
6. Después de cerrar sesión, `/` vuelve a exigir login.

### Pendiente para próximas fases
- CRUD de productos, categorías, proveedores, clientes (Fase 4).
- `seed.py` con datos de prueba.
- Descuento/aumento automático de stock al confirmar venta/compra (Fase 5-6).

## [Fase 2] - 2026-09-08 - Base de datos y modelos

### Agregado
- `database/schema.sql`: esquema completo con las 10 tablas (`usuarios`, `categorias`, `proveedores`, `clientes`, `productos`, `ventas`, `detalle_ventas`, `compras`, `detalle_compras`, `movimientos_stock`), claves foráneas e índices.
- `utils/database.py`: se agregan `init_db()` (crea las tablas a partir de schema.sql) y `contar_tablas()`.
- `models/categoria.py`, `models/proveedor.py`, `models/cliente.py`: CRUD completo.
- `models/producto.py`: CRUD + método `estado_stock()` que clasifica cada producto en `sin_stock`, `critico`, `bajo` o `normal` según los porcentajes configurados en `config.py`.
- `models/movimiento_stock.py`: registro y consulta de la bitácora de movimientos de stock.
- `models/venta.py` y `models/compra.py`: creación transaccional de cabecera + detalle (todo o nada), y consultas con filtro por fecha.
- `models/usuario.py`: modelo de usuario con hashing de contraseña (`werkzeug.security`) y creación automática del usuario `admin` / `admin123` la primera vez que arranca el sistema.
- `app.py`: ahora llama a `init_db()` y `crear_admin_por_defecto()` al arrancar.

### Verificado
- Las 10 tablas se crean correctamente al arrancar la app.
- El usuario `admin` se crea automáticamente con contraseña hasheada (se probó login válido e inválido).
- Se probaron de punta a punta: alta de categoría, proveedor, cliente, producto (con cálculo correcto de estado de stock), venta con detalle, compra con detalle, y registro de movimiento de stock.
- El servidor sigue arrancando sin errores y `/api/health` ahora informa la cantidad de tablas.

### Pendiente para próximas fases
- Login real con sesión y protección de rutas (Fase 3).
- `seed.py` con datos de prueba masivos (Fase 4).
- Descuento/aumento automático de stock al confirmar una venta o compra (Fase 5-6): por ahora `crear_venta_con_detalle` y `crear_compra_con_detalle` solo guardan los datos, todavía no tocan `stock_actual` ni `movimientos_stock` automáticamente.

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
