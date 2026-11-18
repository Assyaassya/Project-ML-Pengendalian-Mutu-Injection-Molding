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
# CUSTOM CSS - TAMPILAN DASHBOARD
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* BACKGROUND UTAMA: gradient kuat + aksen warna */
    .stApp,
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 8% 8%, rgba(56, 139, 253, 0.28) 0%, transparent 34%),
            radial-gradient(ellipse at 92% 14%, rgba(164, 102, 230, 0.25) 0%, transparent 32%),
            radial-gradient(ellipse at 78% 92%, rgba(255, 133, 174, 0.22) 0%, transparent 34%),
            linear-gradient(125deg, #dcecff 0%, #e9e1ff 38%, #ffe4ef 72%, #fff0d8 100%) !important;
        background-attachment: fixed !important;
    }

    /* Jangan biarkan area konten Streamlit menimpa background */
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    .main,
    .main .block-container {
        background: transparent !important;
    }

    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.35) !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #142b4d 0%, #253b70 52%, #3c3478 100%);
        border-right: 1px solid #344d82;
    }

    [data-testid="stSidebar"] * {
        color: #edf3fb !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-baseweb="input"] > div {
        background: #1d2c40 !important;
        border: 1px solid #34465d !important;
        border-radius: 10px !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #c4d0df !important;
    }

    [data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stTickBar"] {
        background: #34465d;
    }

    .main .block-container {
        max-width: 1440px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    /* Panel konten putih transparan agar warna latar tetap terlihat */
    [data-testid="stMainBlockContainer"] {
        background: rgba(255, 255, 255, 0.48) !important;
        border: 1px solid rgba(255, 255, 255, 0.72);
        border-radius: 24px;
        box-shadow: 0 12px 34px rgba(64, 76, 145, 0.08);
        backdrop-filter: blur(8px);
    }

    .hero {
        background: linear-gradient(115deg, #123b70 0%, #176b87 38%, #6250a4 72%, #9a4f83 100%);
        padding: 30px 34px;
        border-radius: 20px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 28px rgba(18, 59, 112, 0.22);
    }

    .hero h1 {
        margin: 0 0 8px 0;
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
    }

    .hero p {
        margin: 0;
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.88);
    }

    .card {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 6px 20px rgba(31, 41, 55, 0.06);
        margin-bottom: 16px;
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
# LOAD MODEL ML (SESUAIKAN NAMA FILE MODEL ANDA)
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
        # Fallback simulasi jika file .joblib belum diunggah ke folder
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
    ax.patch.set_alpha(0.3)

    normalized_vals = [
        (melt_temp - 180) / (280 - 180) * 100,
        (mold_temp - 20) / (90 - 20) * 100,
        (injection_pressure - 500) / (1800 - 500) * 100,
        (holding_pressure - 300) / (1400 - 300) * 100,
        (cooling_time - 5) / (45 - 5) * 100,
        (cycle_time - 15) / (90 - 15) * 100,
    ]
    labels = ["Melt Temp", "Mold Temp", "Inj. Press", "Hold Press", "Cooling", "Cycle"]

    sns.barplot(x=normalized_vals, y=labels, palette="viridis", ax=ax)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Persentase terhadap Rentang Operasi (%)")
    ax.set_title("Distribusi Relatif Parameter Proses")
    st.pyplot(fig)
