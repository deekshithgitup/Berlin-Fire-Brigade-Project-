import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Berlin Emergency Grid | Neighborhood Concentration",
    layout="wide"
)

# =========================
# FUTURISTIC 2035 UI
# =========================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top left, #081a2f, #020617 70%);
    color: #e6f0ff;
    font-family: 'Inter', sans-serif;
}

h1 {
    font-size: 2.7rem;
    font-weight: 700;
    letter-spacing: 1px;
}

p, li {
    font-size: 17px;
    line-height: 1.6;
    color: #cfdcff;
}

label {
    color: #9fb4ff !important;
}

.glow {
    text-shadow: 0 0 16px rgba(0, 200, 255, 0.5);
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_regional():
    df = pd.read_csv(
        "/Users/deekshithsathrasalagangadharaiah/BF-Open-Data/Datasets/Berlin_Regional_2020_2025.csv",
        low_memory=False
    )
    return df

df = load_regional()

# =========================
# HEADER
# =========================
st.markdown(
    """
    # 🏘️ Neighborhood Emergency Concentration  
    <span class="glow">Berlin Emergency Grid • Neighborhood-Level Analysis</span>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
Zoom into **structural emergency demand** at the neighborhood level.  
Identifies **high-pressure zones** for EMS and Fire services.
"""
)

st.markdown("---")

# =========================
# YEAR SELECTION
# =========================
year = st.selectbox(
    "📅 Select Year",
    sorted(df["source_year"].dropna().astype(int).unique())
)

df_y = df[df["source_year"] == year].copy()

# =========================
# PREPARE DATA
# =========================
neighborhood_stats = (
    df_y
    .groupby("district_area_name", as_index=False)
    .agg(
        total_incidents=("mission_count_all", "sum"),
        ems_incidents=("mission_count_ems", "sum"),
        fire_incidents=("mission_count_fire", "sum")
    )
    .sort_values("total_incidents", ascending=False)
    .head(15)
)

# =========================
# NEON BAR CHART
# =========================
fig = px.bar(
    neighborhood_stats,
    x="total_incidents",
    y="district_area_name",
    orientation="h",
    color="total_incidents",
    color_continuous_scale="Turbo",
    labels={
        "district_area_name": "Neighborhood",
        "total_incidents": "Total Emergency Incidents"
    },
    title=f"Top 15 Neighborhoods by Emergency Volume ({year})"
)

fig.update_layout(
    template="plotly_dark",
    height=600,
    title_x=0.5,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(categoryorder="total ascending"),
    font=dict(color="#d6e4ff")
)

fig.update_traces(
    marker=dict(line=dict(width=1, color="rgba(255,255,255,0.25)"), opacity=0.85)
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# KPI METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Incidents (Top 15)",
    f"{neighborhood_stats['total_incidents'].sum():,}"
)

col2.metric(
    "EMS Share",
    f"{(neighborhood_stats['ems_incidents'].sum() / neighborhood_stats['total_incidents'].sum())*100:.1f}%"
)

col3.metric(
    "Fire Share",
    f"{(neighborhood_stats['fire_incidents'].sum() / neighborhood_stats['total_incidents'].sum())*100:.1f}%"
)

# =========================
# SYSTEM INTERPRETATION
# =========================
st.markdown(
    """
### 🔍 Interpretation
- A few neighborhoods carry **disproportionate emergency demand**  
- These represent **structural risk zones**  
- EMS dominates, highlighting **medical emergencies as primary pressure**

### 🎯 Operational Impact
Supports:
- Targeted station placement  
- Neighborhood-specific prevention & outreach  
- Evidence-based urban safety planning  
"""
)
