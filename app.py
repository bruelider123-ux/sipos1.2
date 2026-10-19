"""
app.py
------
Punto de entrada de SIPOS.

En la Fase 1, esta app solo confirma que:
1. Flask arranca correctamente.
2. La configuración se lee bien desde config.py / .env.
3. Se puede abrir una conexión a la base de datos SQLite.

A partir de la Fase 2 en adelante, acá se registrarán los "blueprints"
(módulos de rutas) de productos, ventas, compras, dashboard, etc.
"""

from flask import Flask, render_template, jsonify
from config import config
from utils.database import get_db_connection, init_db, contar_tablas
from models.usuario import crear_admin_por_defecto

def create_app():
    """
    Application factory: crea y configura la instancia de Flask.
    Se usa este patrón (en vez de crear `app` como variable global suelta)
    porque facilita las pruebas automáticas y evitar problemas de
    importación circular a medida que el proyecto crezca.
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["DEBUG"] = config.DEBUG

    # Crea las tablas (si no existen) y el usuario admin por defecto.
    # Es seguro llamarlo cada vez que arranca la app: no duplica nada.
    init_db()
    crear_admin_por_defecto()

    # --------------------------------------------------------------
    # A partir de la Fase 3 en adelante, acá se registran los blueprints:
    #
    # from routes.dashboard import dashboard_bp
    # from routes.productos import productos_bp
    # ...
    # app.register_blueprint(dashboard_bp)
    # app.register_blueprint(productos_bp)
    #
    # Por ahora (Fase 1) no existe ningún blueprint todavía.
    # --------------------------------------------------------------

    @app.route("/")
    def index():
        """Pantalla temporal de verificación (Fase 1 y 2)."""
        try:
            conn = get_db_connection()
            conn.close()
            db_status = "✅ Conectado correctamente"
            total_tablas = contar_tablas()
        except Exception as e:
            db_status = f"❌ Error: {e}"
            total_tablas = 0

        return render_template(
            "fase1_ok.html",
            db_status=db_status,
            debug_mode=app.config["DEBUG"],
            total_tablas=total_tablas,
        )

    @app.route("/api/health")
    def health():
        """Endpoint simple para verificar por API que el servidor responde."""
        return jsonify({
            "status": "ok",
            "fase": "2 - Base de datos y modelos",
            "sistema": "SIPOS",
            "tablas": contar_tablas(),
        })

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=config.DEBUG, host="127.0.0.1", port=5000)
