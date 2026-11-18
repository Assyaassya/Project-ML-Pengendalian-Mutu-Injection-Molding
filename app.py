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
        border: 1.5px solid rgba(255, 133, 192, 0
