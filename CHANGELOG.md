# CHANGELOG - SIPOS

## [Fase 11] - 2026-10-15 - Rediseño de la interfaz

### Rediseño visual (a pedido: que no parezca generado por IA)
- Nueva identidad, pensada para un comercio: verde profundo para el menú y las acciones, mostaza solo para lo que pide atención, fondo gris verdoso suave. Se abandonó el estilo de fábrica de Bootstrap (menú azul oscuro, tarjetas iguales con sombra, verde turquesa).
- Tipografías: Archivo Narrow para títulos y cifras, IBM Plex Sans para el texto.
- Se eliminaron todos los emojis de la interfaz. Los íconos del menú pasan a ser íconos de línea (Bootstrap Icons) y el semáforo de stock (normal, bajo, crítico, sin stock) pasa a puntos de color con texto.
- Menos "cajitas": tablas con líneas finas directamente sobre el fondo, y paneles solo donde hace falta agrupar. Radios de borde distintos según el elemento.
- Menú lateral agrupado por tarea (inicio; ventas y compras; catálogo y stock; análisis; configuración) que se pliega en pantallas chicas.
- Pantalla de ingreso nueva, a pantalla completa, con panel de marca.
- Pantalla de Inicio rediseñada: arranca con "Para reponer esta semana" (usa la recomendación del módulo de IA), sigue con las cifras, los avisos y los cuatro gráficos. Saludo según la hora y fecha en castellano.
- Etiqueta de precio mostaza para la cantidad a comprar: es el único adorno del sistema y está a propósito sobre lo más importante.
- Todo el texto de la interfaz se revisó en un tono más directo.

### Formato argentino
- Plata: `$7.000` y `$1.234,50` (antes `$7000.00`). Cantidades sin ".0" sobrante. Fechas `14/10/2026`.
- Aplica a pantallas, carritos de venta y compra, y a los PDF, Excel y CSV exportados (que además muestran los estados con palabras en vez de `sin_stock`).
- Nuevo `utils/formato.py` con las funciones `pesos`, `cantidad`, `fecha` y `fecha_hora`, registradas como filtros de las plantillas.

### Otros cambios
- Nueva pantalla de Configuración (solo lectura) con los parámetros vigentes. Reemplaza al ítem apagado "(próx.)" del menú.
- La recomendación de reposición redondea hacia arriba la cantidad a comprar en productos que se venden por unidad, caja o paquete (antes podía recomendar "50,5" panes). Los productos por peso o volumen conservan decimales.
- `seed.py`: la leche de 1 L y el arroz de 1 kg pasan a venderse "por unidad", como en un estante real.
- Se eliminó el campo `icono` (emoji) de las alertas de `services/alertas.py`.
- Nuevos archivos: `templates/_componentes.html` (piezas reutilizables: enlace del menú, logo, semáforo), `templates/configuracion.html`, `routes/configuracion.py`.
- README reescrito por completo (estaba desactualizado): problema que resuelve, objetivos, arquitectura, base de datos, IA, instalación para CMD y PowerShell, usuario de prueba.

### Verificado
- Las 20 pantallas del sistema responden correctamente y no hay errores en el log del servidor.
- Semáforo con los 4 estados, reposición con cantidades enteras en productos por unidad, flujo completo de venta (comprobante, total y "Vendido hoy" coinciden), y PDF, Excel y CSV válidos con el nuevo formato.
- No quedan emojis, flechas ni puntos medios en plantillas, servicios, rutas, estilos ni scripts.
- Limitación: en el entorno de desarrollo no hay navegador, así que la apariencia no se pudo revisar con capturas; está pendiente de revisión visual en un navegador real.

### Pendiente
- Fase 12: pruebas finales y corrección de errores (incluye los ajustes visuales que surjan de la primera revisión en el navegador).

## [Fase 10] - 2026-10-06 - Reportes y exportaciones

### Agregado
- `services/reportes.py`: calcula los 8 reportes pedidos (ventas por período, productos más/menos vendidos, stock actual, stock crítico, compras por período, ventas por categoría, rentabilidad estimada), todos con la misma estructura de columnas/filas para poder reutilizar el código de exportación.
- Selector de período con los 5 presets pedidos: Hoy, Últimos 7 días, Este mes, Mes anterior, Rango personalizado.
- `services/exportacion.py`: exporta cualquier reporte a **PDF** (ReportLab), **Excel** (OpenPyXL, con encabezado destacado y ancho de columna automático) y **CSV** (con BOM UTF-8 para que Excel en Windows muestre bien los acentos).
- `routes/reportes.py` + `templates/reportes.html`: pantalla `/reportes` con el selector, la tabla en pantalla, y los 3 botones de descarga.
- Menú lateral: se habilita el link de Reportes.

### Decisiones técnicas
- El reporte de "Rentabilidad estimada" usa el precio de compra ACTUAL del producto (no el costo histórico real de cada compra puntual), porque el sistema no guarda ese dato por separado. Por eso el reporte se llama explícitamente "estimada": es una aproximación razonable para un comercio chico, no un cálculo contable exacto.
- "Productos menos vendidos" incluye también productos con 0 ventas en el período (no solo los que vendieron poco), para que sea realmente útil detectar qué no se está moviendo.

### Verificado (pruebas automáticas)
- Los 8 tipos de reporte cargan correctamente en pantalla.
- Los 3 formatos de exportación generan archivos reales y válidos (confirmado con el comando `file`: PDF real, Excel 2007+ real, CSV con acentos correctos).
- Un reporte sin datos (ej. ventas de "hoy" sin ventas registradas) muestra el mensaje correcto en pantalla y se puede exportar igual sin romperse.
- El rango de fechas personalizado funciona correctamente.

### Pendiente para próximas fases
- Mejoras de diseño y experiencia de usuario (Fase 11).
- Pruebas finales y corrección de errores (Fase 12).

## [Fase 9] - 2026-09-29 - Recomendación de reposición

### Agregado
- `services/reposicion.py`: calcula, para cada producto, `demanda_predicha (7 días) + stock_seguridad − stock_actual`. Si el resultado es mayor a 0, recomienda comprar esa cantidad; si no, indica que no hace falta reponer todavía.
- **Stock de seguridad** (sección 15 de la consigna): si el producto tiene suficiente historial, se calcula estadísticamente (`z × desviación estándar de la demanda diaria × √días de cobertura`), lo que tiene en cuenta qué tan irregular es la demanda de ESE producto en particular. Si no hay suficiente historial, se usa un método simplificado (mitad del stock mínimo) y se marca explícitamente como estimación, nunca como un cálculo estadístico real.
- `routes/prediccion.py`: nueva ruta `/predicciones/reposicion`.
- `templates/reposicion.html`: tabla con Producto, Stock actual, Stock mínimo, Demanda estimada, Stock recomendado, Cantidad a comprar y Prioridad (🔴Alta / 🟡Media / 🟢Baja), con un aviso visual (⚠️ estimado) en los productos donde el stock de seguridad se calculó con el método simplificado.
- Link "Ver recomendación de reposición" agregado en la pantalla de Predicciones IA.

### Verificado (pruebas automáticas)
- Con los datos de `seed.py`, Pan Lactal (sin stock, con historial real) recomendó reponer 49 unidades con prioridad Alta (demanda estimada 39.6 + stock de seguridad estadístico 9.4).
- Detergente (sin historial) se marcó correctamente con el aviso "⚠️ estimado" en lugar de mostrar un cálculo estadístico inexistente.
- Las 7 recomendaciones se ordenaron correctamente por prioridad (alta → media → baja).

### Pendiente para próximas fases
- Reportes exportables en PDF/Excel/CSV (Fase 10).
- Mejoras de diseño y UX (Fase 11).

## [Fase 8] - 2026-09-29 - Machine Learning y predicciones

### Agregado
- **Historial de ventas de prueba**: se extendió `seed.py` para generar ~120 días de ventas simuladas (con más ventas los fines de semana en varios productos), necesarias para entrenar el modelo. A propósito, el Detergente queda sin ningún historial y el Queso con historial muy escaso, para poder probar los casos de "datos insuficientes".
- Se agregó un parámetro `fecha` opcional en toda la cadena venta → movimiento de stock (`models/venta.py`, `models/movimiento_stock.py`, `services/inventario.py`, `services/ventas.py`), usado solo por `seed.py` para poder cargar ventas con fecha pasada.
- `ml/entrenamiento.py`: arma un dataset diario por producto (completando con 0 los días sin ventas) y entrena una **Regresión Lineal** por producto (modelo simple y explicable, como pide la consigna), evaluada con MAE sobre los últimos días. Los modelos se guardan todos juntos en `ml/modelo_stock.pkl`. Un producto con menos de 20 días con venta no se entrena (se considera con datos insuficientes).
- `ml/prediccion.py`: genera la predicción de demanda para 7 y 30 días. Si el producto no tiene modelo entrenado, usa un método simplificado (promedio de las ventas disponibles) y lo aclara explícitamente; si no tiene ninguna venta, informa que no se puede predecir nada, sin inventar números.
- `routes/prediccion.py` + `templates/predicciones.html`: pantalla `/predicciones` con selector de producto, gráfico de ventas históricas, resultado de la predicción (próximos 7 días, próximos 30 días, demanda estimada diaria), información del modelo (modelo utilizado, registros usados, error aproximado, fecha de entrenamiento, producto analizado), botón para reentrenar, y una sección "¿Cómo funciona la predicción?" pensada para poder explicarlo oralmente ante los docentes.
- Menú lateral: se habilita el link de Predicciones IA.
- `requirements.txt`: se agrega `joblib` de forma explícita (se usa directamente para guardar/cargar los modelos).

### Decisiones técnicas
- Se usa Regresión Lineal como primer modelo (tal como sugiere la consigna: "comenzar con un modelo sencillo y explicable"), con variables de fecha (día de la semana, día del mes, mes, días desde el inicio del historial). Queda como mejora futura evaluar Random Forest o Gradient Boosting y comparar el error contra este modelo base.
- El umbral de "datos suficientes" se fijó en 20 días con venta real (no simplemente días de calendario), para evitar entrenar un modelo con muy pocos puntos de datos reales aunque estén repartidos en un rango de fechas amplio.

### Verificado (pruebas automáticas)
- `seed.py` genera 478 ventas históricas en ~3 segundos.
- El entrenamiento generó modelos para 5 de los 7 productos (los 2 restantes quedaron correctamente afuera por datos insuficientes).
- Se probaron los 3 escenarios en la pantalla de predicciones: producto con buen historial (predicción con Regresión Lineal), producto con historial escaso (promedio simple, aclarado), producto sin ventas (mensaje de datos insuficientes, sin predicción numérica).
- El botón de reentrenar funciona, el gráfico histórico muestra datos reales, y el resto del sistema (Dashboard, Stock) sigue funcionando sin problemas.

### Pendiente para próximas fases
- Recomendación automática de cuánto reponer, combinando la predicción con el stock actual y un stock de seguridad (Fase 9).
- Reportes exportables en PDF/Excel/CSV (Fase 10).

## [Fase 7] - 2026-09-23 - Dashboard y gráficos

### Agregado
- `services/dashboard.py`: calcula las 7 tarjetas de resumen (total de productos, con stock bajo, sin stock, valor del inventario a precio de costo, ventas del día, ventas del mes, compras del mes) y los datos de los 4 gráficos, todo con consultas reales a la base de datos.
- `routes/dashboard.py` + `templates/dashboard.html`: reemplaza la pantalla temporal de verificación que se usaba desde la Fase 1. Incluye:
  - Gráfico 1: ventas de los últimos 7 días (incluye los días sin ventas, en 0).
  - Gráfico 2: productos más vendidos (histórico).
  - Gráfico 3: productos en stock crítico o agotados.
  - Gráfico 4: evolución de ventas de los últimos 6 meses.
  - Las 5 alertas más urgentes (reutilizando `services/alertas.py` de la Fase 6), con link a la pantalla de Stock para ver todas.
  - Los gráficos usan Chart.js (ya cargado desde la Fase 1) y se ocultan con un mensaje claro cuando todavía no hay datos suficientes (en vez de mostrar un gráfico vacío o inventado).
- Se eliminó `templates/fase1_ok.html` (ya no se usaba, estaba anunciado que se reemplazaría en esta fase).
- La ruta principal (`/`) ahora vive en `routes/dashboard.py` como `dashboard.index`, en vez de estar declarada directamente en `app.py`.

### Verificado (pruebas automáticas)
- Con los datos de `seed.py` más una venta de prueba, las tarjetas mostraron los números exactos esperados (7 productos, 3 con stock bajo, 1 sin stock, valor de inventario y ventas del día/mes coincidiendo con lo vendido).
- Los 4 gráficos recibieron datos correctos y ordenados (por ejemplo, el gráfico de stock crítico mostró primero el producto con menos stock).
- Arranque limpio de cero sin errores en el log.

### Pendiente para próximas fases
- Módulo de predicción de demanda con Machine Learning (Fase 8).
- Recomendación automática de reposición de stock (Fase 9).
- Reportes exportables en PDF/Excel/CSV (Fase 10).

## [Fase 6] - 2026-09-17 - Control de stock y alertas

### Agregado
- `services/alertas.py`: detecta automáticamente stock bajo, stock crítico, productos agotados, ventas inusualmente altas (comparando la última semana contra el promedio histórico) y productos con baja rotación (30 días sin ventas). Cuando no hay suficiente historial para un cálculo, esa alerta simplemente no se genera (nunca se inventan datos).
- `routes/stock.py` + `templates/stock.html`: pantalla de Stock que muestra las alertas activas y permite hacer un **ajuste manual** de stock sobre cualquier producto (sumar o restar, con motivo obligatorio). Todo ajuste se registra en `movimientos_stock` con tipo `AJUSTE`.
- `services/inventario.py` ya tenía `registrar_ajuste()` desde la Fase 5; en esta fase se lo conecta por primera vez a una pantalla real.
- Menú lateral: se habilita el link de Stock.

### Verificado (pruebas automáticas)
- Con los datos de `seed.py`, el sistema detecta correctamente las 4 alertas esperadas: 1 producto agotado (Pan Lactal), 1 en estado crítico (Queso), 2 en estado bajo (Gaseosa Cola, Detergente).
- Un ajuste manual válido (con motivo) descuenta el stock correctamente y queda en el historial del producto con su motivo.
- Un ajuste sin motivo se rechaza y no modifica el stock.

### Pendiente para próximas fases
- Mostrar las alertas también en el Dashboard principal, con gráficos (Fase 7).
- Módulo de predicción de demanda con Machine Learning (Fase 8).

## [Fase 5] - 2026-09-11 - Ventas y compras

### Agregado
- `services/inventario.py`: punto único para modificar stock (`registrar_entrada`, `registrar_salida`, `registrar_ajuste`). Toda modificación de stock queda siempre registrada en `movimientos_stock`, sin excepciones.
- `services/ventas.py`: `confirmar_venta()` valida stock disponible, crea la venta y descuenta stock, todo o nada (si algo falla al descontar, se revierte la venta).
- `services/compras.py`: `confirmar_compra()` crea la compra y aumenta el stock.
- `routes/ventas.py` + `templates/venta_pos.html`: punto de venta con carrito armado en el navegador (buscar producto, agregar, modificar cantidad, elegir cliente y método de pago), confirmado por AJAX sin recargar la página.
- `routes/compras.py` + `templates/compra_form.html`: mismo esquema para compras, con precio de compra editable por línea.
- `templates/venta_detalle.html` y `templates/compra_detalle.html`: comprobantes.
- `templates/ventas.html` y `templates/compras.html`: listados.
- `config.py`: nueva variable `PERMITIR_STOCK_NEGATIVO` (por defecto `False`) para decidir si se puede vender sin stock suficiente.
- Menú lateral: se habilitan los links de Ventas y Compras.

### Decisiones técnicas
- El carrito de venta/compra se arma 100% en el navegador con JavaScript simple (sin frameworks), y recién se manda al servidor al confirmar. Esto evita crear registros a medias en la base de datos mientras el usuario todavía está eligiendo productos.
- Si el descuento/aumento de stock fallara después de haber creado la venta o compra (caso muy raro, pero posible), el sistema revierte automáticamente la venta/compra para no dejar datos inconsistentes.

### Verificado (pruebas automáticas de punta a punta)
1. Confirmar una venta válida descuenta el stock correctamente (4 → 2 unidades).
2. Intentar vender más cantidad de la disponible se rechaza (HTTP 400) sin modificar el stock ni crear la venta.
3. Confirmar una compra aumenta el stock correctamente (2 → 12 unidades).
4. Los comprobantes de venta y compra muestran los datos correctos.
5. El historial de movimientos del producto muestra tanto la SALIDA (venta) como la ENTRADA (compra), con la referencia correcta ("Venta #1", "Compra #1").

### Pendiente para próximas fases
- Alertas automáticas de stock bajo/crítico visibles en el dashboard (Fase 6-7).
- Ajuste manual de stock desde la pantalla de Stock (Fase 6).
- Dashboard con gráficos reales (Fase 7).

## [Fase 4] - 2026-09-10 - CRUD de productos, categorías, proveedores y clientes

### Agregado
- `routes/categorias.py` + `templates/categorias.html`: listar, crear, editar, eliminar (con modales de Bootstrap).
- `routes/proveedores.py` + `templates/proveedores.html`: listar, crear, editar, activar/desactivar (no se elimina un proveedor con historial).
- `routes/clientes.py` + `templates/clientes.html`: listar, crear, editar, eliminar.
- `routes/productos.py` + `templates/productos.html` + `templates/producto_form.html` + `templates/producto_movimientos.html`: CRUD completo de productos con:
  - Búsqueda por nombre/código y filtros por categoría/proveedor.
  - Tabla con Código, Producto, Categoría, Precio, Stock, Stock mínimo, Estado (🟢🟡🔴⚫) y Acciones.
  - Activar/desactivar (no se elimina un producto con historial).
  - Pantalla de historial de movimientos de stock por producto.
- `templates/base.html`: se agregó el menú lateral (Dashboard, Productos, Categorías, Proveedores, Clientes ya funcionan; Ventas/Compras/Stock/Predicciones/Reportes/Configuración aparecen deshabilitados hasta sus fases correspondientes, para no tener links rotos).
- `templates/fase1_ok.html`: ahora es una mini página de inicio con accesos directos a las 4 secciones nuevas.
- `seed.py`: carga datos de prueba (4 categorías, 3 proveedores, 3 clientes, 7 productos con distintos niveles de stock para poder ver los 4 estados). Se puede correr varias veces sin duplicar datos. Todos los productos de prueba usan el prefijo de código `DEMO-` para identificarse claramente como datos de prueba.

### Verificado (pruebas automáticas)
- Los 4 listados muestran los datos de `seed.py` correctamente.
- Crear categoría funciona; crear una categoría con nombre repetido se rechaza correctamente (restricción UNIQUE) sin romper la página.
- Filtrar productos por categoría funciona.
- Crear, editar, desactivar/activar un producto funcionan; un producto desactivado desaparece del listado normal pero se puede ver tildando "Mostrar también productos desactivados".
- El historial de movimientos de un producto sin movimientos muestra el mensaje correcto (todavía no hay ventas/compras que generen movimientos, eso es la Fase 5-6).

### Pendiente para próximas fases
- Módulo de ventas (punto de venta) y compras, con descuento/aumento automático de stock (Fase 5).
- Alertas automáticas de stock bajo/crítico en el dashboard (Fase 6-7).
- Ampliar `seed.py` con historial de ventas para poder probar el módulo de predicción (Fase 8).

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
