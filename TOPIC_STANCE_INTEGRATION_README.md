# Topic-Based Granular Stance Analysis Integration

## Overview

Sistem analisis stance yang terintegrasi dengan hasil topic modeling untuk menampilkan hierarki lengkap: **Topic → Posts → Comments → Stance Analysis**.

## Fitur Utama

### 1. Integrasi Data
- **Topic Modeling Results**: Menggabungkan hasil topic modeling dengan analisis stance
- **Hierarchical Structure**: Struktur data yang menghubungkan topik, postingan, dan komentar
- **Automatic Mapping**: Pemetaan otomatis berdasarkan conversation_id_str

### 2. Dashboard Interaktif
- **Topic Explorer**: Navigasi berdasarkan topik dengan accordion
- **Multi-level Filtering**: Filter berdasarkan topik, stance, dan confidence
- **Color-coded Display**: Visualisasi stance dengan color-coding
- **Statistics Summary**: Ringkasan statistik per topik dan postingan

### 3. Data Sources
- **Topic Modeling Results**: Data dari folder `results/` (posts_with_topics_*.csv, comments_with_stance_*.csv)
- **Sample Data**: Data contoh untuk testing
- **Upload CSV**: Upload data custom

## Struktur Data

### Input Files
```
results/
├── posts_with_topics_20260505_061312.csv    # Posts dengan kolom Topik
├── comments_with_stance_20260505_061312.csv # Comments dengan stance analysis
└── original_data_20260505_061312.csv        # Data asli dengan conversation_id
```

### Output Structure
```
Topic 1: [Topic Name]
├── Post 1: [Post Text]
│   ├── Comment 1: [Comment Text] → 🟩 Mendukung (0.85)
│   ├── Comment 2: [Comment Text] → 🟥 Menolak (0.72)
│   └── Comment 3: [Comment Text] → ⬜ Netral (0.60)
└── Post 2: [Post Text]
    └── ...
```

## Cara Penggunaan

### 1. Jalankan Dashboard
```bash
python demo_topic_stance_dashboard.py
```

### 2. Pilih Data Source
- Pilih **"Topic Modeling Results"** di sidebar
- Pilih periode analisis yang tersedia
- Dashboard akan otomatis memuat dan mengintegrasikan data

### 3. Eksplorasi Data
- **Topic Level**: Klik expander untuk melihat postingan dalam topik
- **Post Level**: Klik expander untuk melihat komentar dan analisis stance
- **Filter**: Gunakan filter sidebar untuk menyaring berdasarkan stance, confidence, atau topik

### 4. Visualisasi
- **Color Coding**: 🟩 Hijau = Mendukung, 🟥 Merah = Menolak, ⬜ Abu = Netral
- **Statistics**: Metrik persentase dan rata-rata confidence per topik/postingan
- **Charts**: Distribusi stance dan confidence histograms

## File Komponen

### Core Modules
- `topic_stance_integration.py`: Modul integrasi utama
- `streamlit_granular_stance.py`: Dashboard dengan fitur topic-based
- `demo_topic_stance_dashboard.py`: Script demo dan launcher

### Helper Functions
- `load_topic_stance_data()`: Memuat dan menggabungkan data topic + stance
- `get_topic_summary()`: Menghasilkan statistik per topik
- `render_post_with_comments()`: Render hierarki post → comments

## Requirements

### Dependencies
```
pandas>=1.5.0
streamlit>=1.28.0
plotly>=5.15.0
google-generativeai>=0.3.0
```

### Data Requirements
- Hasil topic modeling di folder `results/`
- File stance analysis yang sesuai
- Format CSV dengan kolom yang benar

## Troubleshooting

### Error: "Topic modeling results not found"
- Pastikan folder `results/` ada dan berisi file yang diperlukan
- Jalankan topic modeling terlebih dahulu jika belum ada

### Error: "No stance analysis results"
- Pastikan ada file `comments_with_stance_*.csv` di `results/`
- Jalankan stance analysis granular jika belum ada

### Performance Issues
- Untuk dataset besar, gunakan filter untuk mengurangi data yang ditampilkan
- Aktifkan "Print-friendly mode" untuk tampilan vertikal

## Contoh Output

```
📂 Topik 1: Politik Luar Negeri (45 posts, 128 comments)
├── 📌 Post: "Kebijakan luar negeri Indonesia..."
│   ├── 🟩 Mendukung: 65% | 🟥 Menolak: 25% | ⬜ Netral: 10%
│   ├── ↳ Komentar 1: "Setuju dengan kebijakan ini..." 🟩 Mendukung (0.88)
│   └── ↳ Komentar 2: "Kurang tepat sasaran..." 🟥 Menolak (0.76)
└── 📌 Post: "Hubungan dengan negara tetangga..."
    └── ...
```

## Next Steps

1. **Advanced Filtering**: Tambahkan filter berdasarkan tanggal dan keyword
2. **Export Features**: Export hasil per topik dalam format PDF/Excel
3. **Trend Analysis**: Analisis perubahan stance seiring waktu
4. **Interactive Charts**: Drill-down charts untuk eksplorasi mendalam