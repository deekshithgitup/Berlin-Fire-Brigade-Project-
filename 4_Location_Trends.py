import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Berlin Emergency Grid | Temporal Stress",
    layout="wide"
)

# =========================
# FUTURISTIC 2035 UI
# =========================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at bottom left, #0a1a2f, #020617 70%);
    color: #e6f0ff;
    font-family: 'Inter', sans-serif;
}

h1 {
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: 1px;
}

p, li {
    font-size: 17px;
    line-height: 1.65;
    color: #cfdcff;
}

.glow {
    text-shadow: 0 0 16px rgba(255, 100, 0, 0.45);
}

.block-container {
    padding-top: 2.5rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown(
    """
    # ⏱ Temporal Stress Intelligence  
    <span class="glow">Berlin Emergency Grid • Chrono-Operational Analysis</span>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    Identifying **time-based pressure zones** in emergency response operations by
    analyzing **hourly behavioral stress patterns** across weekdays and weekends.
    """
)

st.markdown("---")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv(
        "/Users/deekshithsathrasalagangadharaiah/BF-Open-Data/Datasets/Berlin_Missions_2020_2025.csv",
        parse_dates=["mission_created_date"],
        low_memory=False
    )

df = load_data()

# =========================
# FEATURE ENGINEERING
# =========================
df["hour"] = df["mission_created_date"].dt.hour
df["weekday"] = df["mission_created_date"].dt.day_name()
df["is_weekend"] = df["mission_created_date"].dt.weekday >= 5
df["day_type"] = df["is_weekend"].map({True: "Weekend", False: "Weekday"})

# =========================
# HEATMAP DATA
# =========================
heatmap = (
    df.groupby(["day_type", "hour"], as_index=False)
    .agg(avg_response_time=("response_time", "mean"))
)

# =========================
# FUTURISTIC HEATMAP
# =========================
fig = px.density_heatmap(
    heatmap,
    x="hour",
    y="day_type",
    z="avg_response_time",
    color_continuous_scale="Inferno",
    labels={
        "hour": "Chrono-Hour",
        "day_type": "Operational Mode",
        "avg_response_time": "Response Latency (sec)"
    },
    title="Chrono-Stress Distribution Across Emergency Operations"
)

fig.update_layout(
    template="plotly_dark",
    height=480,
    title_x=0.5,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#d6e4ff")
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# SYSTEM INTERPRETATION
# =========================
st.markdown(
    """
    ### 🧠 System Intelligence
    - **Night cycles and early mornings** exhibit elevated response latency  
    - **Weekend operational mode** consistently shows higher stress  
    - Temporal pressure is **systematic**, not incidental

    ### 🎯 Strategic Impact
    Enables:
    - Chrono-aware shift optimization  
    - Night-time reinforcement strategies  
    - Predictive staffing and fatigue mitigation  
    """
)
