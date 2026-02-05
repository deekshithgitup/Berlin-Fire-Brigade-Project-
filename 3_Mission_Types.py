import streamlit as st
import pandas as pd
import plotly.express as px

# ============================
# PAGE CONFIG
# ============================
st.set_page_config(
    page_title="Berlin Emergency Grid | Mission Intelligence",
    layout="wide"
)

# ============================
# FUTURISTIC 2035 UI
# ============================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top right, #081a2f, #020617 70%);
    color: #e6f0ff;
    font-family: 'Inter', sans-serif;
}

h1 {
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: 1px;
}

h3 {
    font-weight: 500;
    opacity: 0.85;
}

p, li {
    font-size: 17px;
    line-height: 1.65;
    color: #cfdcff;
}

.glow {
    text-shadow: 0 0 14px rgba(0, 200, 255, 0.45);
}

/* Subtle futuristic container feel */
.block-container {
    padding-top: 2.5rem;
}
</style>
""", unsafe_allow_html=True)

# ============================
# HEADER
# ============================
st.markdown(
    """
    Evaluating how **emergency mission types influence response performance**
    through long-term operational intelligence.
    """
)

st.markdown("---")

# ============================
# LOAD DATA
# ============================
@st.cache_data
def load_data():
    return pd.read_csv(
        "/Users/deekshithsathrasalagangadharaiah/BF-Open-Data/Datasets/Berlin_Missions_2020_2025.csv",
        parse_dates=["mission_created_date"],
        low_memory=False
    )

df = load_data()

# ============================
# CLEANING
# ============================
df = df.dropna(subset=["response_time", "mission_type"])
df = df[df["response_time"] > 0]

# ============================
# AGGREGATION
# ============================
mission_rt = (
    df.groupby("mission_type", as_index=False)
    .agg(
        avg_response_time=("response_time", "mean"),
        total_incidents=("response_time", "count")
    )
)

# ============================
# FUTURISTIC BUBBLE CHART
# ============================
fig = px.scatter(
    mission_rt,
    x="avg_response_time",
    y="mission_type",
    size="total_incidents",
    color="avg_response_time",
    color_continuous_scale="Turbo",
    labels={
        "avg_response_time": "Average Response Time (seconds)",
        "mission_type": "Emergency Classification"
    },
    title="Mission Complexity vs Response Load"
)

fig.update_layout(
    template="plotly_dark",
    height=620,
    title_x=0.5,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#d6e4ff")
)

fig.update_traces(
    marker=dict(
        line=dict(width=1, color="rgba(255,255,255,0.25)"),
        opacity=0.85
    )
)

st.plotly_chart(fig, use_container_width=True)

# ============================
# SYSTEM INTERPRETATION
# ============================
st.markdown(
    """
    ### 🧠 System Interpretation
    - High-complexity missions exhibit **elevated response durations**
    - High-frequency mission types dominate **resource consumption**
    - Bubble density reveals **operational stress concentration**

    ### 🎯 Strategic Value
    Enables:
    - Adaptive unit specialization  
    - Priority-based dispatch logic  
    - Predictive emergency readiness models  
    """
)
