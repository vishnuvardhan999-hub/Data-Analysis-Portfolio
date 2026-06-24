"""
E-Commerce Sales Analytics — Streamlit Dashboard
Deploy: Streamlit Community Cloud  →  share.streamlit.io
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# THEME COLOURS
# ─────────────────────────────────────────────────────────────────────────────
INDIGO = "#6366F1"
CYAN   = "#22D3EE"
AMBER  = "#F59E0B"
GREEN  = "#10B981"
ROSE   = "#F43F5E"
VIOLET = "#A78BFA"
MUTED  = "#94A3B8"
BG     = "#0F172A"
CARD   = "#1E293B"
BORDER = "#334155"

SEG_COLORS = {
    "Champions":           INDIGO,
    "Loyal Customers":     GREEN,
    "Potential Loyalists": CYAN,
    "At Risk":             AMBER,
    "Lost Customers":      ROSE,
    "Others":              VIOLET,
}

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL PLOTLY LAYOUT
# ─────────────────────────────────────────────────────────────────────────────
BASE = dict(
    paper_bgcolor=CARD, plot_bgcolor=CARD,
    font=dict(color="#F1F5F9", family="Inter, sans-serif", size=12),
    margin=dict(l=48, r=24, t=44, b=44),
    xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zerolinecolor=BORDER),
    yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zerolinecolor=BORDER),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)
BASE_LAYOUT = BASE  # alias used throughout charts
CORR_BASE = {k: v for k, v in BASE.items() if k not in ("xaxis", "yaxis")}

# ─────────────────────────────────────────────────────────────────────────────
# LOAD & CLEAN  (cached so it only runs once)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "OnlineRetail.csv")
    df = pd.read_csv(path, encoding="ISO-8859-1", dtype={"CustomerID": str})
    df.dropna(subset=["CustomerID"], inplace=True)
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], dayfirst=False)
    df["Revenue"]     = df["Quantity"] * df["UnitPrice"]
    df["YearMonth"]   = df["InvoiceDate"].dt.to_period("M").astype(str)

    # RFM on full dataset
    snap = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm  = df.groupby("CustomerID").agg(
        Recency   = ("InvoiceDate", lambda x: (snap - x.max()).days),
        Frequency = ("InvoiceNo",   "nunique"),
        Monetary  = ("Revenue",     "sum"),
    ).reset_index()
    rfm["R"] = pd.qcut(rfm["Recency"],   5, labels=[5,4,3,2,1]).astype(int)
    rfm["F"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    rfm["M"] = pd.qcut(rfm["Monetary"],  5, labels=[1,2,3,4,5]).astype(int)

    def seg(row):
        r, f, m = row["R"], row["F"], row["M"]
        if r >= 4 and f >= 4 and m >= 4: return "Champions"
        if r >= 3 and f >= 3:             return "Loyal Customers"
        if r >= 3 and f <= 2:             return "Potential Loyalists"
        if r == 2 and f >= 2:             return "At Risk"
        if r <= 1:                        return "Lost Customers"
        return "Others"

    rfm["Segment"] = rfm.apply(seg, axis=1)
    df = df.merge(rfm[["CustomerID", "Segment"]], on="CustomerID", how="left")
    return df

df_all = load_data()
ALL_COUNTRIES = sorted(df_all["Country"].unique())


def rfm_for(d):
    """Recompute RFM for a (possibly filtered) dataframe."""
    snap = d["InvoiceDate"].max() + pd.Timedelta(days=1)
    r = d.groupby("CustomerID").agg(
        Recency   = ("InvoiceDate", lambda x: (snap - x.max()).days),
        Frequency = ("InvoiceNo",   "nunique"),
        Monetary  = ("Revenue",     "sum"),
    ).reset_index()
    if len(r) < 5:
        r["Segment"] = "Others"
        return r

    def seg(row):
        rv, f, m = row["R"], row["F"], row["M"]
        if rv >= 4 and f >= 4 and m >= 4: return "Champions"
        if rv >= 3 and f >= 3:             return "Loyal Customers"
        if rv >= 3 and f <= 2:             return "Potential Loyalists"
        if rv == 2 and f >= 2:             return "At Risk"
        if rv <= 1:                        return "Lost Customers"
        return "Others"

    r["R"] = pd.qcut(r["Recency"],   5, labels=[5,4,3,2,1]).astype(int)
    r["F"] = pd.qcut(r["Frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    r["M"] = pd.qcut(r["Monetary"],  5, labels=[1,2,3,4,5]).astype(int)
    r["Segment"] = r.apply(seg, axis=1)
    return r

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS  (dark theme polish)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* dark page background */
.stApp { background-color: #0F172A; }

/* sidebar */
[data-testid="stSidebar"] { background-color: #1E293B; border-right: 1px solid #334155; }
[data-testid="stSidebar"] * { color: #F1F5F9 !important; }

/* metric cards */
[data-testid="stMetric"] {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 18px 20px !important;
}
[data-testid="stMetricLabel"]  { color: #94A3B8 !important; font-size: 0.78rem !important; text-transform: uppercase; letter-spacing: 0.07em; }
[data-testid="stMetricValue"]  { color: #F1F5F9 !important; font-size: 1.7rem !important; font-weight: 800 !important; }
[data-testid="stMetricDelta"]  { color: #10B981 !important; }

/* section divider */
hr { border-color: #334155 !important; }

/* hide Streamlit branding */
#MainMenu, footer { visibility: hidden; }

/* section headers */
h2 { color: #F1F5F9 !important; }
h3 { color: #94A3B8 !important; font-size: 0.85rem !important;
     text-transform: uppercase; letter-spacing: 0.07em; font-weight: 600 !important; }

/* insight box */
.insight-box {
    background: rgba(245,158,11,0.08);
    border-left: 3px solid #F59E0B;
    border-radius: 0 8px 8px 0;
    padding: 10px 16px;
    margin-top: 8px;
    font-size: 0.83rem;
    color: #CBD5E1;
}
</style>
""", unsafe_allow_html=True)


def insight(text):
    st.markdown(f'<div class="insight-box">💡 <b>Insight:</b> {text}</div>',
                unsafe_allow_html=True)

def section(icon_title, question):
    st.markdown(f"## {icon_title}")
    st.caption(f"**Business Question:** {question}")
    st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR  — FILTER
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛒 E-Commerce Analytics")
    st.markdown("**Online Retail Dataset**")
    st.caption("Dec 2010 – Dec 2011")
    st.markdown("---")

    st.markdown("### 🌍 Filter by Country")
    country_choice = st.selectbox(
        label="country",
        options=["🌐 All Countries"] + ALL_COUNTRIES,
        index=0,
        label_visibility="collapsed",
    )
    selected = None if country_choice == "🌐 All Countries" else country_choice

    if selected:
        st.success(f"📍 Filtered: **{selected}**")
    else:
        st.info(f"Showing all **{len(ALL_COUNTRIES)}** countries")

    st.markdown("---")
    st.markdown("### 📑 Sections")
    st.markdown("""
- 📌 KPI Cards
- 📈 Revenue Analysis
- 📦 Product Analysis
- 🌍 Country Analysis
- 👥 Customer Analysis
- 🎯 RFM Segmentation
- 🔬 Advanced Insights
    """)
    st.markdown("---")
    st.caption("Built with Plotly + Streamlit")
    st.caption("Data: UCI Online Retail Dataset")


# ─────────────────────────────────────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────────────────────────────────────
df = df_all if selected is None else df_all[df_all["Country"] == selected]
rfm = rfm_for(df)

# per-customer revenue for this slice (used in RFM revenue charts)
crev = df.groupby("CustomerID")["Revenue"].sum().reset_index()
seg_rev_df = (crev.merge(rfm[["CustomerID","Segment"]], on="CustomerID", how="left")
                  .groupby("Segment")["Revenue"].sum()
                  .reset_index().sort_values("Revenue", ascending=False))

# ─────────────────────────────────────────────────────────────────────────────
# HEADER BANNER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#1E293B,#0F172A);
            padding:28px 32px;border-radius:16px;border:1px solid #334155;
            margin-bottom:28px;">
  <h1 style="margin:0;font-size:1.8rem;font-weight:800;color:#F1F5F9;letter-spacing:-0.02em;">
    🛒 E-Commerce Sales Analytics
  </h1>
  <p style="margin:6px 0 12px;color:#94A3B8;font-size:0.9rem;">
    Online Retail  •  Dec 2010 – Dec 2011  •  United Kingdom & Global
  </p>
  <span style="background:#6366F122;color:#6366F1;border:1px solid #6366F155;
               border-radius:99px;padding:3px 12px;font-size:0.75rem;font-weight:600;margin-right:8px;">
    📊 Recruiter-Ready Dashboard
  </span>
  <span style="background:#10B98122;color:#10B981;border:1px solid #10B98155;
               border-radius:99px;padding:3px 12px;font-size:0.75rem;font-weight:600;">
    ✅ RFM Segmented
  </span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — KPI CARDS
# ─────────────────────────────────────────────────────────────────────────────
section("📌 Section 1 — Key Performance Indicators",
        "What does the business look like at a glance?")

total_rev  = df["Revenue"].sum()
tot_orders = df["InvoiceNo"].nunique()
tot_custs  = df["CustomerID"].nunique()
aov        = df.groupby("InvoiceNo")["Revenue"].sum().mean() if tot_orders else 0
tot_prods  = df["StockCode"].nunique()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💰 Total Revenue",    f"£{total_rev/1e6:.2f}M")
c2.metric("📦 Total Orders",     f"{tot_orders:,}")
c3.metric("👥 Total Customers",  f"{tot_custs:,}")
c4.metric("🛒 Avg Order Value",  f"£{aov:,.0f}")
c5.metric("🛍️ Products Listed",  f"{tot_prods:,}")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — REVENUE ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
section("📈 Section 2 — Revenue Analysis",
        "Is revenue increasing over time? Are there seasonal peaks?")

mrev = df.groupby("YearMonth")["Revenue"].sum().reset_index(name="Revenue")
fig_monthly = go.Figure()
fig_monthly.add_trace(go.Scatter(
    x=mrev["YearMonth"], y=mrev["Revenue"],
    mode="lines+markers",
    line=dict(color=INDIGO, width=3),
    marker=dict(size=7, color=INDIGO),
    fill="tozeroy", fillcolor="rgba(99,102,241,0.15)",
    hovertemplate="<b>%{x}</b><br>Revenue: £%{y:,.0f}<extra></extra>",
))
fig_monthly.update_layout(**BASE_LAYOUT, height=320,
    title=dict(text="Monthly Revenue Trend", font=dict(size=13,color="#F1F5F9"), x=0),
    xaxis_tickangle=-30)
st.plotly_chart(fig_monthly, use_container_width=True)
insight("Revenue spikes in Nov–Dec (holiday season). Mid-year shows a steady growth plateau.")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — PRODUCT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
section("📦 Section 3 — Product Analysis",
        "Which products make the most money? Which sell the most units?")

p1, p2 = st.columns(2)

with p1:
    st.markdown("### Top 10 Products by Revenue")
    t = (df.groupby("Description")["Revenue"].sum()
           .reset_index().sort_values("Revenue", ascending=False).head(10))
    t["Description"] = t["Description"].str[:35]
    ts = t.sort_values("Revenue")
    fig = px.bar(ts, x="Revenue", y="Description", orientation="h",
                 color_discrete_sequence=[CYAN],
                 text=ts["Revenue"].apply(lambda v: f"£{v:,.0f}"))
    fig.update_traces(textposition="outside", textfont_color="#F1F5F9")
    fig.update_layout(**BASE_LAYOUT, height=340)
    st.plotly_chart(fig, use_container_width=True)
    insight("High-ticket gift items dominate revenue even if they don't top unit sales.")

with p2:
    st.markdown("### Top 10 Products by Quantity Sold")
    t = (df.groupby("Description")["Quantity"].sum()
           .reset_index().sort_values("Quantity", ascending=False).head(10))
    t["Description"] = t["Description"].str[:35]
    ts = t.sort_values("Quantity")
    fig = px.bar(ts, x="Quantity", y="Description", orientation="h",
                 color_discrete_sequence=[AMBER],
                 text=ts["Quantity"].apply(lambda v: f"{v:,}"))
    fig.update_traces(textposition="outside", textfont_color="#F1F5F9")
    fig.update_layout(**BASE_LAYOUT, height=340)
    st.plotly_chart(fig, use_container_width=True)
    insight("Volume leaders are low-cost novelty items — high demand, lower margin.")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — COUNTRY ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
section("🌍 Section 4 — Country Analysis",
        "Which countries drive sales? Where are our customers located globally?")

st.markdown("### Top 15 Countries by Revenue")
cr = (df.groupby("Country")["Revenue"].sum()
        .reset_index().sort_values("Revenue", ascending=False).head(15))
fig = px.bar(cr, x="Country", y="Revenue",
             color_discrete_sequence=[GREEN],
             text=cr["Revenue"].apply(lambda v: f"£{v/1000:.0f}K"))
fig.update_traces(textposition="outside", textfont_color="#F1F5F9")
fig.update_layout(**BASE_LAYOUT, height=340, xaxis_tickangle=-30)
st.plotly_chart(fig, use_container_width=True)
insight("Netherlands, EIRE and Germany are the top international markets after the UK.")

st.markdown("### World Revenue Map")
wr = df.groupby("Country")["Revenue"].sum().reset_index()
fig_map = px.choropleth(
    wr, locations="Country", locationmode="country names",
    color="Revenue", hover_name="Country",
    color_continuous_scale=[[0,"#1E293B"],[0.3,INDIGO],[1,CYAN]],
    labels={"Revenue":"Revenue (£)"},
)
fig_map.update_layout(**BASE_LAYOUT, height=420,
    geo=dict(bgcolor=CARD, showframe=False, showcoastlines=True,
             coastlinecolor=BORDER, showland=True, landcolor="#1E293B",
             showocean=True, oceancolor=BG))
fig_map.update_coloraxes(colorbar_tickfont_color="#F1F5F9",
                          colorbar_title_font_color="#F1F5F9")
st.plotly_chart(fig_map, use_container_width=True)
insight("Sales are heavily concentrated in Europe. Large growth opportunity in North America and Asia.")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — CUSTOMER ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
section("👥 Section 5 — Customer Analysis",
        "Who are our biggest customers?")

tc = (df.groupby("CustomerID")["Revenue"].sum()
        .reset_index().sort_values("Revenue", ascending=False).head(15))
tc["CustomerID"] = "Cust " + tc["CustomerID"]
ts = tc.sort_values("Revenue")
fig = px.bar(ts, x="Revenue", y="CustomerID", orientation="h",
             color_discrete_sequence=[VIOLET],
             text=ts["Revenue"].apply(lambda v: f"£{v:,.0f}"))
fig.update_traces(textposition="outside", textfont_color="#F1F5F9")
fig.update_layout(**BASE_LAYOUT, height=420)
st.plotly_chart(fig, use_container_width=True)
insight("Top 15 customers account for a disproportionate share of total revenue — classic Pareto pattern.")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 — RFM SEGMENTATION
# ─────────────────────────────────────────────────────────────────────────────
section("🎯 Section 6 — RFM Customer Segmentation",
        "What types of customers do we have? Which segments generate the most revenue?")

st.markdown("""
<div style="background:rgba(99,102,241,0.07);border:1px solid rgba(99,102,241,0.25);
            border-radius:8px;padding:10px 16px;margin-bottom:16px;font-size:0.85rem;color:#CBD5E1;">
  <b style="color:#F1F5F9;">RFM = Recency × Frequency × Monetary</b> &nbsp;—&nbsp;
  Customers scored 1–5 on each dimension and grouped into 5 strategic segments.
</div>
""", unsafe_allow_html=True)

r1, r2 = st.columns(2)

with r1:
    st.markdown("### Customer Segment Distribution")
    sd = rfm["Segment"].value_counts().reset_index()
    sd.columns = ["Segment","Count"]
    colors = [SEG_COLORS.get(s, MUTED) for s in sd["Segment"]]
    fig = go.Figure(go.Pie(
        labels=sd["Segment"], values=sd["Count"], hole=0.55,
        marker=dict(colors=colors, line=dict(color=BG, width=2)),
        textinfo="label+percent", textfont=dict(color="#F1F5F9", size=11),
        hovertemplate="<b>%{label}</b><br>Customers: %{value:,}<br>Share: %{percent}<extra></extra>",
    ))
    fig.update_layout(**BASE_LAYOUT, height=360, showlegend=True,
        annotations=[dict(text=f"<b>{rfm['Segment'].nunique()}<br>Segments</b>",
                          x=0.5, y=0.5, font=dict(size=14,color="#F1F5F9"), showarrow=False)])
    st.plotly_chart(fig, use_container_width=True)

with r2:
    st.markdown("### Revenue by Segment")
    fig = px.bar(seg_rev_df, x="Segment", y="Revenue",
                 color="Segment", color_discrete_map=SEG_COLORS,
                 text=seg_rev_df["Revenue"].apply(lambda v: f"£{v/1000:.0f}K"))
    fig.update_traces(textposition="outside", textfont_color="#F1F5F9")
    fig.update_layout(**BASE_LAYOUT, height=360, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 — ADVANCED INSIGHTS
# ─────────────────────────────────────────────────────────────────────────────
section("🔬 Section 7 — Advanced Insights",
        "Revenue contribution % by segment and correlation between key variables.")

a1, a2 = st.columns(2)

with a1:
    st.markdown("### Revenue Contribution % by Segment")
    colors = [SEG_COLORS.get(s, MUTED) for s in seg_rev_df["Segment"]]
    fig = go.Figure(go.Pie(
        labels=seg_rev_df["Segment"], values=seg_rev_df["Revenue"], hole=0.6,
        marker=dict(colors=colors, line=dict(color=BG, width=2)),
        textinfo="label+percent", textfont=dict(color="#F1F5F9", size=11),
        hovertemplate="<b>%{label}</b><br>Revenue: £%{value:,.0f}<br>Share: %{percent}<extra></extra>",
    ))
    fig.update_layout(**BASE_LAYOUT, height=360, showlegend=True,
        annotations=[dict(text="<b>Revenue<br>Share</b>", x=0.5, y=0.5,
                          font=dict(size=13,color="#F1F5F9"), showarrow=False)])
    st.plotly_chart(fig, use_container_width=True)
    insight("Champions drive the lion's share of revenue despite being a small customer group.")

with a2:
    st.markdown("### Correlation Heatmap")
    cm = df[["Quantity","UnitPrice","Revenue"]].corr().round(2)
    z  = cm.values.tolist()
    fig = go.Figure(go.Heatmap(
        z=z, x=cm.columns.tolist(), y=cm.index.tolist(),
        colorscale=[[0,ROSE],[0.5,"#1E293B"],[1,GREEN]],
        zmin=-1, zmax=1,
        text=[[f"{v:.2f}" for v in row] for row in z],
        texttemplate="%{text}", textfont=dict(size=14,color="#F1F5F9"),
        hovertemplate="<b>%{y} vs %{x}</b><br>Correlation: %{z:.2f}<extra></extra>",
    ))
    fig.update_layout(**CORR_BASE, height=360,
        xaxis=dict(side="bottom", gridcolor=BORDER, linecolor=BORDER),
        yaxis=dict(autorange="reversed", gridcolor=BORDER, linecolor=BORDER))
    st.plotly_chart(fig, use_container_width=True)
    insight("Revenue correlates more with Quantity than UnitPrice — volume drives sales.")

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#475569;font-size:0.78rem;'>"
    "E-Commerce Sales Analytics Dashboard &nbsp;•&nbsp; Built with Plotly + Streamlit &nbsp;•&nbsp; "
    "Data: UCI Online Retail Dataset"
    "</p>",
    unsafe_allow_html=True,
)
