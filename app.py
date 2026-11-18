import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="QC Injection Molding Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS - TEMA BLACK PINK
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* BACKGROUND UTAMA: Hitam pekat + aksen glow pink */
    .stApp,
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 10% 10%, rgba(255, 46, 136, 0.24) 0%, transparent 38%),
            radial-gradient(ellipse at 90% 15%, rgba(219, 39, 119, 0.20) 0%, transparent 35%),
            radial-gradient(ellipse at 80% 90%, rgba(244, 114, 182, 0.16) 0%, transparent 38%),
            linear-gradient(135deg, #07070a 0%, #110b14 48%, #1a0c18 100%) !important;
        background-attachment: fixed !important;
        color: #f8fafc !important;
    }

    /* Jangan biarkan area konten Streamlit menimpa background */
    [data-testid="stMain"],
    .main,
    .main .block-container {
        background: transparent !important;
    }

    /* Warna teks umum agar kontras di latar gelap */
    h1, h2, h3, h4, p, span, label, [data-testid="stMarkdownContainer"] {
        color: #f8fafc !important;
    }

    [data-testid="stHeader"] {
        background: rgba(10, 10, 14, 0.65) !important;
        backdrop-filter: blur(8px);
    }

    /* SIDEBAR: Hitam-pink elegan */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #09090d 0%, #170d16 55%, #261022 100%);
        border-right: 1px solid rgba(255, 46, 136, 0.35);
    }

    [data-testid="stSidebar"] * {
        color: #fce7f3 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-baseweb="input"] > div {
        background: #18121b !important;
        border: 1px solid rgba(255, 46, 136, 0.45) !important;
        border-radius: 10px !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #f9a8d4 !important;
    }

    /* Aksen slider pink */
    [data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
        background-color: #ff2e88 !important;
        border: 2px solid #ffffff !important;
    }

    .main .block-container {
        max-width: 1440px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    /* Panel konten gelap transparan dengan garis tepi pink */
    [data-testid="stMainBlockContainer"] {
        background: rgba(15, 13, 20, 0.76) !important;
        border: 1px solid rgba(255, 46, 136, 0.28);
        border-radius: 24px;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.55);
        backdrop-filter: blur(10px);
    }

    /* HERO BANNER */
    .hero {
        background: linear-gradient(115deg, #0b0b10 0%, #240b1b 42%, #9d174d 78%, #ff2e88 100%);
        border: 1px solid rgba(255, 105, 180, 0.4);
        padding: 30px 34px;
        border-radius: 20px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(255, 46, 136, 0.22);
    }

    .hero h1 {
        margin: 0 0 8px 0;
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff !important;
    }

    .hero p {
        margin: 0;
        font-size: 1rem;
        color: #fbcfe8 !important;
    }

    /* METRIC CARDS */
    [data-testid="stMetric"] {
        background: rgba(24, 18, 29, 0.85);
        border: 1px solid rgba(255, 46, 136, 0.3);
        border-radius: 16px;
        padding: 16px 20px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
    }

    [data-testid="stMetricLabel"] p {
        color: #f9a8d4 !important;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #ff4da6 !important;
        font-weight: 800;
    }

    hr {
        border-color: rgba(255, 46, 136, 0.25) !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO BANNER
# =========================================================
st.markdown("""
<div class="hero">
    <h1>🏭 Quality Control — Injection Molding</h1>
    <p>Sistem Prediksi & Monitoring Mutu Produk Berbasis Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR - INPUT PARAMETER MESIN
# =========================================================
st.sidebar.header("⚙️ Parameter Proses Mesin")

melt_temp = st.sidebar.slider("Melt Temperature (°C)", 180.0, 280.0, 225.0, 0.5)
mold_temp = st.sidebar.slider("Mold Temperature (°C)", 20.0, 90.0, 50.0, 0.5)
injection_pressure = st.sidebar.slider("Injection Pressure (bar)", 500.0, 1800.0, 1100.0, 10.0)
holding_pressure = st.sidebar.slider("Holding Pressure (bar)", 300.0, 1400.0, 800.0, 10.0)
cooling_time = st.sidebar.slider("Cooling Time (detik)", 5.0, 45.0, 18.0, 0.5)
cycle_time = st.sidebar.slider("Cycle Time (detik)", 15.0, 90.0, 35.0, 0.5)

input_df = pd.DataFrame({
    "Melt_Temp": [melt_temp],
    "Mold_Temp": [mold_temp],
    "Injection_Pressure": [injection_pressure],
    "Holding_Pressure": [holding_pressure],
    "Cooling_Time": [cooling_time],
    "Cycle_Time": [cycle_time]
})

# =========================================================
# LOAD MODEL ML
# =========================================================
MODEL_PATH = "model_qc_injection.joblib"

@st.cache_resource
def load_model(path):
    if os.path.exists(path):
        return joblib.load(path)
    return None

model = load_model(MODEL_PATH)

# =========================================================
# RINGKASAN METRIK & PREDIKSI
# =========================================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Melt Temp", f"{melt_temp} °C")
col2.metric("Mold Temp", f"{mold_temp} °C")
col3.metric("Injection Pressure", f"{injection_pressure} bar")
col4.metric("Cycle Time", f"{cycle_time} dtk")

st.markdown("---")

left_col, right_col = st.columns([1, 1.3])

with left_col:
    st.subheader("🔍 Hasil Evaluasi Mutu")
    if model is not None:
        pred = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0] if hasattr(model, "predict_proba") else None
        if pred == 1 or str(pred).upper() in ["OK", "PASS", "GOOD"]:
            st.success(f"**Status Produk: LOLOS QC ({pred})**")
        else:
            st.error(f"**Status Produk: POTENSI DEFECT / NG ({pred})**")
        if proba is not None:
            st.write(f"Tingkat Keyakinan Model: **{np.max(proba) * 100:.2f}%**")
    else:
        is_ok = (205 <= melt_temp <= 245) and (900 <= injection_pressure <= 1350) and (cooling_time >= 12)
        if is_ok:
            st.success("**Status Produk: LOLOS QC (OK)** — *Mode Simulasi*")
        else:
            st.warning("**Status Produk: RISIKO DEFECT (NG)** — *Mode Simulasi*")
        st.caption(f"Catatan: Letakkan file `{MODEL_PATH}` di folder project untuk menggunakan model terlatih.")

    st.dataframe(input_df, use_container_width=True)

with right_col:
    st.subheader("📊 Profil Parameter Saat Ini")
    fig, ax = plt.subplots(figsize=(7, 3.8))
    fig.patch.set_alpha(0.0)
    ax.set_facecolor((0.08, 0.06, 0.11, 0.65))

    normalized_vals = [
        (melt_temp - 180) / (280 - 180) * 100,
        (mold_temp - 20) / (90 - 20) * 100,
        (injection_pressure - 500) / (1800 - 500) * 100,
        (holding_pressure - 300) / (1400 - 300) * 100,
        (cooling_time - 5) / (45 - 5) * 100,
        (cycle_time - 15) / (90 - 15) * 100,
    ]
    labels = ["Melt Temp", "Mold Temp", "Inj. Press", "Hold Press", "Cooling", "Cycle"]
    pink_palette = ["#ff2e88", "#f43f8e", "#ec4899", "#db2777", "#f472b6", "#be185d"]

    sns.barplot(x=normalized_vals, y=labels, palette=pink_palette, ax=ax)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Persentase terhadap Rentang Operasi (%)", color="#fbcfe8")
    ax.set_title("Distribusi Relatif Parameter Proses", color="#ffffff", fontweight="bold")
    ax.tick_params(colors="#fce7f3")
    for spine in ax.spines.values():
        spine.set_color("#ff2e88")
        spine.set_alpha(0.4)

    st.pyplot(fig)
