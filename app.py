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
