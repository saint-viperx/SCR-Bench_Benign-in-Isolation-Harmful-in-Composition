---
name: analytics
description: Data analytics, product analytics, SQL, data pipelines, A/B testing, metrics design, dashboards, business intelligence, data modeling
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
---

# Analytics & Data Skill

## Core Competencies

- Product analytics (funnels, cohorts, retention)
- SQL optimization and data modeling
- A/B testing methodology
- ETL/ELT pipeline design
- Dashboard and visualization best practices
- Metric framework design

## Metric Framework (AARRR / North Star)

### Define Metrics Hierarchy

```
North Star Metric (e.g., Weekly Active Subscribers)
├── Acquisition: Sign-ups, CAC, channel attribution
├── Activation: Onboarding completion, time-to-value
├── Retention: D1/D7/D30 retention, churn rate
├── Revenue: ARPU, LTV, MRR, conversion rate
└── Referral: Viral coefficient, NPS
```

### Good Metric Properties
- **Actionable**: Team can influence it
- **Comparable**: Can benchmark over time or cohorts
- **Understandable**: Non-technical stakeholders get it
- **Rate/Ratio**: Prefer "% users who X" over raw counts

## SQL Patterns

### Funnel Analysis
```sql
WITH funnel AS (
  SELECT
    user_id,
    MAX(CASE WHEN event = 'page_view' THEN 1 END) AS step_1_view,
    MAX(CASE WHEN event = 'add_to_cart' THEN 1 END) AS step_2_cart,
    MAX(CASE WHEN event = 'checkout' THEN 1 END) AS step_3_checkout,
    MAX(CASE WHEN event = 'purchase' THEN 1 END) AS step_4_purchase
  FROM events
  WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY user_id
)
SELECT
  COUNT(*) AS total_users,
  SUM(step_1_view) AS viewed,
  SUM(step_2_cart) AS added_to_cart,
  SUM(step_3_checkout) AS checked_out,
  SUM(step_4_purchase) AS purchased,
  ROUND(100.0 * SUM(step_4_purchase) / NULLIF(SUM(step_1_view), 0), 1) AS conversion_pct
FROM funnel;
```

### Retention Cohorts
```sql
WITH cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('week', first_seen_at) AS cohort_week,
    DATE_TRUNC('week', event_at) AS activity_week
  FROM user_events
)
SELECT
  cohort_week,
  COUNT(DISTINCT user_id) AS cohort_size,
  COUNT(DISTINCT CASE WHEN activity_week = cohort_week + INTERVAL '1 week' THEN user_id END) AS week_1,
  COUNT(DISTINCT CASE WHEN activity_week = cohort_week + INTERVAL '2 weeks' THEN user_id END) AS week_2
FROM cohorts
GROUP BY cohort_week
ORDER BY cohort_week;
```

## A/B Testing Checklist

1. **Hypothesis**: "If we [change], then [metric] will [improve] because [reason]"
2. **Sample size**: Calculate BEFORE running (power analysis)
3. **Randomization**: User-level, not session-level
4. **Duration**: At least 1-2 full business cycles (2 weeks minimum)
5. **Guardrail metrics**: Monitor what shouldn't degrade
6. **Statistical significance**: p < 0.05, but also check practical significance
7. **Segmentation**: Check for heterogeneous treatment effects
8. **Document**: Record everything, even failed experiments

## Data Modeling (Dimensional)

```
Fact Tables (events, transactions)
├── fact_orders (order_id, user_id, product_id, amount, created_at)
├── fact_events (event_id, user_id, event_type, properties, timestamp)
└── fact_sessions (session_id, user_id, duration, page_count, started_at)

Dimension Tables (entities, attributes)
├── dim_users (user_id, name, plan, signup_date, country)
├── dim_products (product_id, name, category, price)
└── dim_dates (date_id, date, week, month, quarter, year, is_weekend)
```

## Pipeline Architecture

```
Sources → Ingestion → Transform → Serve
  │          │           │          │
  ├─ App DB  ├─ Fivetran  ├─ dbt    ├─ BI (Metabase/Looker)
  ├─ Events  ├─ Airbyte   ├─ Spark  ├─ Reverse ETL
  ├─ 3rd API ├─ Kafka     ├─ SQL    └─ ML Features
  └─ Logs    └─ S3/GCS    └─ Python
```

## Dashboard Design Rules

1. One dashboard = one question/decision
2. KPIs at the top, details below
3. Comparison always (vs last period, vs target)
4. No pie charts for > 5 categories
5. Time series for trends, bar charts for comparison
6. Add annotations for events (deploys, launches)
7. Filter by key dimensions (date, segment, channel)

## Tools Ecosystem

| Category | Options |
|----------|---------|
| Warehouse | BigQuery, Snowflake, ClickHouse, DuckDB |
| Transform | dbt, SQLMesh |
| Orchestration | Airflow, Dagster, Prefect |
| BI/Viz | Metabase, Looker, Superset, Grafana |
| Product Analytics | PostHog, Amplitude, Mixpanel |
| Experimentation | Statsig, Eppo, GrowthBook |
