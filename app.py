import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="QC Injection Molding • MiAO Edition",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS - TEMA TUMBLER MiAO (PASTEL MULTI-TONE)
# =========================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    h1, h2, h3, .miao-font {
        font-family: 'Fredoka', sans-serif !important;
        letter-spacing: 0.3px;
    }

    /* BACKGROUND UTAMA: Buttercream Yellow + taburan bintang */
    .stApp,
    [data-testid="stAppViewContainer"] {
        background-color: #FAF0BE !important;
        background-image:
            radial-gradient(circle at 12% 14%, rgba(232, 111, 114, 0.14) 0%, transparent 28%),
            radial-gradient(circle at 88% 85%, rgba(155, 182, 204, 0.22) 0%, transparent 32%),
            radial-gradient(#E86F72 1.5px, transparent 1.5px),
            radial-gradient(#F4CE46 2px, #FAF0BE 2px) !important;
        background-size: 100% 100%, 100% 100%, 48px 48px, 48px 48px !important;
        background-position: 0 0, 0 0, 0 0, 24px 24px !important;
        color: #231F20 !important;
    }

    [data-testid="stMain"],
    .main,
    .main .block-container {
        background: transparent !important;
    }

    h1, h2, h3, h4, p, span, label, [data-testid="stMarkdownContainer"] {
        color: #231F20 !important;
    }

    code {
        background-color: #FDE2DC !important;
        color: #C94A4E !important;
        border: 1.5px solid #E86F72;
        border-radius: 8px;
        padding: 2px 7px;
        font-weight: 700;
    }

    [data-testid="stHeader"] {
        background: rgba(250, 240, 190, 0.75) !important;
        backdrop-filter: blur(8px);
    }

    /* =====================================================
       SIDEBAR BARU: GRADASI PEACH - CREAM - PASTEL BLUE
       ===================================================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FDE6DC 0%, #FAF0BE 52%, #DCE9F5 100%) !important;
        border-right: 3px solid #231F20;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.2rem;
    }

    /* Kartu Header Sidebar ala Tutup Tumbler Coral + Peach */
    .sidebar-header-card {
        background: linear-gradient(135deg, #E86F72 0%, #EE8385 100%);
        border: 2.5px solid #231F20;
        border-radius: 20px;
        padding: 16px 18px;
        margin-bottom: 14px;
        box-shadow: 4px 4px 0px #231F20;
        position: relative;
    }

    .sidebar-clasp {
        display: inline-block;
        background: #FCD5C8;
        color: #231F20 !important;
        border: 2px solid #231F20;
        border-radius: 999px;
        padding: 2px 10px;
        font-size: 0.72rem;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .sidebar-header-card h2 {
        margin: 0 0 4px 0;
        font-size: 1.32rem !important;
        color: #FFFDF7 !important;
        text-shadow: 1.5px 1.5px 0px #231F20;
    }

    .sidebar-header-card p {
        margin: 0;
        font-size: 0.82rem !important;
        color: #FFF6E9 !important;
        font-weight: 700;
        line-height: 1.35;
    }

    /* Membungkus setiap Slider Sidebar menjadi Kartu Stiker Lucu */
    [data-testid="stSidebar"] [data-testid="stSlider"] {
        background: #FFFDF7;
        border: 2px solid #231F20;
        border-radius: 16px;
        padding: 12px 14px 10px 14px;
        margin-bottom: 4px;
        box-shadow: 3.5px 3.5px 0px #9BB6CC;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }

    [data-testid="stSidebar"] [data-testid="stSlider"]:hover {
        transform: translate(-1px, -2px);
        box-shadow: 4.5px 5px 0px #E86F72;
    }

    [data-testid="stSidebar"] [data-testid="stSlider"] label p {
        color: #231F20 !important;
        font-weight: 800 !important;
        font-size: 0.88rem !important;
    }

    /* Badge angka nilai slider */
    [data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
        background: #FCD5C8 !important;
        color: #231F20 !important;
        border: 1.5px solid #231F20 !important;
        border-radius: 8px !important;
        padding: 1px 7px !important;
        font-weight: 800 !important;
        font-size: 0.8rem !important;
    }

    /* Track & Thumb Slider (Kuning Headphone + Gradasi Coral-Biru) */
    [data-testid="stSidebar"] [data-baseweb="slider"] > div > div {
        background-color: #FCD5C8 !important;
        height: 6px !important;
        border-radius: 999px !important;
    }

    [data-testid="stSidebar"] [data-baseweb="slider"] > div > div > div:first-child {
        background: linear-gradient(90deg, #7FA3C2 0%, #E86F72 100%) !important;
        height: 6px !important;
        border-radius: 999px !important;
    }

    [data-testid="stSidebar"] [data-baseweb="slider"] div[role="slider"] {
        background-color: #F7D44C !important;
        border: 2.5px solid #231F20 !important;
        width: 18px !important;
        height: 18px !important;
        box-shadow: 0 2px 0 #231F20 !important;
    }

    /* =====================================================
       KONTAINER UTAMA & HERO BANNER
       ===================================================== */
    .main .block-container {
        max-width: 1400px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    [data-testid="stMainBlockContainer"] {
        background: rgba(255, 253, 245, 0.92) !important;
        border: 3px solid #231F20;
        border-radius: 28px;
        box-shadow: 6px 6px 0px #9BB6CC;
    }

    .miao-hero {
        background: linear-gradient(125deg, #E86F72 0%, #EE8385 100%);
        border: 3px solid #231F20;
        border-radius: 24px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 5px 5px 0px #231F20;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
    }

    .miao-badge {
        display: inline-block;
        background: #FCD5C8;
        color: #231F20 !important;
        border: 2px solid #231F20;
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .miao-hero h1 {
        margin: 0 0 6px 0;
        font-size: 2rem;
        font-weight: 700;
        color: #FFFDF7 !important;
        text-shadow: 2px 2px 0px #231F20;
    }

    .miao-hero p {
        margin: 0;
        font-size: 1rem;
        color: #FFF6E9 !important;
        font-weight: 700;
    }

    /* KARTU METRIK GAYA STIKER RETRO */
    .sticker-card {
        background: #FFF9DF;
        border: 2.5px solid #231F20;
        border-radius: 20px;
        padding: 16px 20px;
        box-shadow: 4px 4px 0px #E86F72;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .sticker-card:hover {
        transform: translate(-2px, -3px);
        box-shadow: 6px 7px 0px #231F20;
    }

    .sticker-label {
        font-size: 0.86rem;
        font-weight: 800;
        color: #C94A4E;
        margin-bottom: 4px;
    }

    .sticker-value {
        font-family: 'Fredoka', sans-serif;
        font-size: 1.75rem;
        font-weight: 700;
        color: #231F20;
    }

    /* KOTAK STATUS EVALUASI MUTU */
    .miao-status-ok {
        background: #E6F8EC;
        border: 2.5px solid #231F20;
        border-radius: 20px;
        padding: 18px 20px;
        box-shadow: 4px 4px 0px #4CAF7D;
        margin-bottom: 14px;
    }

    .miao-status-ng {
        background: #FDE4E4;
        border: 2.5px solid #231F20;
        border-radius: 20px;
        padding: 18px 20px;
        box-shadow: 4px 4px 0px #E86F72;
        margin-bottom: 14px;
    }

    /* TABEL RINGKASAN RETRO */
    .miao-table {
        width: 100%;
        border-collapse: collapse;
        background: #FFFDF7;
        border: 2.5px solid #231F20;
        border-radius: 16px;
        overflow: hidden;
        margin-top: 12px;
        font-size: 0.88rem;
        box-shadow: 4px 4px 0px #F7D44C;
    }

    .miao-table th {
        background: #FCD5C8;
        color: #231F20;
        padding: 10px 8px;
        text-align: center;
        font-weight: 800;
        border-bottom: 2px solid #231F20;
    }

    .miao-table td {
        color: #231F20;
        padding: 10px 8px;
        text-align: center;
        font-weight: 700;
    }

    hr {
        border: none;
        border-top: 2px dashed #E86F72 !important;
        margin: 1.4rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO BANNER DENGAN ILUSTRASI STIKER KUCING "MiAO"
# =========================================================
st.markdown("""
<div class="miao-hero">
    <div>
        <div class="miao-badge">★ Smart Factory QC • MiAO Edition ★</div>
        <h1>Quality Control — Injection Molding</h1>
        <p>Sistem Prediksi & Monitoring Mutu Produk Berbasis Machine Learning</p>
    </div>
    <div style="display:flex; align-items:center; gap:14px; flex-shrink:0;">
        <!-- Stiker Kucing Abu-Biru dengan Headphone Kuning -->
        <svg width="78" height="78" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <rect x="6" y="28" width="14" height="34" rx="7" fill="#F7D44C" stroke="#231F20" stroke-width="3"/>
            <rect x="80" y="28" width="14" height="34" rx="7" fill="#F7D44C" stroke="#231F20" stroke-width="3"/>
            <path d="M22 38 Q50 8 78 38" fill="none" stroke="#F7D44C" stroke-width="7" stroke-linecap="round"/>
            <polygon points="24,36 30,14 45,28" fill="#9BB6CC" stroke="#231F20" stroke-width="2.5"/>
            <polygon points="76,36 70,14 55,28" fill="#9BB6CC" stroke="#231F20" stroke-width="2.5"/>
            <ellipse cx="50" cy="54" rx="32" ry="27" fill="#9BB6CC" stroke="#231F20" stroke-width="2.5"/>
            <ellipse cx="50" cy="61" rx="14" ry="10" fill="#FFF8E7"/>
            <circle cx="42" cy="50" r="5.5" fill="#FFFDF7" stroke="#231F20" stroke-width="1.5"/>
            <circle cx="58" cy="50" r="5.5" fill="#FFFDF7" stroke="#231F20" stroke-width="1.5"/>
            <circle cx="43" cy="50" r="3.2" fill="#231F20"/>
            <circle cx="57" cy="50" r="3.2" fill="#231F20"/>
            <polygon points="47,57 53,57 50,61" fill="#E86F72"/>
            <path d="M44 65 Q50 61 50 61 Q50 61 56 65" fill="none" stroke="#231F20" stroke-width="2" stroke-linecap="round"/>
            <line x1="22" y1="56" x2="36" y2="58" stroke="#231F20" stroke-width="1.8"/>
            <line x1="22" y1="63" x2="36" y2="62" stroke="#231F20" stroke-width="1.8"/>
            <line x1="78" y1="56" x2="64" y2="58" stroke="#231F20" stroke-width="1.8"/>
            <line x1="78" y1="63" x2="64" y2="62" stroke="#231F20" stroke-width="1.8"/>
        </svg>
        <!-- Stiker Kucing Hitam "MiAO" -->
        <svg width="82" height="88" viewBox="0 0 100 110" xmlns="http://www.w3.org/2000/svg">
            <polygon points="22,36 26,12 44,26" fill="#231F20"/>
            <polygon points="27,31 29,18 39,26" fill="#F5A99B"/>
            <polygon points="78,36 74,12 56,26" fill="#231F20"/>
            <polygon points="73,31 71,18 61,26" fill="#F5A99B"/>
            <ellipse cx="50" cy="50" rx="33" ry="27" fill="#231F20"/>
            <ellipse cx="43" cy="58" rx="9" ry="8" fill="#FFF8E7"/>
            <ellipse cx="57" cy="58" rx="9" ry="8" fill="#FFF8E7"/>
            <ellipse cx="43" cy="45" rx="6" ry="7" fill="#FFFDF7"/>
            <ellipse cx="57" cy="45" rx="6" ry="7" fill="#FFFDF7"/>
            <circle cx="44" cy="46" r="3.5" fill="#231F20"/>
            <circle cx="56" cy="46" r="3.5" fill="#231F20"/>
            <polygon points="47,53 53,53 50,56" fill="#E86F72"/>
            <line x1="16" y1="51" x2="34" y2="54" stroke="#FFFDF7" stroke-width="1.8"/>
            <line x1="16" y1="59" x2="34" y2="58" stroke="#FFFDF7" stroke-width="1.8"/>
            <line x1="84" y1="51" x2="66" y2="54" stroke="#FFFDF7" stroke-width="1.8"/>
            <line x1="84" y1="59" x2="66" y2="58" stroke="#FFFDF7" stroke-width="1.8"/>
            <text x="50" y="99" text-anchor="middle" font-family="Fredoka, sans-serif" font-weight="700" font-size="18" fill="#FFFDF7" stroke="#231F20" stroke-width="1">MiAO</text>
        </svg>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR - HEADER CARD & SLIDER PARAMETER MESIN
# =========================================================
st.sidebar.markdown("""
<div class="sidebar-header-card">
    <div class="sidebar-clasp">🐾 Control Panel</div>
    <h2>🐱 Parameter Mesin</h2>
    <p>Atur parameter produksi untuk mengecek kualitas produk ★</p>
</div>
""", unsafe_allow_html=True)

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
# 4 KARTU METRIK UTAMA
# =========================================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="sticker-card">
        <div class="sticker-label">★ Melt Temp</div>
        <div class="sticker-value">{melt_temp:.1f} °C</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="sticker-card">
        <div class="sticker-label">★ Mold Temp</div>
        <div class="sticker-value">{mold_temp:.1f} °C</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="sticker-card">
        <div class="sticker-label">★ Injection Pressure</div>
        <div class="sticker-value">{injection_pressure:.1f} bar</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="sticker-card">
        <div class="sticker-label">★ Cycle Time</div>
        <div class="sticker-value">{cycle_time:.1f} dtk</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================================================
# EVALUASI MUTU & VISUALISASI GRAFIK
# =========================================================
left_col, right_col = st.columns([1.05, 1.25], gap="large")

with left_col:
    st.subheader("🐾 Hasil Evaluasi Mutu")

    if model is not None:
        pred = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0] if hasattr(model, "predict_proba") else None
        is_good = (pred == 1) or (str(pred).upper() in ["OK", "PASS", "GOOD"])
        conf_text = f"<br><span style='font-size:0.9rem;'>Tingkat Keyakinan Model: <b>{np.max(proba)*100:.2f}%</b></span>" if proba is not None else ""

        if is_good:
            st.markdown(f"""
            <div class="miao-status-ok">
                <div style="font-size:1.15rem; font-weight:800; color:#1B6B42;">✅ Status Produk: LOLOS QC ({pred}) ★</div>
                <div style="font-size:0.9rem; color:#231F20; margin-top:4px;">Parameter mesin berada dalam kondisi optimal!{conf_text}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="miao-status-ng">
                <div style="font-size:1.15rem; font-weight:800; color:#B83338;">⚠️ Status Produk: POTENSI DEFECT / NG ({pred})</div>
                <div style="font-size:0.9rem; color:#231F20; margin-top:4px;">Periksa kembali suhu leleh atau tekanan injeksi.{conf_text}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        is_ok = (205 <= melt_temp <= 245) and (900 <= injection_pressure <= 1350) and (cooling_time >= 12)
        if is_ok:
            st.markdown("""
            <div class="miao-status-ok">
                <div style="font-size:1.15rem; font-weight:800; color:#1B6B42;">✅ Status Produk: LOLOS QC (OK) ★</div>
                <div style="font-size:0.88rem; color:#231F20; margin-top:4px;">Mode Simulasi • Semua parameter berada di rentang aman.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="miao-status-ng">
                <div style="font-size:1.15rem; font-weight:800; color:#B83338;">🐱 Status Produk: RISIKO DEFECT (NG)</div>
                <div style="font-size:0.88rem; color:#231F20; margin-top:4px;">Mode Simulasi • Suhu atau tekanan melebihi batas ideal.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"<p style='font-size:0.84rem;'>Catatan: Letakkan file <code>{MODEL_PATH}</code> di folder project untuk prediksi model asli.</p>", unsafe_allow_html=True)

    # Tabel Ringkasan
    st.markdown(f"""
    <table class="miao-table">
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
    ax.set_facecolor("#FFF9DF")

    normalized_vals = [
        (melt_temp - 180) / (280 - 180) * 100,
        (mold_temp - 20) / (90 - 20) * 100,
        (injection_pressure - 500) / (1800 - 500) * 100,
        (holding_pressure - 300) / (1400 - 300) * 100,
        (cooling_time - 5) / (45 - 5) * 100,
        (cycle_time - 15) / (90 - 15) * 100,
    ]
    labels = ["Melt Temp", "Mold Temp", "Inj. Press", "Hold Press", "Cooling", "Cycle"]
    tumbler_palette = ["#E86F72", "#9BB6CC", "#231F20", "#F7D44C", "#F5A99B", "#D95B60"]

    bars = ax.barh(labels, normalized_vals, color=tumbler_palette, height=0.58, edgecolor="#231F20", linewidth=1.6)
    ax.invert_yaxis()
    ax.set_xlim(0, 115)
    ax.grid(axis="x", linestyle="--", alpha=0.35, color="#E86F72")
    ax.set_axisbelow(True)

    for bar, val in zip(bars, normalized_vals):
        ax.text(
            val + 2.2,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%",
            va="center",
            ha="left",
            color="#231F20",
            fontsize=9.5,
            fontweight="bold"
        )

    ax.set_xlabel("Persentase terhadap Rentang Operasi (%)", color="#231F20", fontsize=9.5, fontweight="bold")
    ax.set_title("Distribusi Relatif Parameter Proses ★", color="#231F20", fontsize=11.5, fontweight="bold", pad=12)
    ax.tick_params(colors="#231F20", labelsize=9.5)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax.spines[spine].set_color("#231F20")
        ax.spines[spine].set_linewidth(1.5)

    plt.tight_layout()
    st.pyplot(fig)
