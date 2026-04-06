# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Data analytics project using the **Pizza Place Sales** dataset (Maven Analytics) — one year (2015) of pizza shop transactions. The goal is a complete portfolio project following the methodology defined in Notion: *"La Receta del Data Analyst — Proyecto End to End"*.

**Stack:** Python (Pandas, Matplotlib/Seaborn) + Power BI · Git/GitHub · Notion for documentation

---

## La Receta — 8 Fases del Proyecto

| Fase | Nombre | Estado |
|------|--------|--------|
| 1 | Entender el Contexto (stakeholder, preguntas de negocio) | — |
| 2 | Exploración Inicial (EDA rápido: shape, dtypes, nulls) | — |
| 3 | Limpieza de Datos (nulls, tipos, duplicados, outliers) | — |
| 4 | Transformación y Feature Engineering (columnas calculadas, groupby, joins) | — |
| 5 | Análisis Exploratorio Profundo (univariado, bivariado, insights) | — |
| 6 | Visualización y Dashboard (Power BI) | — |
| 7 | Documentación y Storytelling (README, narrative SCR, presentación) | — |
| 8 | Entrega y Publicación (GitHub, Power BI Service, portafolio, LinkedIn) | — |

**Regla de la receta:** No avanzar a la siguiente fase sin terminar la anterior.

---

## Data Model

Four CSV files in `pizza_sales/`, structured as a relational schema:

```
pizza_types (32 rows)
    └─→ pizzas (96 rows)  ←──────────────────┐
                                              │
                                      order_details (48,620 rows)
                                              ↑
                                      orders (21,350 rows)
```

| File | Rows | Key Fields |
|------|------|------------|
| `pizza_sales/orders.csv` | 21,350 | `order_id`, `date` (2015), `time` |
| `pizza_sales/order_details.csv` | 48,620 | `order_details_id`, `order_id`, `pizza_id`, `quantity` |
| `pizza_sales/pizzas.csv` | 96 | `pizza_id`, `pizza_type_id`, `size` (S/M/L/XL/XXL), `price` |
| `pizza_sales/pizza_types.csv` | 32 | `pizza_type_id`, `name`, `category`, `ingredients` |
| `data_dictionary.csv` | — | Field-level metadata for all tables |

- `pizza_id` is a composite key: `{pizza_type_id}_{size}` (e.g., `bbq_ckn_m`)
- **Pizza categories:** Classic, Chicken, Supreme, Veggie
- **Price range:** ~$12.75 – $20.75 USD

---

## File Structure Convention (Fase 8)

```
/data/raw/          ← original CSVs (never overwrite)
/data/clean/        ← cleaned dataset output
/notebooks/         ← Jupyter notebooks per phase
/visuals/           ← dashboard screenshots
README.md           ← written in English, focused on business impact
```

---

## Key Rules from the Methodology

- **Nunca sobreescribas el raw** — always save cleaned data as a new file (`datos_limpios.csv`)
- **Documenta cada transformación** — a comment in the code is enough
- **Insights en lenguaje de negocio** — not "correlation of 0.7" but "X causes Y, action: Z"
- **Sanity check** — after every aggregation, verify totals against the source data
- **Dashboard validation** — manually compare at least one number against raw data

---

## Notion Reference

- **Metodología:** [La Receta del Data Analyst](https://www.notion.so/33206be4531c81908b4bde2d67f5054e)
- **Dataset seleccionado:** [Pizza Place Sales (Maven Analytics)](https://www.notion.so/33206be4531c81a6a8a4d6129dcc14e6)
- **Espacio profesional:** Eugenio Quintero — [Mi espacio profesional](https://www.notion.so/32f06be4531c80af9a49f99a617f8a47)
