"""
seed.py
--------
Carga datos de prueba en la base de datos, para poder ver el sistema
funcionando sin tener que cargar todo a mano.

IMPORTANTE: estos son DATOS DE PRUEBA, pensados para probar el sistema
durante el desarrollo académico. No son datos reales de ningún comercio.

Uso (con el entorno virtual activado):
    python seed.py

Se puede correr varias veces: antes de insertar, borra los datos de
prueba anteriores (identificados por sus códigos/nombres), así no se
duplican.

NOTA: en esta versión (Fase 4) se cargan categorías, proveedores,
clientes y productos. Las ventas, compras y movimientos históricos
(necesarios para probar el módulo de Machine Learning) se agregan en
este mismo script más adelante, en la Fase 5-6, una vez que existe la
lógica de descuento/aumento automático de stock.
"""

from app import create_app
from utils.database import execute_query
from models.categoria import crear_categoria
from models.proveedor import crear_proveedor
from models.cliente import crear_cliente
from models.producto import crear_producto


def limpiar_datos_de_prueba():
    """
    Borra los datos de prueba de una corrida anterior de este script,
    para poder ejecutarlo varias veces sin duplicar. Se identifican por
    los códigos de producto (empiezan con 'DEMO-') y nombres conocidos.
    """
    execute_query("DELETE FROM detalle_ventas WHERE producto_id IN (SELECT id FROM productos WHERE codigo LIKE 'DEMO-%')", commit=True)
    execute_query("DELETE FROM detalle_compras WHERE producto_id IN (SELECT id FROM productos WHERE codigo LIKE 'DEMO-%')", commit=True)
    execute_query("DELETE FROM movimientos_stock WHERE producto_id IN (SELECT id FROM productos WHERE codigo LIKE 'DEMO-%')", commit=True)
    execute_query("DELETE FROM productos WHERE codigo LIKE 'DEMO-%'", commit=True)
    execute_query("DELETE FROM categorias WHERE nombre IN ('Bebidas', 'Almacén', 'Limpieza', 'Lácteos')", commit=True)
    execute_query("DELETE FROM proveedores WHERE nombre IN ('Distribuidora Norte', 'Almacén Mayorista SA', 'Lácteos del Valle')", commit=True)
    execute_query("DELETE FROM clientes WHERE nombre IN ('Consumidor Final', 'Kiosco La Esquina', 'Restaurante El Fogón')", commit=True)


def cargar_datos():
    print("Cargando DATOS DE PRUEBA en SIPOS...")
    print()

    # --- Categorías ---
    cat_bebidas = crear_categoria("Bebidas", "Gaseosas, aguas, jugos")
    cat_almacen = crear_categoria("Almacén", "Productos secos, enlatados, etc.")
    cat_limpieza = crear_categoria("Limpieza", "Artículos de limpieza del hogar")
    cat_lacteos = crear_categoria("Lácteos", "Leche, quesos, yogures")
    print(f"✔ 4 categorías creadas")

    # --- Proveedores ---
    prov_norte = crear_proveedor("Distribuidora Norte", telefono="388-4000000", email="ventas@distnorte.com.ar")
    prov_mayorista = crear_proveedor("Almacén Mayorista SA", telefono="388-4111111", email="contacto@mayoristasa.com")
    prov_lacteos = crear_proveedor("Lácteos del Valle", telefono="388-4222222", email="pedidos@lacteosdelvalle.com")
    print(f"✔ 3 proveedores creados")

    # --- Clientes ---
    crear_cliente("Consumidor Final")
    crear_cliente("Kiosco La Esquina", telefono="388-4333333")
    crear_cliente("Restaurante El Fogón", telefono="388-4444444", email="compras@elfogon.com")
    print(f"✔ 3 clientes creados")

    # --- Productos (códigos con prefijo DEMO- para poder limpiarlos después) ---
    productos_demo = [
        dict(codigo="DEMO-001", nombre="Gaseosa Cola 2.25L", categoria_id=cat_bebidas, proveedor_id=prov_norte,
             precio_compra=800, precio_venta=1500, stock_minimo=15, stock_maximo=100, stock_inicial=4, unidad="unidad"),
        dict(codigo="DEMO-002", nombre="Agua Mineral 1.5L", categoria_id=cat_bebidas, proveedor_id=prov_norte,
             precio_compra=350, precio_venta=700, stock_minimo=20, stock_maximo=120, stock_inicial=45, unidad="unidad"),
        dict(codigo="DEMO-003", nombre="Pan Lactal", categoria_id=cat_almacen, proveedor_id=prov_mayorista,
             precio_compra=900, precio_venta=1800, stock_minimo=10, stock_maximo=40, stock_inicial=0, unidad="unidad"),
        dict(codigo="DEMO-004", nombre="Arroz 1kg", categoria_id=cat_almacen, proveedor_id=prov_mayorista,
             precio_compra=600, precio_venta=1100, stock_minimo=10, stock_maximo=60, stock_inicial=25, unidad="kg"),
        dict(codigo="DEMO-005", nombre="Detergente 750ml", categoria_id=cat_limpieza, proveedor_id=prov_mayorista,
             precio_compra=1200, precio_venta=2200, stock_minimo=8, stock_maximo=40, stock_inicial=2, unidad="unidad"),
        dict(codigo="DEMO-006", nombre="Leche Entera 1L", categoria_id=cat_lacteos, proveedor_id=prov_lacteos,
             precio_compra=500, precio_venta=950, stock_minimo=20, stock_maximo=80, stock_inicial=30, unidad="litro"),
        dict(codigo="DEMO-007", nombre="Queso Cremoso 500g", categoria_id=cat_lacteos, proveedor_id=prov_lacteos,
             precio_compra=2500, precio_venta=4200, stock_minimo=5, stock_maximo=25, stock_inicial=1, unidad="unidad"),
    ]

    for p in productos_demo:
        crear_producto(**p)

    print(f"✔ {len(productos_demo)} productos creados (con distintos niveles de stock, a propósito, para ver los 4 estados: normal/bajo/crítico/sin stock)")
    print()
    print("Datos de prueba cargados correctamente.")
    print("Iniciá sesión con usuario: admin / contraseña: admin123 y mirá la sección Productos.")


if __name__ == "__main__":
    app = create_app()  # crea las tablas si no existen, y el usuario admin
    with app.app_context():
        limpiar_datos_de_prueba()
        cargar_datos()
