import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    layout="wide",
    page_title="Berlin Emergency Grid | District Intelligence"
)

# =========================
# FUTURISTIC UI STYLE (2035)
# =========================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top left, #0a1a2f, #020617 70%);
    color: #e5f0ff;
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

p {
    font-size: 17px;
    line-height: 1.65;
    color: #cfdcff;
}

label {
    font-size: 15px !important;
    color: #9fb4ff !important;
}

/* Selectbox */
div[data-baseweb="select"] {
    background-color: rgba(15, 30, 60, 0.85);
    border-radius: 14px;
}

/* Subtle glow */
.glow {
    text-shadow: 0 0 12px rgba(0, 180, 255, 0.4);
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown(
    """
    Monitoring long-term emergency pressure through
    **predictive historical trends and spatial intelligence**.
    """
)

st.markdown("---")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(
    "/Users/deekshithsathrasalagangadharaiah/BF-Open-Data/Datasets/Berlin_Missions_2020_2025.csv",
    parse_dates=["mission_created_date"]
)

df["Year"] = df["mission_created_date"].dt.year

# =========================
# DISTRICT CONTROL
# =========================
st.markdown("### 📡 District Selector")

district = st.selectbox(
    "",
    sorted(df["mission_location_district"].dropna().unique())
)

df_d = df[df["mission_location_district"] == district]

# =========================
# TREND DATA
# =========================
yearly = (
    df_d.groupby("Year")
    .size()
    .reset_index(name="Incident Load")
)

# =========================
# FUTURISTIC AREA CHART
# =========================
fig = px.area(
    yearly,
    x="Year",
    y="Incident Load",
    markers=True,
    color_discrete_sequence=["#00E5FF"]
)

fig.update_layout(
    template="plotly_dark",
    height=480,
    title=f"Emergency Load Projection – {district}",
    title_x=0.5,
    xaxis_title="Time Axis",
    yaxis_title="Incident Density",
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
# INTELLIGENCE NOTE
# =========================
st.markdown(
    """
    **System Interpretation**  
    Rising curves indicate increasing **operational load** and sustained
    emergency pressure. Such intelligence supports **predictive deployment
    planning and autonomous resource allocation**.
    """
)
