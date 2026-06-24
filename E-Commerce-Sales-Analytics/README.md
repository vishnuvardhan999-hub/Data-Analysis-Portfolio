# 🛒 E-Commerce Sales Analytics Dashboard

An interactive business intelligence dashboard built with **Python, Plotly, and Streamlit**  
deployed publicly on **Streamlit Community Cloud**.

---

## 🔗 Live Demo
> **[👉 Click here to view the live dashboard](#)**  
> *(Replace this link with your Streamlit Cloud URL after deployment)*

---

## 📊 What's Inside

| Section | Charts | Business Question |
|---------|--------|-------------------|
| 📌 KPIs | 5 metric cards | What does the business look like at a glance? |
| 📈 Revenue | Monthly trend (area+line) | Is revenue growing? Any seasonal peaks? |
| 📦 Products | Top 10 by Revenue + Quantity | Which products make money vs sell volume? |
| 🌍 Countries | Bar chart + Choropleth map | Which countries drive sales globally? |
| 👥 Customers | Top 15 by Revenue | Who are our biggest customers? |
| 🎯 RFM | Segment donut + Revenue by segment | What types of customers do we have? |
| 🔬 Advanced | Revenue contribution % + Correlation heatmap | What % from each segment? What drives revenue? |

---

## 🛠️ Tech Stack
- **Python 3.12**
- **Pandas** — data cleaning & transformation
- **Plotly** — interactive charts
- **Streamlit** — web app framework & deployment
- **RFM Analysis** — customer segmentation (Recency, Frequency, Monetary)

---

## 📁 Project Structure
```
├── app.py               # Streamlit dashboard (main file)
├── OnlineRetail.csv     # Dataset (UCI Online Retail)
├── requirements.txt     # Python dependencies
├── .streamlit/
│   └── config.toml      # Dark theme configuration
└── README.md
```

---

## 🚀 Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Open http://localhost:8501 in your browser.

---

## 📦 Dataset
- **Source:** [UCI Machine Learning Repository — Online Retail](https://archive.ics.uci.edu/ml/datasets/Online+Retail)
- **Period:** December 2010 – December 2011
- **Records:** ~500K transactions across 37 countries
- **After cleaning:** ~398K rows, 4,338 customers, 18,532 orders
