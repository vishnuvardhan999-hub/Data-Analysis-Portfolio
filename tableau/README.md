# Tableau Project — Seattle AirBnB Dashboard

## 📌 Project Overview

This project explores **Seattle AirBnB listing data** to uncover pricing trends, neighborhood demand, and revenue patterns across the city. The raw data was sourced from a real AirBnB dataset and visualized in an interactive **Tableau Dashboard** that allows users to explore listings by location, bedroom count, property type, and more.

---

## 📁 Files

| File | Description |
|------|-------------|
| `Tableau Full Project.xlsx` | Source dataset — Listings, Reviews, Calendar sheets |
| `AirBNB Tableau Dashboard Project.twb` | Tableau workbook with all visualizations and dashboard |

---

## 🗂️ Dataset Structure

The Excel workbook contains **3 sheets** that were connected in Tableau:

| Sheet | Rows | Description |
|-------|------|-------------|
| `Listings` | 3,818 | Full listing details — price, location, property type, host info, reviews |
| `Reviews` | 84,849 | Individual guest reviews linked to listings |
| `Calendar` | ~1M | Daily availability and pricing for each listing across the year |

---

## 📊 Dashboard Visualizations & Key Insights

### 1. 💰 Average Price by Zipcode (Map + Bar Chart)

Listings were plotted on a **filled map of Seattle** by zipcode, with color intensity representing average nightly price. A companion bar chart ranks zipcodes by average price.

| Zipcode | Avg Price | Listings |
|---------|-----------|----------|
| 98134 | $206.60 | 5 |
| 98199 | $172.39 | 66 |
| 98101 | $166.72 | 201 |
| 98119 | $166.38 | 143 |
| 98121 | $153.79 | 196 |
| 98109 | $150.25 | 202 |
| 98116 | $145.35 | 112 |

**Key Insight:** Downtown/waterfront zipcodes (98101, 98121, 98109) command the highest prices. The Queen Anne area (98119) is also a premium zone.

---

### 2. 🛏️ Average Price by Number of Bedrooms

A bar chart showing how nightly price scales with bedroom count across all 3,818 listings.

| Bedrooms | Avg Price | Listings |
|----------|-----------|----------|
| Studio (0) | $103.55 | 372 |
| 1 Bedroom | $95.71 | 2,417 |
| 2 Bedrooms | $174.06 | 640 |
| 3 Bedrooms | $249.53 | 283 |
| 4 Bedrooms | $313.70 | 69 |
| 5 Bedrooms | $441.00 | 24 |
| 6 Bedrooms | $578.17 | 6 |

**Key Insight:** Price scales consistently with bedroom count. 1-bedroom units make up the majority of listings (2,417) and are the most competitive segment at an average of $95.71/night.

---

### 3. 📅 Revenue by Week (Line Chart)

Using the Calendar sheet (~1M rows of daily availability/price data), a weekly revenue trend chart was built by aggregating revenue from booked nights (where `available = false`) across all listings throughout the year.

**Key Insight:** Revenue shows clear seasonal peaks in summer months, with bookings and revenue dropping in winter — helping hosts identify optimal pricing windows.

---

### 4. 🏠 Listing Count by Bedroom

A count chart showing the distribution of listings across bedroom sizes, helping identify market saturation at each tier.

- **1-bedroom listings dominate** at 2,417 (63% of all listings)
- 2-bedroom units are the second most common at 640
- Larger homes (4+ beds) are rare but command premium prices

---

### 5. 🗺️ Room Type Breakdown

| Room Type | Count | Share |
|-----------|-------|-------|
| Entire home/apt | 2,541 | 66.5% |
| Private room | 1,160 | 30.4% |
| Shared room | 117 | 3.1% |

**Key Insight:** Two-thirds of Seattle AirBnB listings are entire homes/apartments, signaling strong demand for private, hotel-like stays over shared accommodation.

---

### 6. 🏘️ Top Neighbourhoods by Listing Count

| Neighbourhood | Listings |
|---------------|----------|
| Broadway | 397 |
| Belltown | 234 |
| Wallingford | 167 |
| Fremont | 158 |
| Minor | 135 |
| University District | 122 |
| Stevens | 119 |
| First Hill | 108 |
| Central Business District | 103 |
| Lower Queen Anne | 94 |

**Key Insight:** Broadway leads in listing volume by a wide margin. The top 10 neighbourhoods all cluster around central Seattle and popular tourist areas.

---

## 🗃️ Data Connections in Tableau

The three sheets were connected as separate data sources in Tableau:
- **Listings** — primary source for all property-level analysis
- **Calendar** — joined for revenue and availability trend charts (daily granularity)
- **Reviews** — used for review count and recency analysis

---

## 💡 Key Tableau Skills Demonstrated

- **Map visualizations** — filled map with zipcode-level price encoding
- **Calculated fields** — revenue = price × booked nights from Calendar
- **Data blending / joins** — connecting Listings, Calendar, and Reviews sheets
- **Filters & parameters** — interactive filters by zipcode, room type, bedroom count
- **Dashboard design** — combining 5+ charts into a single interactive view
- **Date aggregation** — grouping Calendar data by week for trend analysis
- **LOD expressions** — for per-listing and per-zipcode aggregations
