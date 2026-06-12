# Excel Project — Bike Buyers Sales Dashboard

## 📌 Project Overview

This project analyzes a **Bike Buyers dataset** of 1,000 customers to understand what demographic and lifestyle factors influence whether someone purchases a bike. The raw data was cleaned, transformed, and visualized into an interactive **Bike Sales Dashboard** in Excel using Pivot Tables, charts, and slicers.

---

## 📁 Files

| File | Description |
|------|-------------|
| `Excel Project Dataset.xlsx` | Raw bike buyers dataset (original, uncleaned) |
| `Excel Project Dataset_dashboard_project.xlsx` | Cleaned dataset + Pivot Tables + Final Dashboard |

---

## 🗂️ Workbook Structure

Both files share the same 4-sheet structure:

| Sheet | Purpose |
|-------|---------|
| `bike_buyers` | Original raw data with abbreviated/encoded values |
| `Working Sheet` | Cleaned & transformed data used for analysis |
| `Pivot Table` | Three pivot tables powering the dashboard charts |
| `DashBoard` | Final interactive Bike Sales Dashboard with slicers |

---

## 🧹 Data Cleaning & Transformation

### Raw Data Issues (bike_buyers sheet)
The original dataset had shorthand/encoded values in key columns that needed to be expanded for clarity and proper pivot analysis:

| Column | Raw Value | Cleaned Value |
|--------|-----------|---------------|
| Marital Status | `M` | `Married` |
| Marital Status | `S` | `Single` |
| Gender | `M` | `Male` |
| Gender | `F` | `Female` |

**Find & Replace** was used to expand all abbreviated values across 1,000 rows.

---

### New Column Added: Age Bracket

A new column `Age Bracket` was engineered using a nested `IF` formula to group customers into meaningful age segments for trend analysis:

```excel
=IF(L2>54, "Old", IF(L2>=31, "Middle Age", IF(L2<31, "Adolescent", "Invalid")))
```

| Age Range | Bracket |
|-----------|---------|
| Under 31 | Adolescent |
| 31 – 54 | Middle Age |
| 55 and above | Old |

This bucketing made it possible to analyze bike purchase behavior across life stages rather than individual ages.

---

## 📊 Dashboard & Pivot Table Analysis

The **DashBoard** sheet contains an interactive **Bike Sales Dashboard** built from three pivot tables, each revealing a different dimension of customer behavior.

---

### Chart 1 — Average Income by Gender & Purchase Decision

**Pivot:** Average Income → by Gender (rows) × Purchased Bike (columns)

| Gender | Did NOT Buy | Did Buy | Overall Avg |
|--------|-------------|---------|-------------|
| Female | $53,440 | $55,774 | $54,581 |
| Male | $56,208 | $60,124 | $58,063 |
| Overall | $54,875 | $57,963 | $56,360 |

**Key Insight:** Customers who purchased a bike consistently had a higher average income than those who didn't — across both genders. Male bike buyers averaged **$60,124**, the highest segment.

---

### Chart 2 — Bike Purchase Count by Commute Distance

**Pivot:** Count of Purchased Bike → by Commute Distance

| Commute Distance | Did NOT Buy | Did Buy | Total |
|------------------|-------------|---------|-------|
| 0–1 Miles | 166 | 200 | 366 |
| 1–2 Miles | 92 | 77 | 169 |
| 2–5 Miles | 67 | 95 | 162 |
| 5–10 Miles | 116 | 76 | 192 |
| 10+ Miles | 78 | 33 | 111 |

**Key Insight:** The **0–1 mile** commute group had the highest bike purchases (200), suggesting short-distance commuters are the most likely buyers. Purchase likelihood drops significantly for commutes over 5 miles.

---

### Chart 3 — Bike Purchase Count by Age Bracket

**Pivot:** Count of Purchased Bike → by Age Bracket (engineered column)

| Age Bracket | Did NOT Buy | Did Buy | Total |
|-------------|-------------|---------|-------|
| Adolescent | 71 | 39 | 110 |
| Middle Age | 318 | 383 | 701 |
| Old | 130 | 59 | 189 |

**Key Insight:** **Middle Age** customers (31–54) are by far the dominant buyer group — 383 purchases out of 481 total. Adolescents and older customers are much less likely to buy.

---

## 🎛️ Interactive Slicers

The dashboard includes slicers for dynamic filtering across all three charts simultaneously:

- **Marital Status** — Married / Single
- **Region** — Europe / North America / Pacific
- **Education** — Bachelors / Graduate Degree / High School / Partial College / Partial High School

---

## 💡 Key Excel Skills Demonstrated

- **Find & Replace** — Expanding abbreviated values (M/S/F) across large datasets
- **Nested IF Formula** — Engineering the `Age Bracket` column from raw age data
- **Pivot Tables** — Summarizing 1,000 rows into meaningful aggregations
- **Pivot Charts** — Bar and line charts linked to pivot tables
- **Slicers** — Interactive filters connected to all pivot tables/charts
- **Dashboard Design** — Combining multiple charts and slicers into a clean, unified view
