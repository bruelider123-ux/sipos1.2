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

from flask import Flask, jsonify
from config import config
from utils.database import init_db, contar_tablas
from models.usuario import crear_admin_por_defecto
from routes.auth import auth_bp, configurar_sesion
from routes.categorias import categorias_bp
from routes.proveedores import proveedores_bp
from routes.clientes import clientes_bp
from routes.productos import productos_bp
from routes.ventas import ventas_bp
from routes.compras import compras_bp
from routes.stock import stock_bp
from routes.dashboard import dashboard_bp
from routes.prediccion import prediccion_bp
from routes.reportes import reportes_bp
from routes.configuracion import configuracion_bp
from utils.formato import cantidad, pesos, fecha, fecha_hora

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
    configurar_sesion(app)

    # Formato argentino de números y plata en las plantillas: {{ valor|pesos }} y {{ valor|cantidad }}
    app.add_template_filter(cantidad, "cantidad")
    app.add_template_filter(pesos, "pesos")
    app.add_template_filter(fecha, "fecha")
    app.add_template_filter(fecha_hora, "fecha_hora")

    # Crea las tablas (si no existen) y el usuario admin por defecto.
    # Es seguro llamarlo cada vez que arranca la app: no duplica nada.
    init_db()
    crear_admin_por_defecto()

    # --------------------------------------------------------------
    # Blueprints registrados hasta ahora:
    app.register_blueprint(auth_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(proveedores_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(compras_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(prediccion_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(configuracion_bp)
    #
    # A partir de la Fase 11 en adelante, se agregan mejoras de diseño
    # y UX sobre lo ya construido.
    # --------------------------------------------------------------

    @app.route("/api/health")
    def health():
        """Endpoint simple para verificar por API que el servidor responde."""
        return jsonify({
            "status": "ok",
            "fase": "11 - Diseno y mejoras de interfaz",
            "sistema": "SIPOS",
            "tablas": contar_tablas(),
        })

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=config.DEBUG, host="127.0.0.1", port=5000)
