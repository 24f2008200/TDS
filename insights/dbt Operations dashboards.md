Operations dashboards are the nervous system of an e commerce company. They twitch when fulfillment slows. They blink when support queues swell. They whisper early warnings before revenue feels the pain.

dbt is not the dashboard. It is the quiet engineer behind the curtain, shaping clean, trusted tables that BI tools can turn into glowing command centers.

Let’s build this properly.

---

# 1️⃣ How to Build Operations Dashboards in dbt

Think in three layers:

```
raw → staging → operational marts → BI dashboards
```

Operations dashboards need **freshness, clarity, and speed**.

---

## Step 1: Define Core Operational Domains

For fulfillment:

* Orders
* Shipments
* Warehouse events
* Inventory levels

For support:

* Tickets
* Ticket status changes
* Agent assignments
* Resolution events

Create staging models:

```
stg_orders
stg_shipments
stg_tickets
stg_agents
```

These:

* Rename columns
* Standardize timestamps
* Cast types
* Remove junk

No business logic yet.

---

## Step 2: Build Intermediate Logic

This is where operational metrics are born.

Examples:

`int_order_fulfillment_times`

* order_created_at
* shipped_at
* delivered_at
* fulfillment_hours

`int_ticket_lifecycle`

* ticket_created_at
* first_response_at
* resolved_at
* resolution_hours

Example pattern:

```sql
with base as (
    select *
    from {{ ref('stg_orders') }}
),

shipment as (
    select *
    from {{ ref('stg_shipments') }}
),

joined as (
    select
        b.order_id,
        b.created_at as order_created_at,
        s.shipped_at,
        s.delivered_at,
        datediff('hour', b.created_at, s.shipped_at) as time_to_ship_hours,
        datediff('hour', b.created_at, s.delivered_at) as time_to_deliver_hours
    from base b
    left join shipment s using (order_id)
)

select * from joined
```

Now operations has something measurable.

---

## Step 3: Build Operational Marts

Create marts like:

* `fct_fulfillment_daily`
* `fct_support_daily`
* `dim_warehouse`
* `dim_agents`

These should:

* Aggregate by day or hour
* Be dashboard ready
* Include rolling metrics

For example:

```sql
with fulfillment as (
    select *
    from {{ ref('int_order_fulfillment_times') }}
)

select
    date_trunc('day', order_created_at) as metric_date,
    count(order_id) as orders_created,
    avg(time_to_ship_hours) as avg_time_to_ship,
    avg(time_to_deliver_hours) as avg_time_to_deliver,
    sum(case when time_to_ship_hours > 24 then 1 else 0 end) as delayed_shipments
from fulfillment
where order_created_at >= current_date - interval '30 days'
group by 1
order by 1
```

This becomes your dashboard backbone.

---

# 2️⃣ Most Useful Metrics for Fulfillment and Support

Operations dashboards should answer:

* Are we slow?
* Are we overloaded?
* Are we breaking promises?

Let’s split by domain.

---

## 📦 Fulfillment Metrics

### Speed Metrics

* Time to ship
* Time to deliver
* Same day shipping rate
* 24 hour SLA adherence %

### Volume Metrics

* Orders created per day
* Orders shipped per day
* Backlog count
* Pending shipments

### Reliability Metrics

* Delayed shipment rate
* Failed delivery rate
* Return rate
* Inventory stockout rate

### Inventory Metrics

* Days of inventory remaining
* Low stock SKUs
* Inventory turnover

If fulfillment slows, revenue suffers two weeks later.

---

## 🎧 Support Metrics

### Responsiveness

* First response time
* Median response time
* Tickets opened per hour
* Tickets resolved per hour

### Resolution Quality

* Average resolution time
* Reopen rate
* Escalation rate
* SLA breach %

### Workforce Efficiency

* Tickets per agent
* Resolution rate per agent
* Active queue size

Operations dashboards should show both **volume pressure** and **service quality**.

---

# 3️⃣ Automating Dashboard Updates with dbt and BI Tools

Now we turn the machine on.

---

## Step 1: Use Scheduled dbt Runs

Run dbt with:

* dbt Cloud scheduled jobs
* Airflow
* Prefect
* GitHub Actions
* Warehouse native scheduler

Example cron:

```
Every 15 minutes for operations
Daily for executive dashboards
```

Operations data often needs near real time refresh.

---

## Step 2: Use Incremental Models

For high volume tables:

```sql
{{ config(materialized='incremental') }}

select ...
from ...
{% if is_incremental() %}
  where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

This prevents full rebuilds and keeps dashboards fast.

---

## Step 3: Freshness Checks

In `sources.yml`:

```yml
sources:
  - name: app
    tables:
      - name: orders
        freshness:
          warn_after: {count: 30, period: minute}
          error_after: {count: 60, period: minute}
```

If ingestion breaks, you know before leadership does.

---

## Step 4: Connect BI Tool

Popular stack:

* dbt → Snowflake/BigQuery/Redshift
* BI layer:

  * Looker
  * Tableau
  * Power BI
  * Metabase

BI tools query the marts directly.

Best practice:
Never point dashboards at staging models.
Only use mart tables.

---

## Step 5: Version Control and CI

Use:

* dbt tests in CI
* Pull request checks
* Auto run tests before deployment

Broken dashboards erode trust fast.

---

# 🧠 Architecture Blueprint for Operations Dashboards

```
Raw ingestion
    ↓
stg_orders / stg_tickets
    ↓
int_fulfillment / int_ticket_lifecycle
    ↓
fct_fulfillment_daily / fct_support_daily
    ↓
BI dashboards (hourly refresh)
```

---

# ⚙️ Advanced Improvements

* Add rolling 7 day and 30 day metrics inside marts
* Create alert tables for SLA breaches
* Use dbt exposures to document dashboard dependencies
* Add anomaly detection via statistical thresholds
* Partition large fact tables by date

---

Operations dashboards are not just charts.

They are early warning systems.
They are pulse monitors.
They are the difference between “we saw it coming” and “why didn’t anyone notice?”

If you tell me your warehouse and BI tool, I can sketch a production ready folder structure and refresh strategy tailored to your scale.


