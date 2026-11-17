import numpy as np
import pandas as pd

def bersihkan_data(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    if 'bahan' in df_clean.columns:
        df_clean['bahan'] = df_clean['bahan'].astype(str).str.upper().str.replace('.', '', regex=False).str.strip()
    if 'suhu_leleh_C' in df_clean.columns:
        df_clean.loc[(df_clean['suhu_leleh_C'] <= 0) | (df_clean['suhu_leleh_C'] > 350), 'suhu_leleh_C'] = np.nan
    if 'tekanan_injeksi_bar' in df_clean.columns:
        df_clean.loc[df_clean['tekanan_injeksi_bar'] <= 0, 'tekanan_injeksi_bar'] = np.nan
    if 'waktu_siklus_s' in df_clean.columns:
        df_clean.loc[df_clean['waktu_siklus_s'] <= 0, 'waktu_siklus_s'] = np.nan
    return df_clean
