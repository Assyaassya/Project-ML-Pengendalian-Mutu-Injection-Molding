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
    page_title="QC Injection Molding • Cute Black-Pink",
    page_icon="🎀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS - CUTE BLACK-PINK AESTHETIC
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Quicksand:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }

    h1, h2, h3, .cute-title {
        font-family: 'Fredoka', sans-serif !important;
        letter-spacing: 0.3px;
    }

    /* BACKGROUND UTAMA: Hitam velvet + pendaran soft & hot pink */
    .stApp,
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 12% 12%, rgba(255, 105, 180, 0.25) 0%, transparent 35%),
            radial-gradient(circle at 88% 18%, rgba(255, 46, 136, 0.22) 0%, transparent 38%),
            radial-gradient(circle at 75% 88%, rgba(244, 114, 182, 0.20) 0%, transparent 40%),
            linear-gradient(145deg, #09070c 0%, #140b16 50%, #1f0d1d 100%) !important;
        background-attachment: fixed !important;
        color: #fff1f7 !important;
    }

    [data-testid="stMain"],
    .main,
    .main .block-container {
        background: transparent !important;
    }

    h1, h2, h3, h4, p, span, label, [data-testid="stMarkdownContainer"] {
        color: #fff1f7 !important;
    }

    /* Styling inline code agar tidak putih silau */
    code {
        background-color: #2b1226 !important;
        color: #ff85c0 !important;
        border: 1px solid rgba(255, 105, 180, 0.4);
        border-radius: 8px;
        padding: 2px 7px;
        font-weight: 600;
    }

    [data-testid="stHeader"] {
        background: rgba(12, 9, 16, 0.6) !important;
        backdrop-filter: blur(10px);
    }

    /* SIDEBAR LUCU & ELEGAN */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b0810 0%, #190d1a 55%, #291026 100%);
        border-right: 2px dashed rgba(255, 105, 180, 0.38);
    }

    [data-testid="stSidebar"] * {
        color: #ffe4f1 !important;
    }

    [data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
        background: linear-gradient(135deg, #ff7eb3, #ff2e88) !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0 0 10px rgba(255, 46, 136, 0.8);
    }

    .main .block-container {
        max-width: 1420px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* PANEL UTAMA */
    [data-testid="stMainBlockContainer"] {
        background: rgba(18, 12, 22, 0.78) !important;
        border: 1.5px solid rgba(255, 133, 192, 0.32);
        border-radius: 30px;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6), inset 0 0 24px rgba(255, 46, 136, 0.08);
        backdrop-filter: blur(12px);
    }

    /* HERO BANNER LUCU */
    .hero-cute {
        background: linear-gradient(120deg, #160b18 0%, #3b0d2b 42%, #be185d 80%, #ff5ca8 100%);
        border: 2px solid rgba(255, 182, 217, 0.45);
        padding: 28px 34px;
        border-radius: 26px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 30px rgba(255, 46, 136, 0.25);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.4);
        color: #ffffff;
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .hero-cute h1 {
        margin: 0 0 6px 0;
        font-size: 2.05rem;
        font-weight: 700;
        color: #ffffff !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.25);
    }

    .hero-cute p {
        margin: 0;
        font-size: 1rem;
        color: #ffe4f2 !important;
        font-weight: 500;
    }

    /* KARTU METRIK LUCU DENGAN EFEK BOUNCE */
    .cute-metric-card {
        background: linear-gradient(160deg, rgba(33, 18, 36, 0.92), rgba(20, 12, 24, 0.95));
        border: 1.5px solid rgba(255, 117, 181, 0.35);
        border-radius: 22px;
        padding: 18px 20px;
        text-align: left;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35);
    }

    .cute-metric-card:hover {
        transform: translateY(-5px);
        border-color: #ff69b4;
        box-shadow: 0 12px 26px rgba(255, 46, 136, 0.28);
    }

    .metric-tag {
        font-size: 0.85rem;
        font-weight: 700;
        color: #f9a8d4;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .metric-num {
        font-family: 'Fredoka', sans-serif;
        font-size: 1.75rem;
        font-weight: 700;
        color: #ff66b2;
        text-shadow: 0 0 14px rgba(255, 102, 178, 0.35);
    }

    /* KARTU STATUS QC KUSTOM (PENGGANTI ST.WARNING YANG SILAU) */
    .status-box-ok {
        background: linear-gradient(135deg, rgba(16, 48, 38, 0.9), rgba(24, 18, 32, 0.95));
        border: 2px solid #4ade80;
        border-radius: 20px;
        padding: 18px 20px;
        margin-bottom: 14px;
        box-shadow: 0 6px 20px rgba(74, 222, 128, 0.16);
    }

    .status-box-ng {
        background: linear-gradient(135deg, rgba(64, 15, 38, 0.92), rgba(28, 13, 26, 0.95));
        border: 2px solid #ff4da6;
        border-radius: 20px;
        padding: 18px 20px;
        margin-bottom: 14px;
        box-shadow: 0 6px 20px rgba(255, 77, 166, 0.22);
    }

    /* TABEL RINGKASAN PARAMETER KUSTOM */
    .cute-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background: rgba(26, 16, 30, 0.9);
        border: 1.5px solid rgba(255, 105, 180, 0.35);
        border-radius: 18px;
        overflow: hidden;
        margin-top: 12px;
        font-size: 0.88rem;
    }

    .cute-table th {
        background: rgba(255, 46, 136, 0.22);
        color: #ffc2e2;
        padding: 10px 12px;
        text-align: center;
        font-weight: 700;
        border-bottom: 1px solid rgba(255, 105, 180, 0.3);
    }

    .cute-table td {
        color: #ffffff;
        padding: 10px 12px;
        text-align: center;
        font-weight: 600;
    }

    hr {
        border: none;
        border-top: 1.5px dashed rgba(255, 105, 180, 0.3) !important;
        margin: 1.5rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO BANNER
# =========================================================
st.markdown("""
<div class="hero-cute">
    <div class="hero-badge">✨ Smart Factory AI • Quality Assurance</div>
    <h1>🎀 Quality Control — Injection Molding</h1>
    <p>Sistem Prediksi & Monitoring Mutu Produk Berbasis Machine Learning 💖</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR - INPUT PARAMETER MESIN
# =========================================================
st.sidebar.markdown("## 🎛️ Parameter Proses Mesin")
st.sidebar.caption("Geser slider di bawah untuk simulasi kondisi produksi ✨")

melt_temp = st.sidebar.slider("🔥 Melt Temperature (°C)", 180.0, 280.0, 243.5, 0.5)
mold_temp = st.sidebar.slider("❄️ Mold Temperature (°C)", 20.0, 90.0, 71.0, 0.5)
injection_pressure = st.sidebar.slider("💨 Injection Pressure (bar)", 500.0, 1800.0, 1490.0, 10.0)
holding_pressure = st.sidebar.slider("🛡️ Holding Pressure (bar)", 300.0, 1400.0, 800.0, 10.0)
cooling_time = st.sidebar.slider("🧊 Cooling Time (detik)", 5.0, 45.0, 18.0, 0.5)
cycle_time = st.sidebar.slider("⏱️ Cycle Time (detik)", 15.0, 90.0, 35.0, 0.5)

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
# 4 KARTU METRIK UTAMA (CUSTOM CUTE CARDS)
# =========================================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="cute-metric-card">
        <div class="metric-tag">🔥 Melt Temp</div>
        <div class="metric-num">{melt_temp:.1f} °C</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="cute-metric-card">
        <div class="metric-tag">❄️ Mold Temp</div>
        <div class="metric-num">{mold_temp:.1f} °C</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="cute-metric-card">
        <div class="metric-tag">💨 Injection Pressure</div>
        <div class="metric-num">{injection_pressure:.1f} bar</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="cute-metric-card">
        <div class="metric-tag">⏱️ Cycle Time</div>
        <div class="metric-num">{cycle_time:.1f} dtk</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================================================
# EVALUASI MUTU & VISUALISASI GRAFIK
# =========================================================
left_col, right_col = st.columns([1.05, 1.25], gap="large")

with left_col:
    st.subheader("💖 Hasil Evaluasi Mutu")

    if model is not None:
        pred = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0] if hasattr(model, "predict_proba") else None
        is_good = (pred == 1) or (str(pred).upper() in ["OK", "PASS", "GOOD"])
        conf_text = f"<br><span style='font-size:0.9rem; color:#fbcfe8;'>Tingkat Keyakinan Model: <b>{np.max(proba)*100:.2f}%</b> ✨</span>" if proba is not None else ""

        if is_good:
            st.markdown(f"""
            <div class="status-box-ok">
                <div style="font-size:1.15rem; font-weight:700; color:#86efac;">✅ Status Produk: LOLOS QC ({pred}) 🌸</div>
                <div style="font-size:0.9rem; color:#dcfce7; margin-top:4px;">Parameter mesin berada dalam kondisi optimal!{conf_text}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="status-box-ng">
                <div style="font-size:1.15rem; font-weight:700; color:#ff85c0;">⚠️ Status Produk: POTENSI DEFECT / NG ({pred}) 💔</div>
                <div style="font-size:0.9rem; color:#ffe4f2; margin-top:4px;">Periksa kembali suhu leleh atau tekanan injeksi.{conf_text}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        is_ok = (205 <= melt_temp <= 245) and (900 <= injection_pressure <= 1350) and (cooling_time >= 12)
        if is_ok:
            st.markdown("""
            <div class="status-box-ok">
                <div style="font-size:1.15rem; font-weight:700; color:#86efac;">✅ Status Produk: LOLOS QC (OK) 🌸</div>
                <div style="font-size:0.88rem; color:#dcfce7; margin-top:4px;">Mode Simulasi • Semua parameter berada di rentang aman ✨</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-box-ng">
                <div style="font-size:1.15rem; font-weight:700; color:#ff85c0;">🎀 Status Produk: RISIKO DEFECT (NG)</div>
                <div style="font-size:0.88rem; color:#ffe4f2; margin-top:4px;">Mode Simulasi • Suhu atau tekanan melebihi batas ideal 💕</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"<p style='font-size:0.84rem; color:#f9a8d4;'>💡 Catatan: Letakkan file <code>{MODEL_PATH}</code> di folder project untuk prediksi model asli.</p>", unsafe_allow_html=True)

    # Tabel Ringkasan Gelap-Pink (Pengganti dataframe putih)
    st.markdown(f"""
    <table class="cute-table">
        <thead>
            <tr>
                <th>Melt</th>
                <th>Mold</th>
                <th>Inj. Press</th>
                <th>Hold Press</th>
                <th>Cooling</th>
                <th>Cycle</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{melt_temp:.1f}°</td>
                <td>{mold_temp:.1f}°</td>
                <td>{injection_pressure:.0f}</td>
                <td>{holding_pressure:.0f}</td>
                <td>{cooling_time:.1f}s</td>
                <td>{cycle_time:.1f}s</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

with right_col:
    st.subheader("📊 Profil Parameter Saat Ini")

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.patch.set_alpha(0.0)
    ax.set_facecolor((0.11, 0.07, 0.14, 0.78))

    normalized_vals = [
        (melt_temp - 180) / (280 - 180) * 100,
        (mold_temp - 20) / (90 - 20) * 100,
        (injection_pressure - 500) / (1800 - 500) * 100,
        (holding_pressure - 300) / (1400 - 300) * 100,
        (cooling_time - 5) / (45 - 5) * 100,
        (cycle_time - 15) / (90 - 15) * 100,
    ]
    labels = ["Melt Temp", "Mold Temp", "Inj. Press", "Hold Press", "Cooling", "Cycle"]
    cute_pinks = ["#ff4da6", "#ff75b5", "#f43f8e", "#ec4899", "#f9a8d4", "#db2777"]

    bars = ax.barh(labels, normalized_vals, color=cute_pinks, height=0.58, edgecolor="#ffe4f2", linewidth=0.8)
    ax.invert_yaxis()
    ax.set_xlim(0, 114)
    ax.grid(axis="x", linestyle="--", alpha=0.22, color="#ff85c0")
    ax.set_axisbelow(True)

    # Label persentase langsung di ujung batang
    for bar, val in zip(bars, normalized_vals):
        ax.text(
            val + 2.2,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%",
            va="center",
            ha="left",
            color="#ffe4f2",
            fontsize=9.5,
            fontweight="bold"
        )

    ax.set_xlabel("Persentase terhadap Rentang Operasi (%)", color="#fbcfe8", fontsize=9.5, fontweight="bold")
    ax.set_title("Distribusi Relatif Parameter Proses ✨", color="#ffffff", fontsize=11.5, fontweight="bold", pad=12)
    ax.tick_params(colors="#ffe4f2", labelsize=9.5)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax.spines[spine].set_color("#ff69b4")
        ax.spines[spine].set_alpha(0.45)

    plt.tight_layout()
    st.pyplot(fig)
