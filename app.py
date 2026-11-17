import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="QC Injection Molding Dashboard", layout="wide")

st.title("📊 Dashboard Pengendalian Mutu Injection Molding")
st.markdown("Aplikasi prediksi komponen cacat berdasarkan parameter siklus mesin.")

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
    st.subheader("📋 Hasil Analisis & Visualisasi Parameter Mesin")

    # Membuat visualisasi grafik batang interaktif dari input operator mesin
    fig, ax = plt.subplots(figsize=(8, 4))
    kategori = ['Suhu Leleh', 'Suhu Cetakan', 'Tekanan (x10)', 'Kecepatan']
    nilai = [suhu_leleh, suhu_cetakan, tekanan / 10, kecepatan]

    # Menggambar bar plot menggunakan Seaborn
    sns.barplot(x=kategori, y=nilai, palette='Blues_d', ax=ax)
    ax.set_title("Visualisasi Parameter Proses Mesin", fontsize=12, fontweight='bold')
    ax.set_ylabel("Nilai Parameter", fontsize=10)
    ax.set_ylim(0, max(nilai) * 1.2 if max(nilai) > 0 else 100)

    # Menampilkan plot ke dalam aplikasi Streamlit
    st.pyplot(fig)

    st.success("File Streamlit 'app.py' beserta visualisasinya berhasil dimuat dan siap dijalankan!")
