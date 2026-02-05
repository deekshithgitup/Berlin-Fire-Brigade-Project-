import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Berlin Emergency Response | Overview",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CUSTOM CSS (UI STYLING)
# =========================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
    }

    h1, h2, h3 {
        font-weight: 700;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.08);
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }

    .metric-title {
        font-size: 16px;
        opacity: 0.8;
    }

    .metric-value {
        font-size: 30px;
        font-weight: bold;
        margin-top: 5px;
    }

    .section-card {
        background: rgba(255, 255, 255, 0.06);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 8px 28px rgba(0,0,0,0.35);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# TITLE & INTRO
# =========================
st.markdown(
    """
    <h1>🚨 Berlin Emergency Response</h1>
    <p style="font-size:18px; opacity:0.85;">
    A high-level analytical overview of emergency operations in Berlin using
    mission and regional data from <b>2020 to 2025</b>.
    </p>
    """,
    unsafe_allow_html=True
)

# =========================
# LOAD DATA
# =========================
DATA_PATH = "/Users/deekshithsathrasalagangadharaiah/BF-Open-Data/Datasets/Berlin_Missions_2020_2025.csv"

df = pd.read_csv(
    DATA_PATH,
    parse_dates=["mission_created_date"],
    low_memory=False
)

df = df.drop(columns=["Unnamed: 0"], errors="ignore")
df["year"] = df["mission_created_date"].dt.year

# =========================
# TRANSLATE MISSION TYPES
# =========================
mission_map = {
    "Rettungsdienst": "Emergency Medical Service",
    "Notfallrettung": "Emergency Rescue",
    "Brand": "Fire Incident",
    "Technische Hilfeleistung": "Technical Rescue",
    "Krankentransport": "Patient Transport"
}

df["mission_type_en"] = df["mission_type"].map(mission_map).fillna("Other")

# =========================
# KPI METRICS (CUSTOM CARDS)
# =========================
st.markdown("### 📊 Key Operational Metrics")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">🚑 Total Incidents</div>
            <div class="metric-value">{len(df):,}</div>
        </div>
        """, unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">📍 Districts Covered</div>
            <div class="metric-value">{df['mission_location_district'].nunique()}</div>
        </div>
        """, unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">📅 Years Covered</div>
            <div class="metric-value">{df['year'].min()} – {df['year'].max()}</div>
        </div>
        """, unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">⏱ Avg Response Time (sec)</div>
            <div class="metric-value">{round(df['response_time'].mean(), 1)}</div>
        </div>
        """, unsafe_allow_html=True
    )

# =========================
# INCIDENT TREND
# =========================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("📈 Emergency Incident Trend Over Time")

yearly = df.groupby("year").size().reset_index(name="incident_count")

fig1 = px.line(
    yearly,
    x="year",
    y="incident_count",
    markers=True,
    color_discrete_sequence=["#00E5FF"]
)

fig1.update_layout(
    template="plotly_dark",
    height=420,
    xaxis_title="Year",
    yaxis_title="Number of Incidents"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown(
    """
    **Insight:**  
    The trend highlights the long-term growth and fluctuations in emergency demand,
    supporting strategic planning and resource allocation.
    """
)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# MISSION TYPE DISTRIBUTION
# =========================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("🚒 Distribution of Emergency Incident Types")

mission_mix = df["mission_type_en"].value_counts().reset_index()
mission_mix.columns = ["Mission Type", "Incident Count"]

fig2 = px.pie(
    mission_mix,
    names="Mission Type",
    values="Incident Count",
    hole=0.65,
    color_discrete_sequence=[
        "#00E5FF", "#1E90FF", "#2ECC71", "#F39C12", "#9B59B6"
    ]
)

fig2.update_traces(textinfo="percent+label")
fig2.update_layout(
    template="plotly_dark",
    height=460
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """
    **Insight:**  
    Medical-related incidents dominate emergency operations, underlining the critical
    importance of ambulance services and paramedic availability.
    """
)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# REGIONAL CONTEXT
# =========================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("🗺 Regional Data Context")

st.markdown(
    """
    - Emergency incidents show **clear geographical variation** across Berlin  
    - Regional insights enable **data-driven deployment strategies**  
    - Detailed district-level analysis follows in subsequent sections
    """
)

st.success("✅ Overview completed — proceed to regional and operational deep dives")
st.markdown('</div>', unsafe_allow_html=True)
