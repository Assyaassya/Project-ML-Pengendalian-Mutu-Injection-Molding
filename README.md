# Pengendalian Mutu Injection Molding · Tim AI (Assya & Ilma) 16

**Kasus:** Pengendalian Mutu Injection Molding · **Aplikasi:** https://project-ml-pengendalian-mutu-injection-molding-ilma-asya.streamlit.app/ · **Video:** https://drive.google.com/file/d/191HlPajl1P98dq7k-voMxrqtmskhiwjV/view?usp=sharing

| Anggota | NIM | Bagian yang dikerjakan |
|---|---|---|
| Assya Nurhasanah | 2401047 | EDA, pembersihan data, feature enginering, antarmuka aplikasi (UI) |
| Ilma Hafizhotul Qolbi | 2405064 | pemodelan, evaluasi, API, dan deployment |


## Masalah dan pengguna

Pengguna utama aplikasi ini adalah tim Quality Control dan operator produksi injection molding. Model membantu mereka mengambil keputusan cepat apakah suatu siklus produksi berisiko menghasilkan produk cacat, sehingga parameter mesin dapat segera diperiksa atau disesuaikan sebelum cacat meluas.

## Data dan pembersihan

| Masalah yang ditemukan | Jumlah baris | Cara menangani |
|---|---|---|
| Baris duplikat | 350 | Dihapus dengan drop_duplicates().reset_index(drop=True) sehingga data akhir menjadi 25000 baris |
| Nilai mustahil (<= 0) pada tekanan_injeksi_bar | 127 | Diubah menjadi np.nan untuk diimputasi pada pipeline prapemrosesan |
| Nilai mustahil (<= 0) pada waktu_siklus_s | 75 | Diubah menjadi np.nan untuk diimputasi pada pipeline prapemrosesan |
| Nilai kosong bawaan pada waktu_pendinginan_s | 257 | Diimputasi menggunakan median pada pipeline prapemrosesan |
| Suhu leleh ekstrem (> 350) pada suhu_leleh_C | 579 | Diubah menjadi np.nan untuk diimputasi pada pipeline prapemrosesan |

## Hasil

| Model | PR-AUC *validation* | PR-AUC *test* |
|---|---|---|
| *Baseline*: Logistic Regression | 0.4767 | 0.5278 |
| XGBoost Classifier | 0.6070 | 0.6723 |

*Threshold* yang dipakai: 0.25, karena pada simulasi biaya titik ambang batas ini menghasilkan total biaya paling rendah akibat biaya produk cacat yang lolos ke pelanggan lebih besar daripada biaya pengecekan atau penolakan berlebih.

## Cara menjalankan

```bash
pip install -r requirements.txt
uvicorn app.api.main:app --reload       # API
streamlit run app/ui/streamlit_app.py   # aplikasi
```

## Struktur repositori

```
notebooks/      notebook dari EDA sampai penyimpanan model
data/           data mentah (dan data bersih jika perlu)
src/features.py fungsi pembuat fitur, dipakai saat pelatihan dan saat prediksi
artifacts/      model.joblib + metadata.json
app/            API (FastAPI) dan antarmuka (Streamlit)
```

## Keterbatasan

Model dilatih pada dataset proses *injection molding* yang bersifat sintetis sehingga belum tentu menangkap seluruh dinamika atau gangguan tak terduga di lini produksi nyata. Prediksi juga menjadi kurang dapat diandalkan ketika parameter input berada jauh di luar rentang data pelatihan atau ketika aplikasi masih berjalan dengan penyesuaian *environment* artefak/simulasi. Selain itu, data produksi aktual dari pabrik serta kalibrasi biaya operasional *real-time* belum tersedia pada tahap ini.

## Daftar periksa sebelum dikumpulkan

- [ ] Repositori bersifat publik dan setiap anggota memiliki *commit*
- [ ] *Notebook* dapat dijalankan ulang dari awal sampai akhir tanpa galat
- [ ] *Baseline* wajib dilaporkan dan dibandingkan
- [ ] Data *test* hanya dibuka satu kali, di akhir
- [ ] `artifacts/metadata.json` berisi versi model, fitur masukan, *threshold*, dan metrik
- [ ] Aplikasi dapat dibuka orang lain melalui tautan, termasuk dari ponsel
- [ ] Aplikasi tidak berhenti mendadak ketika menerima masukan yang tidak wajar
- [ ] Laporan paling banyak 6 halaman dan video paling lama 5 menit
