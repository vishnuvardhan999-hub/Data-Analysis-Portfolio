# Power BI Project — Data Professional Survey Dashboard

## 📌 Project Overview

This project analyzes a **real-world survey of 630 data professionals** collected in 2022, covering job roles, salaries, programming language preferences, career transition experiences, and workplace happiness. The cleaned data was visualized in an interactive **Power BI Dashboard** to surface key trends in the data industry.

---

## 📁 Files

| File | Description |
|------|-------------|
| `Power BI - Final Project.xlsx` | Raw survey dataset (630 respondents, 28 columns) |
| `power bi dashboard project.pbix` | Power BI workbook with all visuals and dashboard |

---

## 🗂️ Dataset Structure

| Detail | Value |
|--------|-------|
| Source | Data Professional Survey (2022) |
| Respondents | 630 |
| Columns | 28 |
| Sheet | `Data Professional Survey` |

**Key columns used in the dashboard:**

| Column | Description |
|--------|-------------|
| Q1 | Current job title / role |
| Q2 | Did you switch careers into data? |
| Q3 | Current yearly salary range (USD) |
| Q4 | Industry |
| Q5 | Favorite programming language |
| Q6 (×6) | Happiness scores (0–10) for salary, work/life balance, coworkers, management, upward mobility, learning |
| Q7 | Difficulty breaking into data |
| Q8 | Most important factor when looking for a new job |
| Q9 | Gender |
| Q10 | Age |
| Q11 | Country |
| Q12 | Highest level of education |

---

## 📊 Dashboard Visualizations & Key Insights

### 1. 🌍 Survey Takers by Country (Treemap)

A treemap showing the geographic distribution of respondents.

| Country | Respondents |
|---------|-------------|
| United States | 261 |
| India | 73 |
| United Kingdom | 40 |
| Canada | 32 |
| Nigeria | 18 |
| Germany | 14 |

**Key Insight:** The US dominates the respondent pool at 41%, followed by India. The dataset reflects a strong Western/English-speaking bias.

---

### 2. 💻 Favorite Programming Language (Stacked Bar Chart)

Bar chart of preferred languages, broken down by job role.

| Language | Votes |
|----------|-------|
| Python | 420 (66.7%) |
| R | 101 (16.0%) |
| SQL | 38 |
| C/C++ | 7 |
| JavaScript | 6 |

**Key Insight:** Python is the overwhelming favourite across all data roles. R comes second, predominantly among Data Scientists and academics.

---

### 3. 💰 Average Salary by Job Title (Horizontal Bar Chart)

Average yearly salary compared across roles after converting salary range text (e.g. "41k-65k") to numeric midpoint values in Power BI using calculated columns.

| Role | Notes |
|------|-------|
| Data Scientist | Highest avg salary |
| Data Engineer | Second highest |
| Data Analyst | Most respondents (381), mid-range salary |
| Database Developer | Lower range |
| Student / Looking | Entry level / no income |

**Key Insight:** Data Scientists and Data Engineers earn significantly more than Data Analysts despite Analysts making up 60% of all respondents.

---

### 4. 😊 Happiness Gauges

Two gauge charts showing average satisfaction scores out of 10:

| Metric | Avg Score / 10 |
|--------|---------------|
| **Salary Happiness** | **4.27** |
| **Work/Life Balance Happiness** | **5.74** |

**Key Insight:** Salary satisfaction is notably low at 4.27/10 — which aligns directly with "Better Salary" being the #1 job priority for 297 respondents. Work/life balance is moderate at 5.74.

---

### 5. 🚪 Difficulty Breaking into Data (Donut Chart)

| Difficulty Level | Count |
|-----------------|-------|
| Neither easy nor difficult | 269 (42.7%) |
| Difficult | 156 (24.8%) |
| Easy | 134 (21.3%) |
| Very Difficult | 44 (7.0%) |
| Very Easy | 27 (4.3%) |

**Key Insight:** Nearly 1 in 3 respondents found breaking into data difficult or very difficult, while only ~25% found it easy or very easy — reinforcing the high barrier to entry in the field.

---

### 6. 🔄 Career Switchers (Donut / Card)

| Switched into Data? | Count |
|--------------------|-------|
| Yes | 372 (59%) |
| No | 258 (41%) |

**Key Insight:** The majority of data professionals came from a different field — showing that data careers are highly accessible to career changers with the right upskilling.

---

### 7. 🎯 Most Important Job Factor (Bar Chart)

| Factor | Votes |
|--------|-------|
| Better Salary | 297 |
| Remote Work | 127 |
| Good Work/Life Balance | 117 |
| Good Culture | 54 |

**Key Insight:** Better Salary is the single biggest motivator for job seekers in the data field, more than double the next factor (Remote Work).

---

### 8. 📊 KPI Cards

| Metric | Value |
|--------|-------|
| Total Survey Takers | 630 |
| Average Age | 29.9 years |

---

## 🛠️ Data Transformation in Power BI

The raw survey data required several transformations in **Power Query** before visualizing:

- **Salary range → numeric:** Salary was stored as text ranges (e.g. `"41k-65k"`). A calculated column split the range and took the midpoint for averaging.
- **Role/Country cleanup:** Open-ended "Other (Please Specify):" responses were cleaned and grouped into standard categories.
- **Happiness scores:** Six separate happiness columns (Q6) were used individually for gauge and matrix visuals.
- **Age bucketing:** Age values used directly for the average age KPI card.

---

## 💡 Key Power BI Skills Demonstrated

- **Power Query** — data type conversion, text splitting, column cleanup
- **DAX calculated columns** — salary midpoint from range text
- **Treemap** — geographic distribution
- **Stacked bar charts** — language preference by role
- **Gauge charts** — happiness score KPIs
- **Donut charts** — difficulty and career switch breakdowns
- **KPI cards** — summary metrics (count, average age)
- **Dashboard layout** — multi-visual single-page dashboard design
