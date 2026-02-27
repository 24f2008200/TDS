Great set of SQL questions! Let me cover all three thoroughly.

---

## 1. Using COALESCE to Replace NULL Values in DuckDB

`COALESCE` returns the **first non-NULL value** from a list of expressions. It's the standard way to handle NULLs in DuckDB.

```sql
-- Basic usage: replace NULL with a default value
SELECT
    customer_id,
    COALESCE(phone_number, 'N/A')           AS phone,
    COALESCE(discount, 0)                   AS discount,
    COALESCE(middle_name, last_name, 'Unknown') AS fallback_name  -- tries each in order
FROM customers;
```

**Common patterns:**

```sql
-- Replace NULL in aggregation (SUM treats NULL as 0 anyway, but explicit is safer)
SELECT
    order_id,
    COALESCE(SUM(amount), 0) AS total_amount
FROM orders
GROUP BY order_id;

-- Combine two columns, preferring the first non-NULL
SELECT
    COALESCE(preferred_email, work_email, personal_email) AS best_email
FROM contacts;

-- In a JOIN — fill missing lookup values
SELECT
    o.order_id,
    COALESCE(p.product_name, 'Deleted Product') AS product_name
FROM orders o
LEFT JOIN products p ON o.product_id = p.id;
```

> **Key behaviour:** COALESCE is short-circuit — it stops evaluating as soon as it finds a non-NULL value. Also, `COALESCE(a, b)` is equivalent to `CASE WHEN a IS NOT NULL THEN a ELSE b END`.

---

## 2. CASE Expressions to Bin Numeric Values into Categories

DuckDB supports both **searched CASE** (most flexible) and **simple CASE** (equality checks).

```sql
-- Searched CASE: bin a numeric column into labelled ranges
SELECT
    order_id,
    amount,
    CASE
        WHEN amount < 50              THEN 'Small'
        WHEN amount BETWEEN 50 AND 199 THEN 'Medium'
        WHEN amount BETWEEN 200 AND 499 THEN 'Large'
        WHEN amount >= 500            THEN 'Enterprise'
        ELSE 'Unknown'                -- catches NULLs too
    END AS order_tier
FROM orders;
```

**Binning into equal-width buckets dynamically:**

```sql
-- Bin ages into decades
SELECT
    name,
    age,
    CASE
        WHEN age < 18  THEN 'Under 18'
        WHEN age < 30  THEN '18–29'
        WHEN age < 40  THEN '30–39'
        WHEN age < 50  THEN '40–49'
        ELSE                '50+'
    END AS age_group
FROM users;
```

**Simple CASE (equality-based):**

```sql
-- Map a status code to a label
SELECT
    order_id,
    CASE status_code
        WHEN 1 THEN 'Pending'
        WHEN 2 THEN 'Processing'
        WHEN 3 THEN 'Shipped'
        WHEN 4 THEN 'Delivered'
        ELSE        'Cancelled'
    END AS status_label
FROM orders;
```

> **Tip:** DuckDB also has `if(condition, true_val, false_val)` as shorthand for simple two-branch CASE expressions.

---

## 3. Filter Rows AND Aggregate Totals in a Single Query

This is the classic **WHERE + GROUP BY + HAVING** pattern. Each clause plays a distinct role:

```sql
-- Full example: filter first, then aggregate, then filter aggregates
SELECT
    region,
    product_category,
    COUNT(*)            AS order_count,
    SUM(amount)         AS total_revenue,
    AVG(amount)         AS avg_order_value,
    MAX(amount)         AS largest_order
FROM orders
WHERE
    status_code  = 3                        -- filter BEFORE aggregation (row-level)
    AND order_date >= '2024-01-01'
GROUP BY
    region,
    product_category
HAVING
    SUM(amount) > 10000                     -- filter AFTER aggregation (group-level)
    AND COUNT(*) >= 5
ORDER BY
    total_revenue DESC;
```

**Combining COALESCE + CASE + aggregation together:**

```sql
SELECT
    COALESCE(region, 'Unassigned')    AS region,
    CASE
        WHEN amount < 50   THEN 'Small'
        WHEN amount < 200  THEN 'Medium'
        ELSE                    'Large'
    END                               AS order_tier,
    COUNT(*)                          AS order_count,
    SUM(amount)                       AS total_revenue
FROM orders
WHERE status_code != 0                -- exclude cancelled
GROUP BY
    COALESCE(region, 'Unassigned'),   -- group by the same expression
    CASE
        WHEN amount < 50   THEN 'Small'
        WHEN amount < 200  THEN 'Medium'
        ELSE                    'Large'
    END
HAVING COUNT(*) > 10
ORDER BY total_revenue DESC;
```

---

### Quick Reference — Which Clause Does What

| Clause | Runs on | Purpose |
|--------|---------|---------|
| `WHERE` | Individual rows | Filter **before** grouping |
| `GROUP BY` | Row groups | Define aggregation buckets |
| `HAVING` | Aggregated groups | Filter **after** grouping |
| `COALESCE` | Any expression | Replace NULLs |
| `CASE` | Any expression | Conditional branching / binning |

> **DuckDB bonus:** You can reference column aliases defined in `SELECT` directly inside `GROUP BY` and `ORDER BY` — unlike standard SQL, so `GROUP BY order_tier` works instead of repeating the full CASE expression.




```sql
SELECT
    COUNT(*)                    AS order_count,
    ROUND(SUM(amount), 2)       AS total_amount
FROM (
    SELECT
        COALESCE(customer, 'Unknown')   AS customer,
        amount,
        CASE
            WHEN amount > 720   THEN 'high'
            WHEN amount > 323   THEN 'medium'
            ELSE                     'low'
        END                             AS price_band
    FROM orders
    WHERE region = 'LATAM'
)
WHERE price_band = 'medium';
```

---

### How it works — layer by layer

**Inner subquery:**
- `WHERE region = 'LATAM'` — filters to LATAM rows only
- `COALESCE(customer, 'Unknown')` — replaces any NULL customer names
- `CASE` — assigns `high / medium / low` based on the amount thresholds

**Outer query:**
- `WHERE price_band = 'medium'` — isolates just the medium band
- `COUNT(*)` — counts orders in that band
- `ROUND(SUM(amount), 2)` — sums and rounds to 2 decimal places
- Returns exactly **one row** as required

> **DuckDB tip:** DuckDB lets you filter on an alias (`WHERE price_band = 'medium'`) in the outer query, keeping the logic clean. Alternatively you could use `HAVING` if grouping, but since we only need one band, a subquery filter is simpler and more readable.
