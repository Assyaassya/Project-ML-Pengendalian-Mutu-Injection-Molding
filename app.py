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

    .stApp {
        background: linear-gradient(135deg, #e8f1ff 0%, #f0eaff 38%, #fff0f5 72%, #fff5e8 100%);
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

    .hero {
        background: linear-gradient(115deg, #123b70 0%, #176b87 38%, #6250a4 72%, #9a4f83 100%);
        padding: 30px 34px;
        border-radius: 20px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 14px 34px rgba(58, 75, 150, 0.22);
    }

    .hero h1 {
        color: white;
        font-size: 2.15rem;
        font-weight: 800;
        line-height: 1.2;
        margin: 0 0 8px 0;
    }

    .hero p {
        color: #d7e5f3;
        font-size: 1rem;
        margin: 0;
    }

    .hero-tag {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.13);
        color: #e8f3ff;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 14px;
