import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os

# KONFIGURASI HALAMAN & TEMA WARNA
st.set_page_config(
    page_title="QC Injection Molding • Assya & Ilma",
    page_icon="🐱",
    layout="wide"
)

# CSS sederhana untuk tampilan warna pastel (Buttercream & Coral Pink)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&family=Nunito:wght@600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    color: #231F20;
}

h1, h2, h3 {
    font-family: 'Fredoka', sans-serif !important;
    color: #231F20 !important;
}

/* Warna background halaman & sidebar */
.stApp {
    background-color: #FAF0BE;
}

[data-testid="stSidebar"] {
    background-color: #FDE6DC;
    border-right: 2px solid #231F20;
}

/* Banner judul atas */
.banner-utama {
    background-color: #E86F72;
    border: 2.5px solid #231F20;
    border-radius: 20px;
    padding: 20px 25px;
    margin-bottom: 20px;
    box-shadow: 4px 4px 0px #231F20;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
}

.banner-utama h1 {
    color: #FFFDF7 !important;
    margin: 0;
    font-size: 1.9rem;
    text-shadow: 2px 2px 0px #231F20;
}

.banner-utama p {
    color: #FFFDF7 !important;
    margin: 5px 0 0 0;
    font-size: 0.95rem;
}

/* Kartu maskot Assya & Ilma */
.maskot-wrapper {
    display: flex;
    gap: 12px;
}

.kartu-maskot {
    background-color: #FFFDF7;
    border: 2px solid #231F20;
    border-radius: 15px;
    padding: 8px 16px;
    text-align: center;
    box-shadow: 3px 3px 0px #231F20;
}

/* Styling kotak metric bawaan Streamlit */
[data-testid="stMetric"] {
    background-color: #FFFDF7;
    border: 2px solid #231F20;
    border-radius: 15px;
    padding: 12px 15px;
    box-shadow: 3px 3px 0px #E86F72;
}

[data-testid="stMetricLabel"] p {
    color: #C94A4E !important;
    font-weight: 700;
}

[data-testid="stMetricValue"] {
    color: #231F20 !important;
    font-family: 'Fredoka', sans-serif;
}

/* Kotak status QC */
.status-aman {
    background-color: #DCFCE7;
    border: 2px solid #231F20;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 3px 3px 0px #22C55E;
    margin-bottom: 10px;
}

.status-cacat {
    background-color: #FEE2E2;
    border: 2px solid #231F20;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 3px 3px 0px #EF4444;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# HEADER / BANNER APLIKASI
st.markdown("""
<div class="banner-utama">
    <div>
        <h1>Quality Control — Injection Molding</h1>
        <p>Sistem Prediksi & Monitoring Mutu Produk Berbasis Machine Learning</p>
    </div>
    <div class="maskot-wrapper">
        <div class="kartu-maskot" style="background-color: #DCE9F5;">
            <div style="font-size: 1.8rem;">🎧🐱</div>
            <div style="font-weight: 700; font-size: 0.9rem;">Assya</div>
        </div>
        <div class="kartu-maskot" style="background-color: #FCD5C8;">
            <div style="font-size: 1.8rem;">🐈‍⬛🎀</div>
            <div style="font-weight: 700; font-size: 0.9rem;">Ilma</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR INPUT PARAMETER MESIN
st.sidebar.header("⚙️ Parameter Mesin")
st.sidebar.write("Silakan atur parameter produksi di bawah ini:")

mesin = st.sidebar.selectbox("Pilih Mesin", ["IM-01", "IM-02", "IM-03", "IM-04"])
shift = st.sidebar.selectbox("Pilih Shift", ["pagi", "siang", "malam"], index=1)
jenis_bahan = st.sidebar.selectbox("Jenis Bahan Plastik", ["PP", "ABS", "PC"])

st.sidebar.markdown("---")

melt_temp = st.sidebar.slider("Melt Temperature (°C)", 180.0, 280.0, 243.5, 0.5)
mold_temp = st.sidebar.slider("Mold Temperature (°C)", 20.0, 90.0, 71.0, 0.5)
injection_pressure = st.sidebar.slider("Injection Pressure (bar)", 500.0, 1800.0, 1490.0, 10.0)
holding_pressure = st.sidebar.slider("Holding Pressure (bar)", 300.0, 1400.0, 800.0, 10.0)
cooling_time = st.sidebar.slider("Cooling Time (detik)", 5.0, 45.0, 18.0, 0.5)
cycle_time = st.sidebar.slider("Cycle Time (detik)", 15.0, 90.0, 35.0, 0.5)

# Simpan semua input ke DataFrame
input_df = pd.DataFrame({
    "Mesin": [mesin],
    "Shift": [shift],
    "Jenis_Bahan": [jenis_bahan],
    "Melt_Temp": [melt_temp],
    "Mold_Temp": [mold_temp],
    "Injection_Pressure": [injection_pressure],
    "Holding_Pressure": [holding_pressure],
    "Cooling_Time": [cooling_time],
    "Cycle_Time": [cycle_time]
})

# LOAD MODEL & PREDIKSI PROBABILITAS CACAT
MODEL_PATH = "model_qc_injection.joblib"
THRESHOLD_BISNIS = 25.0  # Batas threshold diubah menjadi 25%

@st.cache_resource
def load_model(path):
    if os.path.exists(path):
        return joblib.load(path)
    return None

def hitung_simulasi(m_temp, mo_temp, inj_p, hold_p, cool_t, cyc_t, msn, shf, bhn):
    # Perhitungan simulasi sederhana jika file model .joblib belum tersedia
    skor_risiko = 5.0
    if m_temp < 200 or m_temp > 255:
        skor_risiko += abs(m_temp - 230) * 0.75
    if mo_temp < 30 or mo_temp > 80:
        skor_risiko += abs(mo_temp - 55) * 0.5
    if inj_p < 750 or inj_p > 1620:
        skor_risiko += abs(inj_p - 1200) * 0.045
    if hold_p < 450 or hold_p > 1150:
        skor_risiko += abs(hold_p - 800) * 0.03
    if cool_t < 10:
        skor_risiko += (10 - cool_t) * 4.5
    if cyc_t < 20 or cyc_t > 70:
        skor_risiko += abs(cyc_t - 40) * 0.45
    if shf == "malam":
        skor_risiko += 2.5
    if bhn in ["PC", "ABS"]:
        skor_risiko += 1.5
    if msn == "IM-03":
        skor_risiko += 1.0
    return float(np.clip(skor_risiko, 1.0, 98.5))

model = load_model(MODEL_PATH)

if model is not None:
    try:
        if hasattr(model, "feature_names_in_"):
            data_uji = input_df.reindex(columns=model.feature_names_in_, fill_value=0)
        else:
            data_uji = input_df

        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(data_uji)[0]
            prob_cacat = float(proba[1]) * 100 if len(proba) > 1 else float(proba[0]) * 100
        else:
            pred = model.predict(data_uji)[0]
            prob_cacat = 5.0 if pred in [0, "OK", "NORMAL"] else 65.0
    except Exception:
        prob_cacat = hitung_simulasi(
            melt_temp, mold_temp, injection_pressure, holding_pressure,
            cooling_time, cycle_time, mesin, shift, jenis_bahan
        )
else:
    prob_cacat = hitung_simulasi(
        melt_temp, mold_temp, injection_pressure, holding_pressure,
        cooling_time, cycle_time, mesin, shift, jenis_bahan
    )

lolos_qc = prob_cacat <= THRESHOLD_BISNIS

# TAMPILAN METRIK UTAMA (4 KOLOM)
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡️ Melt Temp", f"{melt_temp:.1f} °C")
col2.metric("❄️ Mold Temp", f"{mold_temp:.1f} °C")
col3.metric("💨 Injection Pressure", f"{injection_pressure:.0f} bar")
col4.metric("⏱️ Cycle Time", f"{cycle_time:.1f} dtk")

st.markdown("---")

# HASIL ANALISIS & GRAFIK PARAMETER
kiri, kanan = st.columns([1.1, 1.2], gap="large")

with kiri:
    st.subheader("📋 Hasil Analisis & Prediksi Model")

    sub_kiri, sub_kanan = st.columns([1.4, 1])

    with sub_kiri:
        if lolos_qc:
            st.markdown("""
            <div class="status-aman">
                <strong style="color: #166534; font-size: 1.05rem;">✅ STATUS: NORMAL (LOLOS QC)</strong>
                <p style="margin: 6px 0 0 0; font-size: 0.9rem;">Parameter proses berada dalam batas aman.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-cacat">
                <strong style="color: #991B1B; font-size: 1.05rem;">⚠️ STATUS: POTENSI CACAT (NG)</strong>
                <p style="margin: 6px 0 0 0; font-size: 0.9rem;">Probabilitas melebihi batas threshold, cek setting mesin!</p>
            </div>
            """, unsafe_allow_html=True)

    with sub_kanan:
        st.metric("Probabilitas Cacat", f"{prob_cacat:.2f}%")
        st.metric("Batas Threshold", f"{THRESHOLD_BISNIS:.1f}%")

    st.write("**Ringkasan Input Parameter:**")
    st.dataframe(input_df, hide_index=True, use_container_width=True)

with kanan:
    st.subheader("📊 Profil Parameter Saat Ini")

    # Hitung persentase tiap parameter terhadap rentang min-max slider
    persen_param = [
        (melt_temp - 180) / (280 - 180) * 100,
        (mold_temp - 20) / (90 - 20) * 100,
        (injection_pressure - 500) / (1800 - 500) * 100,
        (holding_pressure - 300) / (1400 - 300) * 100,
        (cooling_time - 5) / (45 - 5) * 100,
        (cycle_time - 15) / (90 - 15) * 100,
    ]
    nama_param = ["Melt Temp", "Mold Temp", "Inj. Press", "Hold Press", "Cooling", "Cycle"]
    warna_bar = ["#E86F72", "#9BB6CC", "#4A4E69", "#F7D44C", "#F5A99B", "#D95B60"]

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_alpha(0.0)
    ax.set_facecolor("#FFFDF7")

    bars = ax.barh(nama_param, persen_param, color=warna_bar, edgecolor="#231F20", height=0.55)
    ax.bar_label(bars, fmt="%.1f%%", padding=5, fontsize=9, fontweight="bold", color="#231F20")

    ax.invert_yaxis()
    ax.set_xlim(0, 115)
    ax.set_xlabel("Persentase Rentang Operasi (%)", fontweight="bold")
    ax.set_title(f"Profil Parameter • {mesin} ({shift.capitalize()} - {jenis_bahan})", fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)
