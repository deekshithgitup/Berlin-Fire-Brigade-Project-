import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Berlin Emergency Grid | Spatial Intelligence",
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
    # 📍 Spatial Incident Intelligence  
    <span class="glow">Berlin Emergency Grid • Location-Based Analysis</span>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    Analyzing **mission composition by district and year**
    to understand localized emergency demand patterns.
    """
)

st.markdown("---")

# =========================
# LOAD DATA
# =========================
MISSION_PATH = "/Users/deekshithsathrasalagangadharaiah/BF-Open-Data/Datasets/Berlin_Missions_2020_2025.csv"

df = pd.read_csv(
    MISSION_PATH,
    parse_dates=["mission_created_date"],
    low_memory=False
)

df["year"] = df["mission_created_date"].dt.year

# =========================
# MISSION TYPE TRANSLATION
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
# CONTROLS
# =========================
col1, col2 = st.columns(2)

with col1:
    district = st.selectbox(
        "📡 District",
        sorted(df["mission_location_district"].dropna().unique())
    )

with col2:
    year = st.selectbox(
        "🕒 Year",
        sorted(df["year"].unique())
    )

# =========================
# AGGREGATION
# =========================
counts = (
    df[
        (df["mission_location_district"] == district) &
        (df["year"] == year)
    ]
    .groupby("mission_type_en", as_index=False)
    .size()
    .rename(columns={"size": "incidents"})
    .sort_values("incidents", ascending=True)
)

# =========================
# FUTURISTIC BAR CHART
# =========================
fig = px.bar(
    counts,
    x="incidents",
    y="mission_type_en",
    orientation="h",
    color="incidents",
    color_continuous_scale="Turbo",
    labels={
        "incidents": "Number of Incidents",
        "mission_type_en": "Emergency Classification"
    },
    title=f"Incident Distribution — {district} ({year})"
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
# TRANSLATION TABLE
# =========================
st.markdown("### 📘 Mission Type Reference (German → English)")

translation_table = (
    df[["mission_type", "mission_type_en"]]
    .drop_duplicates()
    .sort_values("mission_type")
)

st.dataframe(
    translation_table,
    use_container_width=True,
    hide_index=True
)

# =========================
# SYSTEM NOTE
# =========================
st.markdown(
    """
    **System Insight**  
    The distribution highlights how **local risk profiles differ by district**.
    Dominant mission types indicate **area-specific emergency demand**, supporting
    targeted preparedness and unit specialization.
    """
)
