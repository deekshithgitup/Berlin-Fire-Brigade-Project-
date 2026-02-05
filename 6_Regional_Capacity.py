import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Berlin Emergency Grid | Regional Capacity",
    layout="wide"
)

# =========================
# FUTURISTIC 2035 UI
# =========================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top right, #081a2f, #020617 70%);
    color: #e6f0ff;
    font-family: 'Inter', sans-serif;
}

h1 {
    font-size: 2.7rem;
    font-weight: 700;
    letter-spacing: 1px;
}

p {
    font-size: 17px;
    line-height: 1.6;
    color: #cfdcff;
}

label {
    color: #9fb4ff !important;
}

.glow {
    text-shadow: 0 0 14px rgba(0, 200, 255, 0.45);
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown(
    """
    # 🏙 Regional Capacity Intelligence  
    <span class="glow">Berlin Emergency Grid • Infrastructure Load Analysis</span>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    Monitoring **regional emergency workload trends** to assess
    infrastructure capacity, staffing pressure, and long-term readiness.
    """
)

st.markdown("---")

# =========================
# LOAD DATA
# =========================
REGIONAL_PATH = "/Users/deekshithsathrasalagangadharaiah/BF-Open-Data/Datasets/Berlin_Regional_2020_2025.csv"

df = pd.read_csv(REGIONAL_PATH, low_memory=False)

# =========================
# CONTROLS
# =========================
district = st.selectbox(
    "📡 District Area",
    sorted(
        df["district_area_name"]
        .dropna()
        .astype(str)
        .unique()
    )
)

df_d = df[df["district_area_name"] == district]

# =========================
# FUTURISTIC CAPACITY TREND
# =========================
fig = px.area(
    df_d,
    x="source_year",
    y="mission_count_all",
    markers=True,
    color_discrete_sequence=["#00E5FF"],
    labels={
        "source_year": "Operational Year",
        "mission_count_all": "Total Mission Load"
    },
    title=f"Regional Emergency Workload — {district}"
)

fig.update_layout(
    template="plotly_dark",
    height=480,
    title_x=0.5,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#d6e4ff")
)

fig.update_traces(
    line=dict(width=3),
    marker=dict(size=7)
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# SYSTEM STORY
# =========================
st.markdown(
    """
    ### 🧠 System Interpretation
    - Rising curves indicate **increasing regional workload**
    - Sustained growth suggests **capacity saturation risk**
    - Patterns support **station placement and staffing optimization**

    **Operational Value**  
    Enables data-driven decisions for:
    - Regional staffing allocation  
    - Infrastructure expansion planning  
    - Long-term emergency resilience  
    """
)
