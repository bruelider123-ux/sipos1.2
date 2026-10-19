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

Desde la Fase 8, además de categorías/proveedores/clientes/productos,
este script genera ~120 días de HISTORIAL DE VENTAS simulado para la
mayoría de los productos (con más ventas los fines de semana en
algunos casos), necesario para poder entrenar el módulo de Machine
Learning de predicción de demanda. A propósito:
- El Detergente (DEMO-005) NO tiene ningún historial generado, para
  poder probar el caso de "datos insuficientes" (Fase 8, sección 16).
- El Queso (DEMO-007) tiene historial muy escaso (pocas ventas
  aisladas), para probar el caso límite de "casi sin datos".
Al final, se ajusta el stock de cada producto a un nivel elegido a
propósito para poder ver los 4 estados de stock (normal/bajo/crítico/
sin stock) en el resto del sistema, tal como en las fases anteriores.
"""

import random
from datetime import datetime, timedelta

from app import create_app
from utils.database import execute_query
from models.categoria import crear_categoria
from models.proveedor import crear_proveedor
from models.cliente import crear_cliente
from models.producto import crear_producto
from services.ventas import confirmar_venta
from services.inventario import registrar_ajuste

SEMILLA_ALEATORIA = 42  # fija, para que el historial generado sea siempre el mismo


def limpiar_datos_de_prueba():
    """
    Borra los datos de prueba de una corrida anterior de este script,
    para poder ejecutarlo varias veces sin duplicar. Se identifican por
    los códigos de producto (empiezan con 'DEMO-') y nombres conocidos.
    """
    execute_query("DELETE FROM detalle_ventas WHERE producto_id IN (SELECT id FROM productos WHERE codigo LIKE 'DEMO-%')", commit=True)
    execute_query("DELETE FROM detalle_compras WHERE producto_id IN (SELECT id FROM productos WHERE codigo LIKE 'DEMO-%')", commit=True)
    execute_query("DELETE FROM movimientos_stock WHERE producto_id IN (SELECT id FROM productos WHERE codigo LIKE 'DEMO-%')", commit=True)
    # Cualquier venta/compra que haya quedado sin ninguna línea de detalle
    # (porque todas sus líneas eran de productos DEMO- que acabamos de
    # borrar) queda huérfana: se elimina también su cabecera.
    execute_query("DELETE FROM ventas WHERE id NOT IN (SELECT DISTINCT venta_id FROM detalle_ventas)", commit=True)
    execute_query("DELETE FROM compras WHERE id NOT IN (SELECT DISTINCT compra_id FROM detalle_compras)", commit=True)
    execute_query("DELETE FROM productos WHERE codigo LIKE 'DEMO-%'", commit=True)
    execute_query("DELETE FROM categorias WHERE nombre IN ('Bebidas', 'Almacén', 'Limpieza', 'Lácteos')", commit=True)
    execute_query("DELETE FROM proveedores WHERE nombre IN ('Distribuidora Norte', 'Almacén Mayorista SA', 'Lácteos del Valle')", commit=True)
    execute_query("DELETE FROM clientes WHERE nombre IN ('Consumidor Final', 'Kiosco La Esquina', 'Restaurante El Fogón')", commit=True)


# Parámetros de la simulación de ventas históricas por producto.
# "objetivo_final" es el nivel de stock al que se ajusta el producto
# DESPUÉS de simular las ventas, para poder ver los 4 estados de stock
# en el resto del sistema (igual que en fases anteriores).
CONFIG_SIMULACION = {
    "DEMO-001": dict(base=3.0, variacion=0.35, factor_finde=1.6, dias=120, prob_venta=0.85, objetivo_final=4),
    "DEMO-002": dict(base=4.5, variacion=0.30, factor_finde=1.7, dias=120, prob_venta=0.85, objetivo_final=45),
    "DEMO-003": dict(base=6.0, variacion=0.25, factor_finde=0.7, dias=120, prob_venta=0.95, objetivo_final=0),
    "DEMO-004": dict(base=1.8, variacion=0.40, factor_finde=1.0, dias=120, prob_venta=0.55, objetivo_final=25),
    "DEMO-006": dict(base=5.0, variacion=0.25, factor_finde=1.1, dias=120, prob_venta=0.90, objetivo_final=30),
    "DEMO-007": dict(base=1.0, variacion=0.60, factor_finde=1.0, dias=120, prob_venta=0.12, objetivo_final=1),
    # DEMO-005 (Detergente) queda deliberadamente afuera: sin historial.
}


def generar_historial_ventas(ids_por_codigo: dict, precios_por_codigo: dict):
    """
    Genera ventas históricas día por día (terminando ayer, para no tocar
    las estadísticas de "hoy" del dashboard), con más ventas los fines
    de semana en los productos donde así se configuró. Usa
    services.ventas.confirmar_venta con una fecha pasada explícita, así
    que también genera los movimientos_stock correspondientes, exactamente
    como si hubiera sido una venta real ese día.
    """
    random.seed(SEMILLA_ALEATORIA)
    hoy = datetime.now().date()
    total_ventas_generadas = 0

    for codigo, cfg in CONFIG_SIMULACION.items():
        producto_id = ids_por_codigo[codigo]
        precio = precios_por_codigo[codigo]
        ventas_de_este_producto = 0

        for offset in range(cfg["dias"], 0, -1):
            dia = hoy - timedelta(days=offset)
            es_finde = dia.weekday() >= 5  # 5=sábado, 6=domingo

            if random.random() > cfg["prob_venta"]:
                continue  # ese día no hubo venta de este producto

            media = cfg["base"] * (cfg["factor_finde"] if es_finde else 1.0)
            cantidad = round(random.gauss(media, cfg["base"] * cfg["variacion"]))
            if cantidad <= 0:
                continue

            fecha_str = dia.strftime("%Y-%m-%d") + " 12:00:00"
            confirmar_venta(
                cliente_id=None, metodo_pago="Efectivo",
                lineas=[{"producto_id": producto_id, "cantidad": cantidad, "precio_unitario": precio}],
                fecha=fecha_str,
            )
            ventas_de_este_producto += 1

        total_ventas_generadas += ventas_de_este_producto
        print(f"  · {codigo}: {ventas_de_este_producto} ventas históricas generadas")

    print(f"✔ {total_ventas_generadas} ventas históricas generadas en total (últimos ~120 días)")


def ajustar_stock_final():
    """
    Después de simular el historial de ventas, el stock de cada producto
    quedó en un valor "realista" pero impredecible. Se ajusta al final a
    un nivel elegido a propósito, para poder demostrar los 4 estados de
    stock (normal/bajo/crítico/sin stock) igual que en fases anteriores.
    """
    for codigo, cfg in CONFIG_SIMULACION.items():
        producto = execute_query("SELECT id, stock_actual FROM productos WHERE codigo = ?", (codigo,), fetchone=True)
        delta = cfg["objetivo_final"] - producto["stock_actual"]
        if delta != 0:
            registrar_ajuste(producto["id"], delta, motivo="Ajuste de datos de prueba (nivel de stock para demo)")


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
    # Los que van a tener historial de ventas simulado arrancan con stock
    # alto (1000) para que la simulación nunca se quede sin stock a mitad
    # de camino; al final, ajustar_stock_final() los deja en su nivel
    # "de demo" definitivo.
    productos_demo = [
        dict(codigo="DEMO-001", nombre="Gaseosa Cola 2.25L", categoria_id=cat_bebidas, proveedor_id=prov_norte,
             precio_compra=800, precio_venta=1500, stock_minimo=15, stock_maximo=100, stock_inicial=1000, unidad="unidad"),
        dict(codigo="DEMO-002", nombre="Agua Mineral 1.5L", categoria_id=cat_bebidas, proveedor_id=prov_norte,
             precio_compra=350, precio_venta=700, stock_minimo=20, stock_maximo=120, stock_inicial=1000, unidad="unidad"),
        dict(codigo="DEMO-003", nombre="Pan Lactal", categoria_id=cat_almacen, proveedor_id=prov_mayorista,
             precio_compra=900, precio_venta=1800, stock_minimo=10, stock_maximo=40, stock_inicial=1000, unidad="unidad"),
        dict(codigo="DEMO-004", nombre="Arroz 1kg", categoria_id=cat_almacen, proveedor_id=prov_mayorista,
             precio_compra=600, precio_venta=1100, stock_minimo=10, stock_maximo=60, stock_inicial=1000, unidad="unidad"),
        dict(codigo="DEMO-005", nombre="Detergente 750ml", categoria_id=cat_limpieza, proveedor_id=prov_mayorista,
             precio_compra=1200, precio_venta=2200, stock_minimo=8, stock_maximo=40, stock_inicial=2, unidad="unidad"),
        dict(codigo="DEMO-006", nombre="Leche Entera 1L", categoria_id=cat_lacteos, proveedor_id=prov_lacteos,
             precio_compra=500, precio_venta=950, stock_minimo=20, stock_maximo=80, stock_inicial=1000, unidad="unidad"),
        dict(codigo="DEMO-007", nombre="Queso Cremoso 500g", categoria_id=cat_lacteos, proveedor_id=prov_lacteos,
             precio_compra=2500, precio_venta=4200, stock_minimo=5, stock_maximo=25, stock_inicial=1000, unidad="unidad"),
    ]

    ids_por_codigo = {}
    precios_por_codigo = {}
    for p in productos_demo:
        pid = crear_producto(**p)
        ids_por_codigo[p["codigo"]] = pid
        precios_por_codigo[p["codigo"]] = p["precio_venta"]

    print(f"✔ {len(productos_demo)} productos creados")
    print()
    print("Generando historial de ventas simulado (esto tarda unos segundos)...")
    generar_historial_ventas(ids_por_codigo, precios_por_codigo)
    ajustar_stock_final()
    print("✔ Stock final ajustado para mostrar los 4 estados (normal/bajo/crítico/sin stock)")

    print()
    print("Datos de prueba cargados correctamente.")
    print("Iniciá sesión con usuario: admin / contraseña: admin123")
    print(" - Sección Productos: vas a ver los 4 estados de stock.")
    print(" - Sección Predicciones IA: Gaseosa Cola, Agua Mineral, Pan Lactal, Arroz y Leche")
    print("   tienen ~120 días de historial para entrenar el modelo.")
    print("   El Queso tiene historial muy escaso, y el Detergente no tiene historial:")
    print("   sirven para ver cómo el sistema avisa cuando los datos son insuficientes.")


if __name__ == "__main__":
    app = create_app()  # crea las tablas si no existen, y el usuario admin
    with app.app_context():
        limpiar_datos_de_prueba()
        cargar_datos()
