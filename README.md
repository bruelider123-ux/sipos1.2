# SIPOS — Sistema Inteligente de Predicción y Optimización de Stock

## Descripción
SIPOS es un sistema web para que pequeños y medianos comercios controlen su inventario, analicen sus ventas y tomen mejores decisiones de reposición de stock, incorporando un módulo de Machine Learning para predecir demanda futura.

Proyecto académico — Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial.

## Estado actual del desarrollo
- ✅ **Fase 1: Arquitectura y configuración** (esta entrega).
- ⬜ Fase 2 en adelante: base de datos y modelos, autenticación, CRUDs, ventas/compras, stock y alertas, dashboard, Machine Learning, recomendación de reposición, reportes, diseño, pruebas finales.

## Tecnologías utilizadas
- **Backend:** Python 3.12+, Flask
- **Base de datos:** SQLite, accedida mediante el módulo estándar `sqlite3` (ver nota técnica más abajo)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- **Machine Learning:** Pandas, NumPy, scikit-learn (a partir de la Fase 8)
- **Reportes:** ReportLab (PDF), OpenPyXL (Excel) (a partir de la Fase 10)

### Nota técnica sobre la base de datos
La consigna original permitía usar "SQLAlchemy o sqlite3". Se optó por `sqlite3` (librería estándar de Python) en lugar de `Flask-SQLAlchemy` porque simplifica la instalación (una dependencia menos) y es más que suficiente para el volumen de datos de un comercio pequeño/mediano. Todas las consultas usan parámetros (`?`) para evitar inyección SQL. El acceso a la base de datos está centralizado en `utils/database.py`, así que si en el futuro se quisiera migrar a SQLAlchemy, solo habría que reemplazar ese archivo.

## Arquitectura del proyecto
```
SIPOS/
├── app.py                 -> Punto de entrada de la aplicación Flask
├── config.py               -> Configuración centralizada (lee .env)
├── requirements.txt
├── .env.example             -> Plantilla de variables de entorno
├── database/
│   └── sipos.db             -> Base de datos SQLite (se genera al arrancar)
├── models/                  -> Definición de entidades (Fase 2)
├── routes/                  -> Rutas/Blueprints de Flask (Fase 3 en adelante)
├── services/                -> Lógica de negocio (inventario, ventas, predicción, reportes)
├── ml/                      -> Módulo de Machine Learning (Fase 8)
├── templates/                -> Vistas HTML (Jinja2)
├── static/
│   ├── css/style.css
│   ├── js/app.js
│   └── img/
└── utils/
    └── database.py          -> Conexión centralizada a la base de datos
```

## Base de datos
El diseño completo de tablas (`usuarios`, `categorias`, `productos`, `proveedores`, `clientes`, `ventas`, `detalle_ventas`, `compras`, `detalle_compras`, `movimientos_stock`) se implementa en la **Fase 2**. En esta Fase 1 solo existe la conexión a la base de datos; el archivo `sipos.db` se crea vacío al arrancar la aplicación por primera vez.

## Funcionamiento (resumen general)
1. El usuario inicia sesión (Fase 3).
2. Gestiona productos, categorías, proveedores y clientes (Fase 4).
3. Registra ventas y compras, que actualizan el stock automáticamente (Fase 5-6).
4. El dashboard muestra el estado general del negocio con gráficos (Fase 7).
5. El módulo de IA analiza el historial de ventas y predice demanda futura, recomendando cuánto reponer (Fase 8-9).
6. Se pueden generar reportes exportables en PDF/Excel/CSV (Fase 10).

## Inteligencia Artificial utilizada
Se implementará a partir de la Fase 8: un modelo de regresión (a definir entre Regresión Lineal, Random Forest o Gradient Boosting, comenzando por el más simple y explicable) entrenado con el historial de ventas de cada producto, para estimar la demanda de los próximos 7 y 30 días. Se documentará en detalle en esa fase, incluyendo una sección "¿Cómo funciona la predicción?" pensada para poder explicarse oralmente.

## Instalación

### 1. Clonar/descargar el proyecto
Descomprimir el `.zip` del proyecto en la carpeta que prefieras.

### 2. Abrirlo en Visual Studio Code
```powershell
code SIPOS
```

### 3. Crear entorno virtual
```powershell
python -m venv venv
```

### 4. Activar entorno virtual (Windows PowerShell)
```powershell
venv\Scripts\Activate.ps1
```
> Si PowerShell bloquea la ejecución de scripts, ejecutar una vez como administrador:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 5. Instalar dependencias
```powershell
pip install -r requirements.txt
```

### 6. Configurar variables de entorno
```powershell
copy .env.example .env
```

### 7. Crear base de datos
Se implementa en la Fase 2. Por ahora, al ejecutar `app.py` se crea automáticamente el archivo vacío `database/sipos.db`.

### 8. Ejecutar seed.py (datos de prueba)
Se implementa en la Fase 2/4. Todavía no existe en esta entrega.

### 9. Ejecutar la aplicación
```powershell
python app.py
```

### 10. Abrir en el navegador
```
http://127.0.0.1:5000
```
Deberías ver la pantalla **"✅ SIPOS - Proyecto base OK"** confirmando que el servidor, la configuración y la base de datos funcionan.

### 11. Iniciar sesión
El sistema de login se implementa en la **Fase 3**. Usuario de prueba planeado: `admin` / `admin123` (con contraseña hasheada, nunca en texto plano).

## Estructura de próximas fases
- Fase 2: Base de datos completa y modelos.
- Fase 3: Autenticación.
- Fase 4: CRUD de productos, categorías, proveedores, clientes.
- Fase 5: Ventas y compras.
- Fase 6: Control de stock y alertas.
- Fase 7: Dashboard y gráficos.
- Fase 8: Machine Learning y predicciones.
- Fase 9: Recomendación de reposición.
- Fase 10: Reportes y exportaciones.
- Fase 11: Diseño y mejoras UX.
- Fase 12: Pruebas y corrección de errores.

## Posibles mejoras futuras
- Autenticación multi-comercio (multi-tenant) para escalar a varios negocios.
- Notificaciones automáticas (email/WhatsApp) ante stock crítico.
- App móvil complementaria.
- Modelos de ML más avanzados (series de tiempo, XGBoost) a medida que haya más datos históricos reales.
