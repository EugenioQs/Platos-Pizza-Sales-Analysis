# Diario de Proceso Analítico — Plato's Pizza

> Este archivo documenta el **cómo** detrás de cada decisión del proyecto:
> de dónde viene la información, qué razonamiento se usó, y por qué se tomó cada camino.
> Se actualiza al final de cada fase.

---

## FASE 1 — Entender el Contexto

### Fuentes de información usadas
1. **Notion — "La Receta del Data Analyst"**: framework metodológico con las preguntas que hay que responder en esta fase.
2. **Notion — "Dataset Seleccionado — Pizza Place Sales"**: página con contexto del cliente (Plato's Pizza), preguntas de negocio sugeridas y advertencias del dataset.
3. **`data_dictionary.csv`** + los 4 CSV del dataset: estructura de datos disponible.

---

### 1.1 — ¿Cómo se identificó al stakeholder?

**Fuente:** Página de Notion del dataset (Maven Analytics).

Maven Analytics, al publicar este dataset, lo presentó como un reto de negocio real:
*"Plato's Pizza quiere usar sus datos para mejorar sus operaciones"*. Eso define al stakeholder
como el **dueño o gerente del restaurante**, no como un analista técnico ni un equipo de IT.

**Razonamiento:** El stakeholder se identifica preguntando *"¿quién toma decisiones con este dato?"*.
En un restaurante, las decisiones de menú, horarios y personal las toma la gerencia — no el cocinero
ni el cajero. Por eso el stakeholder es la **dirección del negocio**.

---

### 1.2 — ¿Cómo se construyó la oración de decisión de negocio?

**Fuente:** Las preguntas sugeridas en Notion + la estructura de las tablas disponibles.

La oración de decisión se construye conectando dos cosas:
- **Qué datos tenemos:** ventas por tiempo (fecha/hora), por producto (pizza, tamaño, categoría) y por volumen (cantidad, precio).
- **Qué puede hacer el negocio con eso:** ajustar el menú, planificar turnos de personal, enfocar promociones.

La oración resultante fue:
> *"Quiero optimizar mis operaciones y menú para el próximo año: saber qué pizzas potenciar,
> cuándo necesito más personal, y si hay productos que debería eliminar."*

**Regla aplicada:** Una buena oración de decisión tiene siempre un **verbo de acción**
("optimizar", "eliminar", "potenciar") — no solo una descripción ("entender las ventas").
Si la oración no implica que alguien va a hacer algo diferente después de leer el análisis,
no es una decisión de negocio, es solo curiosidad.

---

### 1.3 — ¿Cómo se priorizaron las preguntas de análisis?

**Fuente:** 8 preguntas sugeridas en Notion. Se seleccionaron 5 prioritarias.

**Criterio de priorización — 3 filtros:**

1. **¿Responde directamente la oración de decisión?**
   - "¿Cuáles son nuestros bestsellers y cuáles deberíamos quitar del menú?" → SÍ (menú)
   - "¿Cuántos clientes por día? ¿Hay horas pico?" → SÍ (personal/operaciones)
   - "¿Cuál tamaño es más popular por categoría?" → NO directamente (es detalle secundario)

2. **¿Es respondible con los datos disponibles?**
   Todas las preguntas son respondibles porque tenemos fecha, hora, producto, precio y cantidad.
   No hay preguntas que requieran datos que no tenemos (ej. datos de clientes individuales,
   costos de ingredientes, o datos de competencia).

3. **¿Produce un insight accionable?**
   - "¿Hay estacionalidad en ingresos?" → Accionable: ajustar inventario y promociones por temporada.
   - "¿Cuántas pizzas lleva un pedido en promedio?" → Menos accionable por sí sola; se deja como secundaria.

**Las 5 preguntas prioritarias elegidas:**
1. ¿Cuánto dinero generamos por mes? ¿Hay estacionalidad? *(Ingresos)*
2. ¿Cuáles son nuestros bestsellers y cuáles deberíamos quitar del menú? *(Menú)*
3. ¿Cuántos clientes atendemos por día? ¿Hay horas pico? *(Operaciones)*
4. ¿Cuál es el ticket promedio por pedido? *(Ingresos)*
5. ¿Qué días de la semana vendemos más? *(Operaciones)*

---

### Decisiones y supuestos documentados

| Decisión | Razonamiento | Supuesto asumido |
|----------|-------------|------------------|
| Stakeholder = gerente/dueño | Es quien toma decisiones de menú y operaciones | El dataset simula un negocio real con un tomador de decisiones único |
| Año de análisis = 2015 completo | Es la cobertura total del dataset | Los datos son completos y representativos de un año normal de operación |
| Unidad de análisis = pedido (order) | La pregunta de negocio es operacional, no de cliente individual | No hay datos de clientes únicos (sin ID de cliente en el dataset) |

---

*Última actualización: Fase 1 completada*

---

## FASE 2 — Exploración Inicial (EDA Rápido)

### Fuentes de información usadas
1. **Lectura directa de los 4 CSV** con la herramienta Read (primeras y últimas filas).
2. **`data_dictionary.csv`** para validar el significado oficial de cada columna.
3. Cálculos manuales simples (divisiones, conteos) para obtener métricas de volumen.

---

### 2.1 — Primer vistazo: shape y estructura

| Tabla | Filas | Columnas | Observación inmediata |
|-------|-------|----------|-----------------------|
| `orders` | 21,350 | 3 | `order_id`, `date`, `time` — estructura muy limpia |
| `order_details` | 48,620 | 4 | Tabla principal de análisis |
| `pizzas` | 96 | 4 | Catálogo de combinaciones tipo+tamaño |
| `pizza_types` | 32 | 4 | Catálogo maestro de pizzas |

**¿Cómo se obtuvo el shape?**
No se usó Python todavía — se contaron las filas leyendo la primera y última línea de cada archivo.
`order_id` va de 1 a 21,350 (sin saltos visibles) y `order_details_id` de 1 a 48,620. Eso confirma
que los IDs son secuenciales y el conteo de filas es confiable.

**Cobertura temporal confirmada:**
- Primera orden: `2015-01-01` a las `11:38:36`
- Última orden: `2015-12-31` a las `23:02:05`
- = 365 días completos del año 2015 ✓

---

### 2.2 — Diccionario de datos

**Fuente:** `data_dictionary.csv` (archivo raíz del proyecto).

Hallazgo importante en la descripción de `ingredients`:
> *"they all include Mozzarella Cheese, even if not specified; and they all include Tomato Sauce, unless another sauce is specified"*

**Implicación analítica:** La columna `ingredients` no es exhaustiva — hay ingredientes implícitos.
Si en Fase 4 se analiza uso de ingredientes, habrá que agregar Mozzarella a todas las pizzas
y Tomato Sauce a las que no tengan otra salsa especificada.

**Hallazgo en `order_details.quantity`:**
> *"pizzas of the same type and size are kept in the same row, and the quantity increases"*

**Implicación:** No confundir número de filas en `order_details` (48,620) con pizzas vendidas.
El total de pizzas vendidas = `SUM(quantity)`, que puede ser mayor a 48,620.

---

### 2.3 — Problemas detectados a simple vista

#### Problema 1 — `brie_carre` solo tiene talla S
`pizzas.csv` muestra que todas las pizzas tienen S, M y L — excepto `brie_carre` que solo tiene S.
`the_greek` además tiene XL ($25.50) y XXL ($35.95), únicos en el menú.

**¿Por qué importa?** Si se analiza popularidad por talla, estas pizzas distorsionan el conteo.
`brie_carre` nunca puede aparecer en talla M o L aunque sea popular — no es que se venda poco en esos
tamaños, es que no existe en esos tamaños.

**Decisión de Fase 3:** Documentar como característica del menú, no como error. No se modifica.

#### Problema 2 — Encoding en `pizza_types.ingredients`
`calabrese` tiene: `"ÑDuja Salami"` → debería ser `"'Nduja Salami"` (salchicha italiana).
Es un problema de encoding UTF-8 al leer el archivo.

**Decisión de Fase 3:** Corregir al limpiar. No afecta análisis de ventas pero sí si se analiza ingredientes.

#### Problema 3 — Líneas vacías al final de los CSV
`pizzas.csv` y `pizza_types.csv` tienen una línea vacía como última fila.

**Decisión de Fase 3:** Limpiar con `dropna(how='all')` al cargar en Pandas. No afecta datos.

#### Problema 4 — `quantity` puede ser > 1 (pendiente de verificar)
El diccionario confirma que quantity puede acumular varias unidades en una fila.
No se ha verificado aún el rango real de valores (¿hay 0s? ¿negativos? ¿valores extremos?).

**Pendiente:** Verificar en Fase 3 con `df['quantity'].describe()` y `value_counts()`.

---

### Métricas derivadas (calculadas manualmente)

| Métrica | Cálculo | Resultado |
|---------|---------|-----------|
| Promedio de líneas de detalle por pedido | 48,620 / 21,350 | ~2.28 líneas/pedido |
| Promedio de pedidos por día | 21,350 / 365 | ~58.5 pedidos/día |
| Tipos de pizza únicos | Conteo `pizza_types` | 32 tipos |
| Combinaciones tipo × talla | Conteo `pizzas` | 96 SKUs |
| Rango de precios | Min-Max `pizzas.price` | $9.75 – $35.95 |

**Nota sobre "2.28 líneas/pedido":** Este número no es igual a "pizzas por pedido" porque
quantity puede ser > 1. El promedio real de pizzas por pedido se calculará en Fase 5.

---

### Decisiones y supuestos documentados

| Decisión | Razonamiento | Supuesto asumido |
|----------|-------------|------------------|
| No usar Python en Fase 2 | El shape y estructura son verificables leyendo filas clave | Los IDs son secuenciales sin saltos — verificar en Fase 3 |
| `brie_carre` S-only = intencional | No es un error de datos, es una característica del menú | El dataset refleja fielmente el menú real |
| Encoding de calabrese = error de carga | El carácter "Ñ" no tiene sentido en un nombre italiano | El CSV original fue exportado sin encoding UTF-8 correcto |

---

*Última actualización: Fase 2 completada*

---

## FASE 3 — Limpieza de Datos

### Fuentes de información usadas
1. Hallazgos documentados en Fase 2 (lista de problemas identificados).
2. Lectura directa de `data_dictionary.csv` para entender el comportamiento esperado de `quantity`.
3. Conocimiento del modelo relacional para diseñar el JOIN final.

---

### ¿Por qué se crea una tabla maestra unificada?

Las preguntas de negocio de Fase 1 requieren cruzar información de las 4 tablas:
- "¿Cuánto dinero por mes?" → necesita `date` (orders) + `price` (pizzas) + `quantity` (order_details)
- "¿Cuáles son los bestsellers?" → necesita `name` y `category` (pizza_types) + `quantity` (order_details)
- "¿Horas pico?" → necesita `time` (orders) + `quantity` (order_details)

En lugar de repetir el JOIN en cada análisis, se construye una sola vez aquí y se guarda como `pizza_data_clean.csv`.
Esto es más confiable y evita errores al repetir el merge en distintos notebooks.

---

### ¿Cómo se diseñó el JOIN?

La tabla central es `order_details` (la que tiene más filas y conecta todo).
Se hace LEFT JOIN desde `order_details` hacia las demás:

```
order_details
  → LEFT JOIN orders       ON order_id       (agrega date, time)
  → LEFT JOIN pizzas       ON pizza_id       (agrega size, price, pizza_type_id)
  → LEFT JOIN pizza_types  ON pizza_type_id  (agrega name, category, ingredients)
```

Se usa LEFT JOIN (no INNER JOIN) para detectar huérfanos: si una fila de `order_details`
no encuentra match, aparece como null en las columnas del JOIN — lo que dispara una alerta
en el sanity check posterior.

**Sanity check diseñado:** `assert len(df) == len(order_details)` — si el JOIN produce más
filas que order_details, significa que hay duplicados en las tablas de dimensión (pizzas o orders),
lo que sería un error de datos grave.

---

### ¿Por qué se agrega la columna `revenue` en esta fase?

`revenue = price × quantity` es la métrica más fundamental del análisis.
Se calcula en limpieza (no en análisis) porque:
1. Depende de que `price` y `quantity` ya estén con el tipo correcto.
2. Al estar en la tabla maestra, todos los análisis futuros la usan consistentemente.
3. Si hubiera un error en la fórmula, se corrige en un solo lugar.

---

### Decisiones documentadas

| Decisión | Razonamiento |
|----------|-------------|
| Copiar CSVs a `data/raw/` antes de tocarlos | Proteger los originales — nunca modificar el raw |
| No modificar `brie_carre` ni `the_greek` | Son características del menú, no errores |
| Guardar tabla maestra + tablas individuales limpias | La maestra es para análisis; las individuales para consultas de catálogo |
| Usar `how='left'` en todos los JOINs | Para detectar huérfanos vía nulls post-merge |

---

### Estructura de archivos tras Fase 3

```
data/
  raw/          ← 4 CSVs originales intactos
  clean/
    pizza_data_clean.csv    ← tabla maestra (48,620 filas, todas las columnas)
    orders_clean.csv        ← orders con date/time como datetime
    pizza_types_clean.csv   ← pizza_types con encoding corregido
notebooks/
  02_cleaning.ipynb         ← código reproducible de toda esta fase
```

---

### Resultados reales de la ejecución

| Verificación | Resultado |
|-------------|-----------|
| Nulls | 0 en todas las tablas |
| Duplicados | 0 en todas las tablas |
| Huérfanos en foreign keys | 0 en todas las relaciones |
| quantity range | min=1, max=4 |
| quantity distribución | 47,693 (x1) · 903 (x2) · 21 (x3) · 3 (x4) |
| Sanity check JOIN | OK — 48,620 filas exactas |
| Nulls post-JOIN | 0 en columnas clave |

**Números clave del dataset (validados):**
- Revenue total año 2015: **$817,860.05**
- Total pizzas vendidas: **49,574** (distinto a 48,620 líneas por quantity > 1)
- Promedio real de pedidos/día: 21,350 / 365 = **~58.5 pedidos/día**

### Hallazgo nuevo en ejecución

**Encoding del CSV:** Los archivos originales están en `cp1252` (Windows), no UTF-8.
Esto causó un `UnicodeDecodeError` al intentar cargar con el encoding por defecto de Pandas.

**¿Cómo se detectó?** El error de Python fue explícito: `'utf-8' codec can't decode byte 0x91`.
El byte `0x91` es el apóstrofo curvo izquierdo en cp1252 — carácter frecuente en texto europeo.

**Implicación para el proyecto:** Todos los notebooks deben cargar los CSVs raw con
`encoding='cp1252'`. Los archivos guardados en `data/clean/` sí se guardan en UTF-8,
por lo que los notebooks de análisis posteriores (Fase 5) cargarán sin problema con el default.

---

*Última actualización: Fase 3 completada y ejecutada*

---

## FASE 4 — Transformación y Feature Engineering

### Fuentes de información usadas
1. `pizza_data_clean.csv` — tabla maestra de Fase 3.
2. Preguntas de negocio de Fase 1 — para saber qué columnas son necesarias.
3. Convención de Power BI — columnas de orden (`size_order`, `month_order`) para que los visuales se ordenen correctamente sin configuración manual.

### ¿Qué columnas se crearon y por qué?

**Columnas temporales desde `date`:**
- `month`, `month_name` → para el análisis de estacionalidad (P1)
- `day_of_week`, `day_name_es` → para el análisis por día (P5)
- `is_weekend` → flag binario para segmentar semana vs fin de semana
- `quarter`, `week` → granularidades adicionales para tendencia en PBI
- `hour` → para análisis de horas pico (P3); se extrae del campo `time` (string) usando `pd.to_datetime().dt.hour`

**`time_block`:**
Se creó con `pd.cut()` sobre `hour` para agrupar la jornada en 5 bloques operativos.
Los cortes (11, 14, 17, 20) se definieron observando los valles naturales en el histograma
de pedidos por hora — no son arbitrarios.

**`ticket_total`:**
Es el `SUM(revenue)` por `order_id`. Se calcula aquí (no en análisis) porque varios cálculos
de Fase 5 lo necesitan. Se agrega de vuelta a la tabla transaccional con un merge para que
cada línea tenga el ticket de su pedido completo.

**`size_label` y `size_order`:**
El campo original `size` tiene valores S/M/L/XL/XXL. En Power BI, los visuales ordenan
texto alfabéticamente por defecto, lo que dejaría L antes que M. `size_order` es un entero
(1-5) que sirve como columna de ordenamiento explícito.

---

## FASE 5 — Análisis Exploratorio Profundo

### Fuentes de información usadas
1. `pizza_features.csv` — tabla con todas las columnas calculadas de Fase 4.
2. Las 5 preguntas de negocio de Fase 1 — guía de qué calcular.
3. Las preguntas secundarias de Notion — para el análisis extra de tallas.

### Metodología: de preguntas a números

Cada pregunta de negocio se convierte en una agregación específica:

| Pregunta | Transformación |
|----------|---------------|
| ¿Revenue por mes? | `groupby(['month','month_name']).agg(revenue=sum)` |
| ¿Bestsellers? | `groupby(['name','category']).agg(revenue=sum, qty=sum)` + rank |
| ¿Horas pico? | `groupby('hour').agg(orders=nunique)` |
| ¿Ticket promedio? | `groupby('order_id')['revenue'].sum()` → `.mean()` |
| ¿Día más activo? | `groupby('day_name_es').agg(orders=nunique)` |

### ¿Por qué se usa `nunique` para contar pedidos?

`order_id` aparece múltiples veces en la tabla transaccional (una vez por cada pizza del pedido).
Usar `count` sobrecontaría — daría el número de líneas, no de pedidos únicos.
`nunique` cuenta valores distintos, lo que equivale a contar pedidos reales.

### Hallazgo inesperado — Días cerrados

Al calcular días de operación se esperaban 365. El resultado fue **358**. Se identificaron
los 7 días sin registros:

| Fecha | Día | Observación |
|-------|-----|-------------|
| 2015-09-24 | Jueves | Cierre puntual |
| 2015-09-25 | Viernes | Cierre puntual |
| 2015-10-05 | Lunes | Cierre sistemático |
| 2015-10-12 | Lunes | Cierre sistemático |
| 2015-10-19 | Lunes | Cierre sistemático |
| 2015-10-26 | Lunes | Cierre sistemático |
| 2015-12-25 | Viernes | Navidad |

**¿Cómo afecta esto al análisis?**
Los 4 lunes de octubre explican parcialmente por qué octubre fue el mes de menor revenue.
Normalizado por días operados, octubre no es tan diferente del resto. Esto cambia la
interpretación: no hay estacionalidad negativa en otoño — hay simplemente menos días abiertos.

**¿Qué hacer con esto?**
En el dashboard de Power BI se documentará que el análisis usa días de operación reales (358),
no días del calendario (365). Los KPIs de promedio diario se calcularán sobre 358.

### Clasificación ABC de pizzas

Se aplicó una clasificación ABC por revenue:
- **Clase A** (top 8 = 25% del catálogo): generan el mayor volumen de ingresos
- **Clase B** (posiciones 9-20): desempeño medio
- **Clase C** (posiciones 21-32): menor contribución — candidatas a revisión

Criterio: se eligió dividir en tercios aproximados del catálogo de 32 pizzas, no en tercios
del revenue (método Pareto 80/20 clásico). Razón: con 32 pizzas muy balanceadas en revenue,
el método Pareto no generaría grupos útiles operacionalmente.

### KPIs finales validados

| KPI | Valor |
|-----|-------|
| Revenue total 2015 | **$817,860.05** |
| Total pedidos | **21,350** |
| Total pizzas vendidas | **49,574** |
| Ticket promedio | **$38.31** |
| Ticket mediana | **$32.50** |
| Días de operación | **358** |
| Pedidos promedio/día operado | **59.6** |
| Hora pico | **12:00h** (2,520 pedidos) |
| Día más activo | **Viernes** (3,538 pedidos, $136K) |
| Pizza top revenue | **Thai Chicken** ($43,434) |
| Pizza top unidades | **Classic Deluxe** (2,453 unidades) |
| Categoría top | **Classic** (26.9% del revenue) |

### Los 5 insights accionables

1. **Viernes necesita doble personal.** 34% más pedidos que domingo, 27% más que lunes. Staffing parejo toda la semana es ineficiente.
2. **Turnos split: 10-11h y 16-17h son los mejores momentos de preparación.** Los picos de pedidos son 12h y 18-19h — hay ventanas claras antes de cada pico para preparar.
3. **Potenciar las 3 Chicken de alto valor.** Thai, BBQ y California son top 3 en revenue. Tienen precio mayor que las Classic más baratas. Promocionarlas mejora el ticket promedio.
4. **Brie Carre es candidata a retiro.** Último lugar en revenue ($11,588), solo existe en S, 490 unidades en el año. Una pizza nueva en ese slot podría generar más ventas.
5. **Octubre no es un mes malo — solo tuvo menos días abiertos.** Los 4 lunes de cierre reducen el revenue calculado. Normalizado, octubre es comparable al resto del año.

### Tablas generadas para Power BI

| Archivo | Filas | Uso en dashboard |
|---------|-------|-----------------|
| `agg_monthly.csv` | 12 | Gráfica de línea — tendencia mensual |
| `agg_daily.csv` | 7 | Gráfica de barras — ventas por día |
| `agg_hourly.csv` | 15 | Gráfica de área — horas pico |
| `agg_pizza_performance.csv` | 32 | Tabla rankeada + clasificación ABC |
| `agg_category_size.csv` | 14 | Gráfica apilada — tallas por categoría |
| `agg_tickets.csv` | 21,350 | Histograma de distribución de tickets |
| `agg_weekly.csv` | 53 | Gráfica de línea — tendencia semanal |

---

*Última actualización: Fases 4 y 5 completadas*
*Próxima fase: Fase 6 — Visualización y Dashboard (Power BI)*

---

## FASE 6 — Diseño del Dashboard (previo a construcción)

### Fuentes de información usadas
1. Los 5 insights de Fase 5 — definen qué historia cuenta cada página.
2. La receta (Notion) — regla de máximo 3-4 slicers visibles, jerarquía KPIs arriba.
3. Las preguntas de negocio de Fase 1 — cada página responde a una audiencia específica.

### ¿Por qué 3 páginas y no 1?

La receta recomienda "1 página por audiencia o área de análisis". Se definieron 3 audiencias:
- **Dueño** → quiere el resumen financiero completo (Página 1)
- **Gerente operativo** → necesita saber cuándo poner personal (Página 2)
- **Dueño tomando decisión de menú** → necesita ver qué funciona y qué no (Página 3)

Poner todo en una sola página habría requerido scroll y habría perdido claridad.

### ¿Por qué NO crear relaciones entre tablas en Power BI?

Las tablas `agg_*.csv` ya están pre-agregadas en Python. Crear relaciones entre ellas en Power BI
introduciría el riesgo de dobles conteos o filtros cruzados inesperados.

La excepción es `pizza_features.csv` que sí es la tabla transaccional completa —
se usa para las medidas DAX de los KPIs y para el heatmap de operaciones.

### ¿Por qué se necesitan medidas DAX para Ticket Promedio?

`AVG(revenue)` daría el promedio por *línea de detalle*, no por *pedido*.
La medida correcta usa `AVERAGEX` sobre `VALUES(order_id)` para calcular primero
el total por pedido y luego promediar esos totales.

Este es el mismo problema que en Python donde `SUM(quantity)` ≠ `COUNT(rows)`.

### Decisiones de diseño visual

| Decisión | Razonamiento |
|----------|-------------|
| Donut en vez de pie | El pie chart distorsiona la percepción de proporciones pequeñas |
| Colores fijos por categoría | Consistencia entre páginas — el usuario no tiene que re-aprender la leyenda |
| Títulos con conclusión | "Viernes lidera con 3,538" > "Pedidos por día de semana" |
| Heatmap para operaciones | Muestra día+hora simultáneamente — imposible con barras separadas |
| Scatter revenue vs unidades | Identifica visualmente outliers como Brie Carre sin necesitar texto |

### Archivo de referencia
Diseño completo en: `visuals/dashboard_design.md`

---

*Última actualización: Fase 6 diseñada — pendiente de construcción en Power BI*
*Próxima fase: Fase 7 — Documentación y Storytelling (README)*
