# Diseño del Dashboard — Plato's Pizza 2015

## Archivos a importar en Power BI

Importar desde `data/clean/` — todos como CSV, encoding UTF-8:

| Archivo | Rol en el modelo |
|---------|-----------------|
| `pizza_features.csv` | Tabla de hechos principal |
| `agg_monthly.csv` | Tabla de agregación mensual |
| `agg_daily.csv` | Tabla de agregación por día |
| `agg_hourly.csv` | Tabla de agregación por hora |
| `agg_pizza_performance.csv` | Tabla de performance por pizza |
| `agg_category_size.csv` | Tabla de tallas por categoría |
| `agg_tickets.csv` | Tabla de tickets (distribución) |
| `agg_weekly.csv` | Tabla de tendencia semanal |

> En este dashboard NO se construyen relaciones entre tablas en Power BI —
> cada tabla `agg_*` ya está agregada y es independiente. Se usan directamente en los visuales.
> La única tabla de hechos con granularidad completa es `pizza_features.csv`.

---

## Estructura del Dashboard — 3 páginas

### Página 1: Resumen Ejecutivo
**Audiencia:** Dueño/gerente. Ve el negocio completo en 30 segundos.

### Página 2: Operaciones
**Audiencia:** Gerente operativo. Cuándo y cómo trabaja el restaurante.

### Página 3: Menú & Productos
**Audiencia:** Dueño. Qué pizzas potenciar, cuáles revisar.

---

## PÁGINA 1 — Resumen Ejecutivo

### Fila 1 — KPI Cards (5 tarjetas)
Usar visual "Card" de Power BI. Fuente: `pizza_features.csv`

| Tarjeta | Campo | Formato |
|---------|-------|---------|
| Revenue Total | `SUM(pizza_features[revenue])` | $817,860 |
| Total Pedidos | `DISTINCTCOUNT(pizza_features[order_id])` | 21,350 |
| Pizzas Vendidas | `SUM(pizza_features[quantity])` | 49,574 |
| Ticket Promedio | Medida DAX (ver abajo) | $38.31 |
| Pedidos/Día | Medida DAX (ver abajo) | 59.6 |

**Medidas DAX necesarias:**
```
Ticket Promedio =
AVERAGEX(
    VALUES(pizza_features[order_id]),
    CALCULATE(SUM(pizza_features[revenue]))
)

Pedidos Por Dia =
DIVIDE(
    DISTINCTCOUNT(pizza_features[order_id]),
    DISTINCTCOUNT(pizza_features[date])
)
```

### Fila 2 — Gráficas principales

**Visual A — Tendencia de Revenue Mensual** (60% del ancho)
- Tipo: Line chart
- Fuente: `agg_monthly.csv`
- Eje X: `month_name` (ordenar por `month`)
- Eje Y: `revenue`
- Línea de referencia: promedio mensual ($68,155)
- Título: "Revenue mensual — tendencia 2015"

**Visual B — Revenue por Categoría** (40% del ancho)
- Tipo: Donut chart (no pie)
- Fuente: `pizza_features.csv`
- Valores: `SUM(revenue)`
- Leyenda: `category`
- Colores sugeridos: Classic=azul, Chicken=naranja, Supreme=rojo, Veggie=verde
- Título: "Distribución de revenue por categoría"

### Fila 3 — Contexto adicional

**Visual C — Revenue por Día de la Semana** (50% del ancho)
- Tipo: Bar chart horizontal
- Fuente: `agg_daily.csv`
- Eje Y: `day_name_es` (ordenar por `day_of_week`)
- Eje X: `orders`
- Highlight: Viernes con color diferente
- Título: "Pedidos por día — Viernes lidera con 3,538"

**Visual D — Tabla de días cerrados** (50% del ancho)
- Tipo: Table o Card con texto
- Nota: El restaurante operó 358 de 365 días
- Texto fijo: "7 días sin operación: 4 lunes de Oct + Sep 24-25 + Dic 25"

---

## PÁGINA 2 — Operaciones

### Fila 1 — KPIs operativos (3 tarjetas)

| Tarjeta | Valor |
|---------|-------|
| Hora Pico | 12:00h — 2,520 pedidos |
| Día Más Activo | Viernes — 3,538 pedidos |
| Días Operados | 358 días |

### Fila 2 — Heatmap de actividad (visual principal, ancho completo)

**Visual E — Pedidos por Hora y Día** (si tienes Power BI Pro o Premium)
- Tipo: Matrix heatmap
- Filas: `day_name_es` (ordenar por `day_of_week`)
- Columnas: `hour`
- Valores: `DISTINCTCOUNT(order_id)`
- Color: gradiente blanco → rojo oscuro
- Fuente: `pizza_features.csv`
- Título: "Mapa de calor — actividad por hora y día"

> Si no tienes la visual de heatmap: usar Matrix nativa de Power BI con formato condicional por color.

### Fila 3 — Detalle de horarios

**Visual F — Área de Pedidos por Hora** (60% del ancho)
- Tipo: Area chart
- Fuente: `agg_hourly.csv`
- Eje X: `hour`
- Eje Y: `orders`
- Anotación: marcar hora 12 como pico
- Título: "Distribución de pedidos por hora del día"

**Visual G — Bloques Horarios** (40% del ancho)
- Tipo: Bar chart vertical
- Fuente: `pizza_features.csv` con columna `time_block`
- Eje X: `time_block`
- Eje Y: `DISTINCTCOUNT(order_id)`
- Ordenar: por volumen descendente
- Título: "Almuerzo y noche = 61% de los pedidos"

### Fila 4 — Tendencia semanal

**Visual H — Revenue por Semana del Año** (ancho completo)
- Tipo: Line chart
- Fuente: `agg_weekly.csv`
- Eje X: `week`
- Eje Y: `revenue`
- Destacar semanas de baja (semanas 38-39 = Sep cierre, semanas 40-43 = Oct lunes cerrados)
- Título: "Revenue semanal — identificar semanas atípicas"

---

## PÁGINA 3 — Menú & Productos

### Fila 1 — KPIs de menú (3 tarjetas)

| Tarjeta | Valor |
|---------|-------|
| Pizzas en Menú | 32 tipos · 96 SKUs |
| Pizza Top Revenue | Thai Chicken — $43,434 |
| Pizza Top Unidades | Classic Deluxe — 2,453 uds |

### Fila 2 — Ranking de pizzas (visual principal)

**Visual I — Bar chart horizontal de Revenue por Pizza** (55% del ancho)
- Tipo: Bar chart horizontal
- Fuente: `agg_pizza_performance.csv`
- Eje Y: `name`
- Eje X: `revenue`
- Colorear por `abc_class` (A=verde, B=amarillo, C=rojo)
- Ordenar: descendente por revenue
- Mostrar todas las 32 pizzas (scroll)
- Título: "Revenue por pizza — clasificación ABC"

**Visual J — Scatter: Revenue vs Unidades** (45% del ancho)
- Tipo: Scatter chart
- Fuente: `agg_pizza_performance.csv`
- Eje X: `qty` (unidades vendidas)
- Eje Y: `revenue`
- Tamaño de punto: `orders`
- Leyenda de color: `category`
- Anotar manualmente: Brie Carre (outlier abajo-izquierda)
- Título: "Volumen vs Revenue — detectar outliers de menú"

### Fila 3 — Análisis por categoría y talla

**Visual K — Talla más popular por categoría** (50% del ancho)
- Tipo: Stacked bar chart
- Fuente: `agg_category_size.csv`
- Eje X: `category`
- Valores apilados: `qty` por `size_label`
- Ordenar tallas por `size_order`
- Título: "Chicken prefiere Large · Classic prefiere Small"

**Visual L — Tabla de performance detallada** (50% del ancho)
- Tipo: Table con formato condicional
- Fuente: `agg_pizza_performance.csv`
- Columnas: `name`, `category`, `revenue`, `qty`, `abc_class`
- Formato condicional en `revenue`: barra de datos
- Ordenar: por `revenue_rank`
- Título: "Performance completa del menú"

---

## Filtros / Slicers (presentes en todas las páginas)

Máximo 3 slicers visibles por página — regla de la receta:

| Slicer | Tipo | Opciones |
|--------|------|----------|
| Mes | Dropdown o lista | Jan–Dec (ordenar por `month`) |
| Categoría | Botones | Classic · Chicken · Supreme · Veggie |
| Día de semana | Lista | Lunes a Domingo (ordenar por `day_of_week`) |

> El slicer de mes y categoría se puede poner en todas las páginas.
> El slicer de día aplica más a Operaciones.

---

## Paleta de colores sugerida

| Elemento | Color HEX | Uso |
|----------|-----------|-----|
| Classic | `#2E75B6` | Azul corporativo |
| Chicken | `#ED7D31` | Naranja cálido |
| Supreme | `#C00000` | Rojo oscuro |
| Veggie | `#70AD47` | Verde |
| Acento positivo | `#00B050` | Crecimiento, A-class |
| Acento negativo | `#FF0000` | Bajo rendimiento, C-class |
| Neutro | `#A6A6A6` | Gris para contexto |
| Fondo | `#F2F2F2` | Gris muy claro |

---

## Checklist antes de publicar el dashboard

- [ ] Todos los KPIs validados contra el notebook 04_analysis.ipynb
- [ ] Revenue total del dashboard = $817,860.05
- [ ] Total pedidos = 21,350
- [ ] Los slicers no generan dobles conteos
- [ ] Los meses están ordenados Ene–Dic (no alfabético)
- [ ] Las tallas están ordenadas S–M–L–XL–XXL (usando `size_order`)
- [ ] Los días están ordenados Lun–Dom (usando `day_of_week`)
- [ ] El título de cada gráfica dice la conclusión, no solo la descripción
- [ ] Alguien sin contexto entiende la página 1 en menos de 30 segundos
