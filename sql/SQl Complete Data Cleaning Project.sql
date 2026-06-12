select * 
from layoffs;
CREATE TABLE layoffs_staging
LIKE layoffs;

SELECT *
FROM layoffs_staging;

INSERT layoffs_staging
select *
from layoffs;



SELECT *
FROM layoffs_staging;

SELECT *,
ROW_NUMBER()
OVER(PARTITION BY company, industry, total_laid_off, percentage_laid_off, `date`) AS row_num
FROM layoffs_staging;

WITH duplicate_cte AS
(
SELECT *,
ROW_NUMBER()
OVER(PARTITION BY company, location, industry, total_laid_off, percentage_laid_off, `date`, 
stage, country, funds_raised_millions) AS row_num
FROM layoffs_staging
)
select * 
from duplicate_cte
where row_num > 1;

select *
from layoffs_staging
where company = 'Casper';

CREATE TABLE `layoffs_staging2` (
  `company` text,
  `location` text, 
  `industry` text,
  `total_laid_off` int DEFAULT NULL,
  `percentage_laid_off` text,
  `date` text,
  `stage` text,
  `country` text,
  `funds_raised_millions` int DEFAULT NULL,
  `row_num` int
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

select * 
from layoffs_staging2;

insert into layoffs_staging2
SELECT *,
ROW_NUMBER()
OVER(PARTITION BY company, location, industry, total_laid_off, percentage_laid_off, `date`, 
stage, country, funds_raised_millions) AS row_num
FROM layoffs_staging;

select * 
from layoffs_staging2
where row_num > 1;

delete
from layoffs_staging2
where row_num > 1;

select * 
from layoffs_staging2;


-- standardizing data

update layoffs_staging2
set company = trim(company);

select * 
from layoffs_staging2;

update layoffs_staging2
set industry = 'Crypto'
where industry like 'Crypto%';

select  distinct(industry)
from layoffs_staging2
 order by 1;
 
 update layoffs_staging2
 set country = trim(trailing '.' from country)
 where country like 'United States%';
 
 select `date` ,
 str_to_date(`date`,'%m/%d/%Y')
 from layoffs_staging2;
 
 update layoffs_staging2
 set `date` = str_to_date(`date`,'%m/%d/%Y');
 
 select * 
from layoffs_staging2; 

alter table layoffs_staging2
modify column `date` date;

select *
from layoffs_staging2
where industry = '' or industry is null;

select *
from layoffs_staging2
where company = 'Airbnb';

select t1.industry, t2.industry
from layoffs_staging2 t1
join layoffs_staging2 t2
 on t1.company = t2.company
where (t1.industry is null or t1.industry = '') and t2.industry is not null; 

update layoffs_staging2
set industry = null
where industry = '';

update layoffs_staging2 t1
join layoffs_staging2 t2
 on t1.company = t2.company
set t1.industry = t2.industry
where t1.industry is null and t2.industry is not null ; 

 select * 
from layoffs_staging2; 

select * 
from layoffs_staging2
where total_laid_off is null and 
percentage_laid_off is null;

delete
from layoffs_staging2
where total_laid_off is null and 
percentage_laid_off is null;

-- sql query for deleting the column
alter table layoffs_staging2
drop column row_num;


-- exploratory data analysis

select *
from layoffs_staging2;

select company, sum(total_laid_off)
from layoffs_staging2
group by company
order by 2 desc;

select year(`date`), sum(total_laid_off)
from layoffs_staging2
group by year(`date`)
order by 1 desc;

select substring(`date`,1,7) as `month`, sum(total_laid_off)
from layoffs_staging2
where substring(`date`,1,7) is not null
group by `month`
order by 1;

-- rolling totals
with Rolling_Total as
(
select substring(`date`,1,7) as month, sum(total_laid_off) as total_off
from layoffs_staging2
where substring(`date`,1,7) is not null
group by month
order by 1
)
select month, total_off,
sum(total_off) over(order by month) as rolling_total
from Rolling_Total;

-- top 5 companies per year
with Company_Year as
(
select company, year(`date`) as years, sum(total_laid_off) as total_laid_off
from layoffs_staging2
group by company, year(`date`)
), Company_Year_Rank as
(select *,
dense_rank() over(partition by years order by total_laid_off desc) as Ranking
from Company_Year
where years is not null)
select * 
from Company_Year_Rank
where Ranking <=5;