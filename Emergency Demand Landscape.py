import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Berlin Emergency Grid | District Map",
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
    font-size: 2.8rem;
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
def load_data():
    df = pd.read_csv(
        "/Users/deekshithsathrasalagangadharaiah/BF-Open-Data/Datasets/Berlin_Regional_2020_2025.csv",
        low_memory=False
    )
    return df

df = load_data()

# =========================
# HEADER
# =========================
st.markdown(
    """
    # 🗺 Emergency Demand Landscape  
    <span class="glow">Berlin Emergency Grid • District-Level Map</span>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
Zoom into **structural emergency pressure by district**.  
Treemap visualization highlights **where operational load is concentrated**.
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

df_y = (
    df[df["source_year"] == year]
    .groupby("district_area_name", as_index=False)
    .agg(total_incidents=("mission_count_all", "sum"))
)

# =========================
# FUTURISTIC TREEMAP
# =========================
fig = px.treemap(
    df_y,
    path=["district_area_name"],
    values="total_incidents",
    color="total_incidents",
    color_continuous_scale="Plasma",
    title=f"Relative Emergency Load by District ({year})"
)

fig.update_layout(
    template="plotly_dark",
    height=600,
    margin=dict(t=60, l=10, r=10, b=10),
    font=dict(color="#d6e4ff")
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# SYSTEM INTERPRETATION
# =========================
st.markdown(
    """
### 🧭 How to read this
- Larger blocks = higher emergency pressure  
- Darker colors = heavier operational load  
- Quickly identifies **hotspot districts**

### 🎯 Operational Value
- Enables **district-level resource allocation**  
- Supports **strategic station placement**  
- Preserves **spatial intuition** without map geometry complexity
"""
)
