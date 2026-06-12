# SQL Projects

This section contains SQL-based data analysis projects. Each project demonstrates real-world data handling skills using MySQL, including data cleaning, transformation, and exploratory data analysis (EDA).

---

## 📂 Projects in This Section

### 1. 🧹 Tech Layoffs — Data Cleaning & EDA

| Detail       | Info                            |
|--------------|---------------------------------|
| **Dataset**  | `layoffs.csv`                   |
| **Tool**     | MySQL                           |
| **File**     | `SQl Complete Data Cleaning Project.sql` |

---

### 📋 Project Overview

This project works with a real-world dataset of **global tech company layoffs**. The goal was to clean the raw data thoroughly and then perform exploratory analysis to uncover trends.

---

### 🧹 Part 1 — Data Cleaning

The raw `layoffs` table was staged and cleaned through the following steps:

#### Step 1: Create a Staging Table
A staging table (`layoffs_staging`) was created as a copy of the raw data to preserve the original untouched.

```sql
CREATE TABLE layoffs_staging LIKE layoffs;
INSERT layoffs_staging SELECT * FROM layoffs;
```

#### Step 2: Remove Duplicate Records
Used `ROW_NUMBER()` with a `PARTITION BY` across all key columns to identify exact duplicate rows, then deleted them via a second staging table (`layoffs_staging2`).

```sql
WITH duplicate_cte AS (
  SELECT *,
    ROW_NUMBER() OVER(
      PARTITION BY company, location, industry, total_laid_off,
      percentage_laid_off, date, stage, country, funds_raised_millions
    ) AS row_num
  FROM layoffs_staging
)
SELECT * FROM duplicate_cte WHERE row_num > 1;
```

#### Step 3: Standardize Data
- Trimmed leading/trailing whitespace from `company` names.
- Unified inconsistent `industry` values (e.g., `Crypto`, `Crypto Currency` → `Crypto`).
- Cleaned `country` values (e.g., removed trailing dots from `United States.`).
- Converted `date` column from `TEXT` to proper `DATE` type using `STR_TO_DATE`.

```sql
UPDATE layoffs_staging2 SET company = TRIM(company);
UPDATE layoffs_staging2 SET industry = 'Crypto' WHERE industry LIKE 'Crypto%';
UPDATE layoffs_staging2 SET date = STR_TO_DATE(date, '%m/%d/%Y');
ALTER TABLE layoffs_staging2 MODIFY COLUMN date DATE;
```

#### Step 4: Handle NULL / Blank Values
- Identified rows with blank or NULL `industry` values.
- Used a self-join to populate missing `industry` values from other records of the same company.
- Deleted rows where both `total_laid_off` and `percentage_laid_off` were NULL (unusable records).

```sql
UPDATE layoffs_staging2 t1
JOIN layoffs_staging2 t2 ON t1.company = t2.company
SET t1.industry = t2.industry
WHERE t1.industry IS NULL AND t2.industry IS NOT NULL;
```

#### Step 5: Drop Helper Column
Dropped the `row_num` helper column after deduplication was complete.

---

### 📊 Part 2 — Exploratory Data Analysis (EDA)

After cleaning, the data was analyzed to surface meaningful insights:

#### Total Layoffs by Company
```sql
SELECT company, SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY company
ORDER BY 2 DESC;
```

#### Total Layoffs by Year
```sql
SELECT YEAR(date), SUM(total_laid_off)
FROM layoffs_staging2
GROUP BY YEAR(date)
ORDER BY 1 DESC;
```

#### Monthly Layoff Trends + Rolling Total
Calculated a running cumulative total of layoffs month-over-month using a CTE and `SUM() OVER()` window function.

```sql
WITH Rolling_Total AS (
  SELECT SUBSTRING(date, 1, 7) AS month, SUM(total_laid_off) AS total_off
  FROM layoffs_staging2
  WHERE SUBSTRING(date, 1, 7) IS NOT NULL
  GROUP BY month
  ORDER BY 1
)
SELECT month, total_off,
  SUM(total_off) OVER(ORDER BY month) AS rolling_total
FROM Rolling_Total;
```

#### Top 5 Companies with Most Layoffs Per Year
Used two nested CTEs with `DENSE_RANK()` to rank companies by layoffs within each year and filter to the top 5.

```sql
WITH Company_Year AS (
  SELECT company, YEAR(date) AS years, SUM(total_laid_off) AS total_laid_off
  FROM layoffs_staging2
  GROUP BY company, YEAR(date)
),
Company_Year_Rank AS (
  SELECT *, DENSE_RANK() OVER(PARTITION BY years ORDER BY total_laid_off DESC) AS Ranking
  FROM Company_Year
  WHERE years IS NOT NULL
)
SELECT * FROM Company_Year_Rank WHERE Ranking <= 5;
```

---

### 📁 Files

| File | Description |
|------|-------------|
| `layoffs.csv` | Raw dataset of global tech layoffs |
| `SQl Complete Data Cleaning Project.sql` | Full SQL script — data cleaning + EDA |

---

### 💡 Key SQL Concepts Used

- `ROW_NUMBER()`, `DENSE_RANK()` — Window functions
- `CTEs` (Common Table Expressions) — Modular query building
- `STR_TO_DATE()`, `TRIM()`, `SUBSTRING()` — String & date functions
- `Self JOIN` — Filling NULL values from related rows
- `ALTER TABLE`, `UPDATE`, `DELETE` — DDL & DML operations
- `GROUP BY` + aggregate functions for EDA
