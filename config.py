"""
config.py
---------
Configuración centralizada de SIPOS.

Todos los valores sensibles o dependientes del entorno (claves secretas,
rutas, modo debug) se leen desde variables de entorno usando python-dotenv,
en lugar de estar escritos directamente en el código. Esto permite además
que el mismo código funcione en distintas máquinas sin modificarlo.
"""

import os
from dotenv import load_dotenv

# Carga el archivo .env si existe (en desarrollo). En producción, las
# variables de entorno se definirían directamente en el sistema operativo.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Config:
    """Configuración base de la aplicación."""

    # Clave usada por Flask para firmar la sesión (cookies). Si no existe
    # en el .env, se usa un valor por defecto SOLO para desarrollo.
    SECRET_KEY = os.environ.get("SECRET_KEY", "sipos-dev-secret-key-cambiar-en-produccion")

    # Modo debug: activa recarga automática y mensajes de error detallados.
    # NUNCA debe estar en True en un entorno real de producción.
    DEBUG = os.environ.get("FLASK_DEBUG", "True") == "True"

    # Ruta absoluta al archivo de base de datos SQLite.
    DATABASE_PATH = os.path.join(BASE_DIR, "database", "sipos.db")

    # Duración de la sesión de login, en minutos.
    SESSION_LIFETIME_MINUTES = int(os.environ.get("SESSION_LIFETIME_MINUTES", "120"))

    # Parámetros de negocio usados por el módulo de stock/predicción.
    # Se dejan acá para poder ajustarlos sin tocar la lógica del sistema.
    STOCK_BAJO_PORCENTAJE = float(os.environ.get("STOCK_BAJO_PORCENTAJE", "0.5"))   # 50% del mínimo
    STOCK_CRITICO_PORCENTAJE = float(os.environ.get("STOCK_CRITICO_PORCENTAJE", "0.2"))  # 20% del mínimo

    # Si es False (por defecto), el sistema NO permite confirmar una venta
    # que deje el stock de algún producto por debajo de cero.
    PERMITIR_STOCK_NEGATIVO = os.environ.get("PERMITIR_STOCK_NEGATIVO", "False") == "True"


config = Config()
