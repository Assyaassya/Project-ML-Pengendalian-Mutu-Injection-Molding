import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

# Konfigurasi Halaman
st.set_page_config(page_title="QC Injection Molding Dashboard", layout="wide")

st.title("📊 Dashboard Pengendalian Mutu Injection Molding")
st.markdown("Aplikasi prediksi komponen cacat berdasarkan parameter siklus mesin.")

# Memuat model yang sudah dilatih (Artifacts)
@st.cache_resource
def load_model():
    model_path = "artifacts/model.joblib"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

model = load_model()

# Sidebar untuk Input Parameter Mesin
st.sidebar.header("⚙️ Masukkan Parameter Mesin")
mesin = st.sidebar.selectbox("Pilih Mesin", ["IM-01", "IM-02", "IM-03", "IM-04"])
shift = st.sidebar.selectbox("Pilih Shift", ["pagi", "siang", "malam"])
bahan = st.sidebar.selectbox("Jenis Bahan Plastik", ["PP", "ABS", "PC"])
suhu_leleh = st.sidebar.slider("Suhu Leleh (°C)", 200.0, 300.0, 240.0)
suhu_cetakan = st.sidebar.slider("Suhu Cetakan (°C)", 20.0, 100.0, 50.0)
tekanan = st.sidebar.slider("Tekanan Injeksi (bar)", 700.0, 1200.0, 900.0)
kecepatan = st.sidebar.slider("Kecepatan Injeksi (mm/s)", 50.0, 120.0, 80.0)
waktu_dingin = st.sidebar.slider("Waktu Pendinginan (s)", 5.0, 30.0, 15.0)
waktu_siklus = st.sidebar.slider("Waktu Siklus (s)", 20.0, 45.0, 30.0)
kelembaban = st.sidebar.slider("Kelembaban Bahan (%)", 0.01, 0.20, 0.05)

if st.button("🔍 Prediksi Kualitas Komponen"):
    st.subheader("📋 Hasil Analisis & Prediksi Model")
    
    # 1. Menyiapkan Data Input dalam bentuk DataFrame (sesuai kolom pelatihan)
    input_data = pd.DataFrame({
        'mesin': [mesin],
        'shift': [shift],
        'bahan': [bahan],
        'suhu_leleh_C': [suhu_leleh],
        'suhu_cetakan_C': [suhu_cetakan],
        'tekanan_injeksi_bar': [tekanan],
        'kecepatan_injeksi_mm_s': [kecepatan],
        'waktu_pendinginan_s': [waktu_dingin],
        'waktu_siklus_s': [waktu_siklus],
        'kelembaban_bahan_pct': [kelembaban]
    })
    
    # 2. Melakukan Prediksi jika model tersedia
    if model is not None:
        try:
            probabilitas_cacat = model.predict_proba(input_data)[0][1]
            # Threshold optimal dari hasil analisis biaya bisnis kita adalah 0.31
            threshold_optimal = 0.31
            hasil_prediksi = 1 if probabilitas_cacat >= threshold_optimal else 0
            
            # Menampilkan Kotak Hasil
            col1, col2 = st.columns(2)
            with col1:
                if hasil_prediksi == 1:
                    st.error(f"⚠️ **PERINGATAN: KOMPONEN BERPOTENSI CACAT!**")
                    st.markdown("Saran: Segera hentikan mesin, pisahkan komponen, dan periksa suhu leleh serta kelembaban bahan.")
                else:
                    st.success(f"✅ **STATUS: KOMPONEN NORMAL (LOLOS QC)**")
                    st.markdown("Parameter proses dalam kondisi aman.")
            with col2:
                st.metric(label="Probabilitas Cacat", value=f"{probabilitas_cacat * 100:.2f}%")
                st.metric(label="Batas Threshold Bisnis", value=f"{threshold_optimal * 100}%")
                
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses prediksi: {e}")
    else:
        st.warning("⚠️ File model (`artifacts/model.joblib`) tidak ditemukan di repositori GitHub!")

    st.markdown("---")
    
    # 3. Visualisasi Grafik Batang Parameter Mesin
    st.markdown("### 📈 Visualisasi Parameter Proses Mesin")
    fig, ax = plt.subplots(figsize=(8, 4))
    kategori = ['Suhu Leleh', 'Suhu Cetakan', 'Tekanan (x10)', 'Kecepatan']
    nilai = [suhu_leleh, suhu_cetakan, tekanan / 10, kecepatan]

    sns.barplot(x=kategori, y=nilai, palette='Blues_d', ax=ax)
    ax.set_ylabel("Nilai Parameter", fontsize=10)
    ax.set_ylim(0, max(nilai) * 1.2 if max(nilai) > 0 else 100)

    st.pyplot(fig)
