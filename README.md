# SIPOS: Sistema Inteligente de Predicción y Optimización de Stock

## Descripción
SIPOS es un sistema web para que pequeños y medianos comercios controlen su inventario, analicen sus ventas y decidan qué conviene reponer. Incluye un módulo de Machine Learning que predice la demanda de cada producto y recomienda cuánto comprar.

Proyecto académico de la Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial.

## Problema que resuelve
Un comercio chico suele llevar el stock "de memoria" o en planillas: se queda sin mercadería que se vende mucho, o compra de más productos que casi no rotan. SIPOS reemplaza esa intuición por datos: muestra qué hay, qué se vende, qué está por agotarse y cuánto conviene comprar.

## Objetivo general
Desarrollar un sistema web funcional que ayude a un comercio a controlar su inventario y a tomar mejores decisiones de reposición, usando el historial de ventas como base.

## Objetivos específicos
- Registrar productos, categorías, proveedores, clientes, compras y ventas.
- Mantener el stock actualizado de forma automática y dejar registro de cada movimiento.
- Avisar cuando un producto está agotado, en nivel crítico o bajo.
- Mostrar el estado del negocio en un panel de inicio con cifras y gráficos.
- Predecir la demanda de cada producto con un modelo de Machine Learning explicable.
- Recomendar la cantidad a reponer, con un margen de seguridad calculado a partir de los datos.
- Generar reportes exportables a PDF, Excel y CSV.

## Estado del desarrollo
Completadas las fases 1 a 11 (arquitectura, base de datos, autenticación, altas y bajas, ventas y compras, control de stock y alertas, panel de inicio, Machine Learning, recomendación de reposición, reportes y diseño de la interfaz). Pendiente la fase 12: pruebas finales y corrección de errores.

## Tecnologías utilizadas
- **Backend:** Python 3.12 o superior, Flask.
- **Base de datos:** SQLite, accedida con el módulo estándar `sqlite3` (ver nota técnica).
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js, Bootstrap Icons.
- **Machine Learning:** Pandas, NumPy, scikit-learn, joblib.
- **Reportes:** ReportLab (PDF), OpenPyXL (Excel), módulo `csv` de Python.

### Nota técnica sobre la base de datos
La consigna permitía usar "SQLAlchemy o sqlite3". Se eligió `sqlite3` (librería estándar de Python) en lugar de `Flask-SQLAlchemy` porque simplifica la instalación (una dependencia menos) y alcanza de sobra para el volumen de datos de un comercio chico o mediano. Todas las consultas usan parámetros (`?`) para evitar inyección SQL. El acceso a la base está centralizado en `utils/database.py`: si en el futuro se quisiera migrar a SQLAlchemy, solo habría que reemplazar ese archivo.

## Arquitectura
```
SIPOS/
├── app.py                  Punto de entrada de la aplicación Flask
├── config.py               Configuración centralizada (lee el archivo .env)
├── seed.py                 Carga de datos de prueba
├── requirements.txt
├── .env.example            Plantilla de variables de entorno
├── database/
│   ├── schema.sql          Definición de las tablas
│   └── sipos.db            Base de datos (se genera al arrancar)
├── models/                 Acceso a datos de cada entidad
├── routes/                 Pantallas y endpoints (un archivo por sección)
├── services/               Lógica de negocio: inventario, ventas, compras,
│                           alertas, reposición, reportes, exportación
├── ml/
│   ├── entrenamiento.py    Arma el dataset y entrena los modelos
│   ├── prediccion.py       Genera las predicciones
│   └── modelo_stock.pkl    Modelos entrenados (se genera al entrenar)
├── templates/              Vistas HTML (Jinja2)
├── static/
│   ├── css/style.css       Estilos propios de SIPOS
│   └── js/app.js           Menú y estilo de los gráficos
└── utils/
    ├── database.py         Conexión centralizada a SQLite
    ├── helpers.py          Protección de rutas (login)
    └── formato.py          Formato argentino de plata, números y fechas
```

## Base de datos
SQLite, con 10 tablas: `usuarios`, `categorias`, `proveedores`, `clientes`, `productos`, `ventas`, `detalle_ventas`, `compras`, `detalle_compras` y `movimientos_stock`. Tienen claves foráneas e índices; el esquema completo está en `database/schema.sql` y se crea solo al arrancar la aplicación. Cada cambio de stock (venta, compra o ajuste manual) queda registrado en `movimientos_stock`.

## Funcionamiento
- **Inicio:** arranca con los productos que conviene reponer esta semana, y sigue con las cifras del negocio, los avisos y cuatro gráficos.
- **Productos, categorías, proveedores y clientes:** altas, ediciones y bajas. Los productos con historial se desactivan en vez de borrarse.
- **Ventas y compras:** se arma un carrito en pantalla; al confirmar, el stock se actualiza solo. No se puede vender más de lo que hay (se puede cambiar en la configuración).
- **Stock:** avisos automáticos y ajustes manuales con motivo obligatorio.
- **Predicciones IA:** predicción de demanda por producto y tabla de reposición recomendada.
- **Reportes:** ocho reportes con período a elección, exportables a PDF, Excel y CSV.
- **Configuración:** muestra los parámetros con los que funciona el sistema.

## Diseño de la interfaz
Pensada para un comerciante que mira la pantalla entre cliente y cliente. Verde profundo para el menú y las acciones principales, mostaza solo para lo que pide atención, y un semáforo de stock con puntos de color y texto. Los títulos usan la tipografía Archivo Narrow y el texto IBM Plex Sans. El menú se pliega en pantallas chicas. Los números, la plata y las fechas se muestran en formato argentino.

## Inteligencia Artificial utilizada
**Modelo:** Regresión Lineal (scikit-learn), entrenada por separado para cada producto.

**Variables (features):** día de la semana, día del mes, mes, y días transcurridos desde el inicio del historial de ese producto (para captar tendencia).

**Datos de entrenamiento:** serie diaria de "unidades vendidas por día" por producto, construida a partir de `detalle_ventas` + `ventas`, completando con 0 los días sin ventas. Se requieren al menos 20 días con venta real para entrenar un modelo; por debajo de eso, el sistema usa un promedio simple y lo aclara explícitamente (nunca se presenta una predicción como certeza con datos insuficientes).

**Evaluación:** se separan los últimos días como conjunto de prueba y se calcula el error absoluto medio (MAE) comparando la predicción contra lo que realmente se vendió.

**Dónde se ve en el sistema:** pantalla `/predicciones` (menú "Predicciones IA"), con selector de producto, gráfico de historial, predicción a 7 y 30 días, información del modelo, y una explicación en lenguaje simple de cómo funciona.

**Código:** `ml/entrenamiento.py` (entrenamiento) y `ml/prediccion.py` (predicción).

## Instalación
Los comandos funcionan en el Símbolo del sistema (CMD) y en PowerShell, salvo donde se indica.

1. **Descargar el proyecto** y descomprimir el `.zip`. Entrar a la carpeta interna que contiene `app.py`.
2. **Abrir la carpeta en Visual Studio Code** (Archivo, Abrir carpeta).
3. **Crear el entorno virtual:**
   ```
   python -m venv venv
   ```
4. **Activarlo:**
   - CMD: `venv\Scripts\activate.bat`
   - PowerShell: `.\venv\Scripts\Activate.ps1` (si bloquea la ejecución, correr una vez `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)

   La línea de la terminal tiene que empezar con `(venv)`.
5. **Instalar las dependencias:**
   ```
   pip install -r requirements.txt
   ```
6. **Crear el archivo de configuración:**
   ```
   copy .env.example .env
   ```
7. **Cargar los datos de prueba** (crea la base de datos y unos 120 días de ventas simuladas; tarda unos segundos):
   ```
   python seed.py
   ```
8. **Entrenar los modelos de predicción** (opcional: también se puede hacer desde la pantalla Predicciones IA):
   ```
   python -m ml.entrenamiento
   ```
9. **Ejecutar la aplicación:**
   ```
   python app.py
   ```
10. **Abrir el navegador** en `http://127.0.0.1:5000` e iniciar sesión.

Se necesita conexión a internet al usar el sistema: las tipografías, los íconos, Bootstrap y Chart.js se cargan desde la red.

## Usuario de prueba
- Usuario: `admin`
- Contraseña: `admin123` (se guarda con hash, nunca en texto plano)

Los datos de prueba están identificados con el prefijo `DEMO-` en el código de cada producto. El Detergente no tiene historial de ventas y el Queso tiene muy poco, a propósito, para ver cómo avisa el sistema cuando los datos no alcanzan para predecir.

## Posibles mejoras futuras
- Autenticación multi-comercio para que varios negocios usen el mismo sistema.
- Notificaciones automáticas (correo o WhatsApp) ante stock crítico.
- Edición de la configuración desde la propia pantalla.
- Modelos de ML más avanzados (series de tiempo, Random Forest, Gradient Boosting) comparados contra la regresión lineal base cuando haya más datos reales.
- Registro del costo histórico de cada compra, para calcular la rentabilidad con exactitud.
