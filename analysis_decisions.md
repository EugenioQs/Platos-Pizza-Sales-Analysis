# Analysis Decisions — Plato's Pizza

> This document captures the *how* behind each decision in the project:
> where the information came from, what reasoning was applied, and why each path was chosen.
> Updated at the end of each phase.

---

## PHASE 1 — Understanding the Context

### Information sources used
1. The four dataset CSV files and `data_dictionary.csv` — available data structure.
2. Maven Analytics' dataset description — business context for Plato's Pizza.

---

### 1.1 — How was the stakeholder identified?

Maven Analytics published this dataset as a real business challenge:
*"Plato's Pizza wants to use their data to improve operations."* That frames the stakeholder as the
**restaurant owner or general manager** — not a technical analyst or IT team.

**Reasoning:** The stakeholder is identified by asking *"who makes decisions with this data?"*
In a restaurant, menu, scheduling, and staffing decisions are made by management — not the cook
or the cashier. Therefore the stakeholder is **business leadership**.

---

### 1.2 — How was the business decision statement built?

The decision statement connects two things:
- **What data we have:** sales by time (date/hour), by product (pizza, size, category), and by volume (quantity, price).
- **What the business can do with it:** adjust the menu, plan staff shifts, focus promotions.

The resulting statement:
> *"I want to optimize our operations and menu for next year: identify which pizzas to promote,
> when we need more staff, and whether there are products we should drop."*

**Rule applied:** A good decision statement always has an **action verb**
("optimize", "drop", "promote") — not just a description ("understand sales").
If the statement doesn't imply someone will do something differently after reading the analysis,
it's not a business decision — it's just curiosity.

---

### 1.3 — How were the analysis questions prioritized?

Eight questions were considered. Five priority questions were selected using three filters:

1. **Does it directly answer the decision statement?**
   - "Which are our bestsellers and which should we drop?" → YES (menu)
   - "How many customers per day? Are there peak hours?" → YES (staffing/operations)
   - "Which size is most popular by category?" → NO — secondary detail

2. **Is it answerable with the available data?**
   All questions are answerable: we have date, time, product, price, and quantity.
   No question requires data we don't have (individual customer data, ingredient costs, competitor data).

3. **Does it produce an actionable insight?**
   - "Is there revenue seasonality?" → Actionable: adjust inventory and promotions by season.
   - "How many pizzas per order on average?" → Less actionable on its own; kept as secondary.

**The 5 priority questions selected:**
1. How much revenue do we generate per month? Is there seasonality? *(Revenue)*
2. Which are our bestsellers and which should we drop? *(Menu)*
3. How many customers do we serve per day? Are there peak hours? *(Operations)*
4. What is the average ticket per order? *(Revenue)*
5. Which days of the week do we sell the most? *(Operations)*

---

### Documented decisions and assumptions

| Decision | Reasoning | Assumption made |
|----------|-----------|-----------------|
| Stakeholder = owner/manager | They make menu and operations decisions | The dataset simulates a real business with a single decision-maker |
| Analysis period = full year 2015 | Total dataset coverage | Data is complete and representative of a normal operating year |
| Unit of analysis = order | The business question is operational, not individual-customer | No individual customer data exists (no customer ID in the dataset) |

---

*Last updated: Phase 1 complete*

---

## PHASE 2 — Initial Exploration (Quick EDA)

### Information sources used
1. Direct reading of the four CSVs (first and last rows).
2. `data_dictionary.csv` to validate the official meaning of each column.
3. Simple manual calculations (division, counts) to get volume metrics.

---

### 2.1 — First look: shape and structure

| Table | Rows | Columns | Immediate observation |
|-------|------|---------|----------------------|
| `orders` | 21,350 | 3 | `order_id`, `date`, `time` — very clean structure |
| `order_details` | 48,620 | 4 | Main analysis table |
| `pizzas` | 96 | 4 | Catalog of type × size combinations |
| `pizza_types` | 32 | 4 | Master pizza catalog |

**How was the shape obtained?**
No Python yet — row counts were verified by reading the first and last line of each file.
`order_id` runs from 1 to 21,350 (no visible gaps) and `order_details_id` from 1 to 48,620.
This confirms sequential IDs and reliable row counts.

**Confirmed temporal coverage:**
- First order: `2015-01-01` at `11:38:36`
- Last order: `2015-12-31` at `23:02:05`
- = 365 full days of 2015 ✓

---

### 2.2 — Data dictionary

Key finding in the `ingredients` column description:
> *"They all include Mozzarella Cheese, even if not specified; and they all include Tomato Sauce,
> unless another sauce is specified."*

**Analytical implication:** The `ingredients` column is not exhaustive — there are implicit ingredients.
If ingredient usage is analyzed in Phase 4, Mozzarella must be added to all pizzas
and Tomato Sauce to any pizza that doesn't specify another sauce.

**Finding in `order_details.quantity`:**
> *"Pizzas of the same type and size are kept in the same row, and the quantity increases."*

**Implication:** Don't confuse rows in `order_details` (48,620) with pizzas sold.
Total pizzas sold = `SUM(quantity)`, which can be higher than 48,620.

---

### 2.3 — Problems detected at a glance

#### Problem 1 — `brie_carre` only has size S
`pizzas.csv` shows all pizzas have S, M, and L — except `brie_carre` which only has S.
`the_greek` also has XL ($25.50) and XXL ($35.95), unique on the menu.

**Why it matters:** If popularity by size is analyzed, these pizzas distort the count.
`brie_carre` can never appear in size M or L even if it's popular — it doesn't exist in those sizes.

**Phase 3 decision:** Document as a menu characteristic, not a data error. No modification.

#### Problem 2 — Encoding in `pizza_types.ingredients`
`calabrese` shows: `"ÑDuja Salami"` → should be `"'Nduja Salami"` (Italian sausage).
This is a UTF-8 encoding issue when reading the file.

**Phase 3 decision:** Fix during cleaning. Doesn't affect sales analysis but matters for ingredient analysis.

#### Problem 3 — Trailing empty lines in CSVs
`pizzas.csv` and `pizza_types.csv` have an empty line as their last row.

**Phase 3 decision:** Clean with `dropna(how='all')` when loading in Pandas. No data impact.

#### Problem 4 — `quantity` can be > 1 (pending verification)
The data dictionary confirms quantity can accumulate multiple units in one row.
The actual range of values hasn't been verified yet (are there 0s? negatives? extreme values?).

**Pending:** Verify in Phase 3 with `df['quantity'].describe()` and `value_counts()`.

---

### Derived metrics (calculated manually)

| Metric | Calculation | Result |
|--------|-------------|--------|
| Avg detail lines per order | 48,620 / 21,350 | ~2.28 lines/order |
| Avg orders per day | 21,350 / 365 | ~58.5 orders/day |
| Unique pizza types | Count `pizza_types` | 32 types |
| Type × size combinations | Count `pizzas` | 96 SKUs |
| Price range | Min-Max `pizzas.price` | $9.75 – $35.95 |

**Note on "2.28 lines/order":** This is not the same as "pizzas per order" because
quantity can be > 1. The actual average pizzas per order will be calculated in Phase 5.

---

### Documented decisions and assumptions

| Decision | Reasoning | Assumption made |
|----------|-----------|-----------------|
| No Python in Phase 2 | Shape and structure are verifiable by reading key rows | IDs are sequential without gaps — verify in Phase 3 |
| `brie_carre` S-only = intentional | Not a data error, it's a menu characteristic | The dataset faithfully reflects the real menu |
| Calabrese encoding = loading error | The "Ñ" character makes no sense in an Italian name | The original CSV was exported without correct UTF-8 encoding |

---

*Last updated: Phase 2 complete*

---

## PHASE 3 — Data Cleaning

### Information sources used
1. Issues documented in Phase 2.
2. Direct reading of `data_dictionary.csv` to understand expected behavior of `quantity`.
3. Knowledge of the relational model to design the final JOIN.

---

### Why create a single unified master table?

The Phase 1 business questions require joining information from all 4 tables:
- "How much revenue per month?" → needs `date` (orders) + `price` (pizzas) + `quantity` (order_details)
- "Which are the bestsellers?" → needs `name` and `category` (pizza_types) + `quantity` (order_details)
- "Peak hours?" → needs `time` (orders) + `quantity` (order_details)

Rather than repeating the JOIN in every analysis, it's built once here and saved as `pizza_data_clean.csv`.
This is more reliable and avoids errors from repeating the merge across different notebooks.

---

### How was the JOIN designed?

The central table is `order_details` (it has the most rows and connects everything).
LEFT JOINs are performed from `order_details` outward:

```
order_details
  → LEFT JOIN orders       ON order_id       (adds date, time)
  → LEFT JOIN pizzas       ON pizza_id       (adds size, price, pizza_type_id)
  → LEFT JOIN pizza_types  ON pizza_type_id  (adds name, category, ingredients)
```

LEFT JOIN (not INNER JOIN) is used to detect orphan rows: if an `order_details` row
finds no match, it appears as null in the JOIN columns — triggering an alert in the
subsequent sanity check.

**Sanity check designed:** `assert len(df) == len(order_details)` — if the JOIN produces more
rows than order_details, it means there are duplicates in the dimension tables (pizzas or orders),
which would be a serious data error.

---

### Why is the `revenue` column added in this phase?

`revenue = price × quantity` is the most fundamental metric of the analysis.
It's calculated during cleaning (not analysis) because:
1. It depends on `price` and `quantity` already having the correct data types.
2. Being in the master table means all future analyses use it consistently.
3. If there's an error in the formula, it's fixed in one place.

---

### Documented decisions

| Decision | Reasoning |
|----------|-----------|
| Copy CSVs to `data/raw/` before touching them | Protect originals — never modify raw data |
| Don't modify `brie_carre` or `the_greek` | They are menu characteristics, not errors |
| Save master table + individual clean tables | Master for analysis; individual for catalog lookups |
| Use `how='left'` in all JOINs | To detect orphans via post-merge nulls |

---

### File structure after Phase 3

```
data/
  raw/          ← 4 original CSVs untouched
  clean/
    pizza_data_clean.csv    ← master table (48,620 rows, all columns)
    orders_clean.csv        ← orders with date/time as datetime
    pizza_types_clean.csv   ← pizza_types with encoding corrected
notebooks/
  02_cleaning.ipynb         ← reproducible code for this entire phase
```

---

### Actual execution results

| Verification | Result |
|-------------|--------|
| Nulls | 0 across all tables |
| Duplicates | 0 across all tables |
| Orphans in foreign keys | 0 across all relationships |
| quantity range | min=1, max=4 |
| quantity distribution | 47,693 (×1) · 903 (×2) · 21 (×3) · 3 (×4) |
| JOIN sanity check | OK — exactly 48,620 rows |
| Post-JOIN nulls | 0 in key columns |

**Key dataset numbers (validated):**
- Total revenue 2015: **$817,860.05**
- Total pizzas sold: **49,574** (differs from 48,620 rows due to quantity > 1)
- Average orders/day: 21,350 / 365 = **~58.5 orders/day**

### New finding during execution

**CSV encoding:** The original files are in `cp1252` (Windows), not UTF-8.
This caused a `UnicodeDecodeError` when loading with Pandas' default encoding.

**How it was detected:** Python's error was explicit: `'utf-8' codec can't decode byte 0x91`.
Byte `0x91` is the left curly apostrophe in cp1252 — common in European text.

**Project implication:** All notebooks must load raw CSVs with `encoding='cp1252'`.
Files saved in `data/clean/` are saved in UTF-8, so subsequent analysis notebooks
(Phase 5 onward) load without issues using the default encoding.

---

*Last updated: Phase 3 complete and executed*

---

## PHASE 4 — Transformation and Feature Engineering

### Information sources used
1. `pizza_data_clean.csv` — master table from Phase 3.
2. Phase 1 business questions — to determine which columns are needed.
3. Power BI ordering convention — sort columns (`size_order`, `month_order`) so visuals
   sort correctly without manual configuration.

### What columns were created and why?

**Temporal columns from `date`:**
- `month`, `month_name` → for seasonality analysis (Q1)
- `day_of_week`, `day_name_es` → for day-of-week analysis (Q5)
- `is_weekend` → binary flag to segment weekdays vs weekends
- `quarter`, `week` → additional granularities for trend analysis in Power BI
- `hour` → for peak hour analysis (Q3); extracted from the `time` field (string) using `pd.to_datetime().dt.hour`

**`time_block`:**
Created with `pd.cut()` on `hour` to group the operating day into 5 operational blocks.
The cut points (11, 14, 17, 20) were defined by observing natural valleys in the
orders-per-hour histogram — not arbitrary.

**`ticket_total`:**
This is `SUM(revenue)` per `order_id`. Calculated here (not in analysis) because multiple
Phase 5 calculations depend on it. Merged back into the transactional table so that
each line carries the total ticket of its complete order.

**`size_label` and `size_order`:**
The original `size` field has values S/M/L/XL/XXL. Power BI sorts text alphabetically
by default, which would place L before M. `size_order` is an integer (1–5) used as
an explicit sort column.

---

*Last updated: Phase 4 complete*

---

## PHASE 5 — Deep Exploratory Analysis

### Information sources used
1. `pizza_features.csv` — table with all calculated columns from Phase 4.
2. The 5 Phase 1 business questions — guide for what to calculate.

### Methodology: from questions to numbers

Each business question maps to a specific aggregation:

| Question | Transformation |
|----------|---------------|
| Revenue by month? | `groupby(['month','month_name']).agg(revenue=sum)` |
| Bestsellers? | `groupby(['name','category']).agg(revenue=sum, qty=sum)` + rank |
| Peak hours? | `groupby('hour').agg(orders=nunique)` |
| Average ticket? | `groupby('order_id')['revenue'].sum()` → `.mean()` |
| Busiest day? | `groupby('day_name_es').agg(orders=nunique)` |

### Why `nunique` for counting orders?

`order_id` appears multiple times in the transactional table (once per pizza in the order).
Using `count` would overcount — it gives the number of lines, not unique orders.
`nunique` counts distinct values, which is equivalent to counting real orders.

### Unexpected finding — Closed days

When calculating operating days, 365 were expected. The result was **358**. Seven days
with no records were identified:

| Date | Day | Observation |
|------|-----|-------------|
| 2015-09-24 | Thursday | One-off closure |
| 2015-09-25 | Friday | One-off closure |
| 2015-10-05 | Monday | Systematic closure |
| 2015-10-12 | Monday | Systematic closure |
| 2015-10-19 | Monday | Systematic closure |
| 2015-10-26 | Monday | Systematic closure |
| 2015-12-25 | Friday | Christmas |

**How does this affect the analysis?**
The 4 Mondays in October partially explain why October had the lowest revenue.
Normalized by operating days, October is not significantly different from other months.
This changes the interpretation: there is no negative seasonality in fall — there are simply
fewer days open.

**How this is handled:**
The Power BI dashboard documents that the analysis uses actual operating days (358),
not calendar days (365). Daily average KPIs are calculated on 358.

### ABC classification of pizzas

An ABC classification was applied by revenue:
- **Class A** (top 8 = 25% of catalog): generate the highest revenue volume
- **Class B** (positions 9–20): average performance
- **Class C** (positions 21–32): lowest contribution — candidates for review

Criterion: the catalog of 32 pizzas was divided into approximate thirds, not into thirds
of revenue (the classic Pareto 80/20 method). Reason: with 32 pizzas very balanced in revenue,
the Pareto method would not produce operationally useful groups.

### Final validated KPIs

| KPI | Value |
|-----|-------|
| Total revenue 2015 | **$817,860.05** |
| Total orders | **21,350** |
| Total pizzas sold | **49,574** |
| Average ticket | **$38.31** |
| Median ticket | **$32.50** |
| Operating days | **358** |
| Avg orders / operating day | **59.6** |
| Peak hour | **12:00h** (2,520 orders) |
| Busiest day | **Friday** (3,538 orders, $136K) |
| Top pizza by revenue | **Thai Chicken** ($43,434) |
| Top pizza by units | **Classic Deluxe** (2,453 units) |
| Top category | **Classic** (26.9% of revenue) |

### The 5 actionable insights

1. **Fridays need double staffing.** 34% more orders than Sunday, 27% more than Monday. Equal staffing all week is inefficient.
2. **Split shifts: 10–11h and 16–17h are the best prep windows.** Order peaks are at 12h and 18–19h — there are clear windows before each rush to prepare.
3. **Push the 3 high-value Chicken pizzas.** Thai, BBQ, and California are top 3 by revenue. They're priced higher than the cheaper Classic options. Promoting them improves the average ticket.
4. **Brie Carre is a candidate for removal.** Last place in revenue ($11,588), only available in size S, 490 units sold in the year. A new pizza in that slot could generate more sales.
5. **October is not a slow month — it just had fewer open days.** The 4 Monday closures reduce the calculated revenue. Normalized, October is comparable to the rest of the year.

### Tables generated for Power BI

| File | Rows | Dashboard use |
|------|------|--------------|
| `agg_monthly.csv` | 12 | Line chart — monthly trend |
| `agg_daily.csv` | 7 | Bar chart — sales by day |
| `agg_hourly.csv` | 15 | Area chart — peak hours |
| `agg_pizza_performance.csv` | 32 | Ranked table + ABC classification |
| `agg_category_size.csv` | 14 | Stacked chart — sizes by category |
| `agg_tickets.csv` | 21,350 | Ticket distribution histogram |
| `agg_weekly.csv` | 53 | Line chart — weekly trend |

---

*Last updated: Phases 4 and 5 complete*

---

## PHASE 6 — Dashboard Design (prior to build)

### Information sources used
1. The 5 Phase 5 insights — define what story each page tells.
2. Best practices for dashboard design — max 3–4 visible slicers, KPIs at the top.
3. Phase 1 business questions — each page answers a specific audience.

### Why 3 pages and not 1?

One page per audience or area of analysis was the guiding principle. Three audiences were defined:
- **Owner** → wants the complete financial summary (Page 1)
- **Operations manager** → needs to know when to schedule staff (Page 2)
- **Owner making a menu decision** → needs to see what works and what doesn't (Page 3)

Putting everything on one page would require scrolling and lose clarity.

### Why NOT create relationships between tables in Power BI?

The `agg_*.csv` tables are already pre-aggregated in Python. Creating relationships between them
in Power BI would introduce the risk of double-counting or unexpected cross-filters.

The exception is `pizza_features.csv`, which is the full transactional table —
used for DAX measures on KPIs and for the operations heatmap.

### Why are DAX measures needed for Average Ticket?

`AVG(revenue)` would give the average per *detail line*, not per *order*.
The correct measure uses `AVERAGEX` over `VALUES(order_id)` to first calculate
the total per order and then average those totals.

This is the same problem as in Python where `SUM(quantity)` ≠ `COUNT(rows)`.

### Visual design decisions

| Decision | Reasoning |
|----------|-----------|
| Donut instead of pie | Pie charts distort perception of small proportions |
| Fixed colors per category | Consistency across pages — users don't need to re-learn the legend |
| Titles with conclusion | "Friday leads with 3,538" > "Orders by day of week" |
| Heatmap for operations | Shows day + hour simultaneously — impossible with separate bar charts |
| Revenue vs units scatter | Visually identifies outliers like Brie Carre without needing text |

### Reference file
Full design in: `visuals/dashboard_design.md`

---

*Last updated: Phase 6 designed and built in Power BI*
