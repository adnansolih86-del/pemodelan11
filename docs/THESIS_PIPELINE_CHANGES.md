THESIS: Pipeline changes for thesis
=================================

Tanggal: 2026-05-17
Penulis: Tim Pemodelan

Tujuan
------
Mendokumentasikan perubahan cepat (quick-fixes) untuk memperbaiki bias klasifikasi "Neutral" yang berlebihan pada pipeline stance analysis. Perubahan ini ditujukan untuk keperluan eksperimen dan bab metodologi / hasil di tesis.

Perubahan yang dibuat
--------------------
1. Confidence threshold
   - File: `stance_analysis.py`
   - Perubahan: Default `confidence_threshold` untuk pipeline transformer diturunkan dari `0.70` menjadi `0.45`.
   - Alasan: Ambang konservatif 0.70 menyebabkan banyak prediksi low-confidence otomatis diset ke `Neutral`. Menurunkannya mengurangi false-neutral.

2. Context-aware Improved Analyzer
   - File: `stance_analysis.py`, `improved_stance_analyzer.py`
   - Perubahan: `run_stance_analysis_improved` sekarang menerima `posts_df` (opsional) dan meneruskan konteks post (`post_text`) ke `ImprovedStanceAnalyzer.analyze()` untuk penyesuaian prediksi berdasarkan konteks.
   - Alasan: Banyak komentar bersifat kritik terhadap post (contradiction), sehingga konteks post membantu mendeteksi stance yang sebenarnya.

3. Lexicon & Preprocessing (tidak diubah dalam patch ini — sudah tersedia)
   - File: `indonesian_stance_lexicon.py`, `enhanced_preprocessing.py`, `improved_stance_analyzer.py`
   - Catatan: Lexicon bahasa Indonesia dan preprocessing yang mempertahankan sinyal (ALL CAPS, tanda seru/ganda, repetisi) sudah diimplementasikan dan digunakan oleh analyzer.

Instruksi Reproduksi
--------------------
1. Jalankan analisis menggunakan improved analyzer (direkomendasikan):

```bash
python -c "from stance_analysis import run_stance_analysis; import pandas as pd; posts=pd.read_csv('posts.csv'); comments=pd.read_csv('comments.csv'); df=run_stance_analysis(posts, comments, use_improved=True); df.to_csv('stance_results.csv', index=False)"
```

2. Jika ingin menggunakan transformer (legacy) dengan ambang baru:

```bash
python -c "from stance_analysis import run_stance_analysis; import pandas as pd; posts=pd.read_csv('posts.csv'); comments=pd.read_csv('comments.csv'); df=run_stance_analysis(posts, comments, use_improved=False); df.to_csv('stance_results_transformer.csv', index=False)"
```

Catatan Metodologis untuk Tesis
--------------------------------
- Jelaskan bahwa threshold netral di-tune sebagai bagian dari langkah validasi awal untuk mengurangi bias kelas mayoritas.
- Sertakan table perbandingan metrik (precision/recall/F1) sebelum & sesudah perubahan ini pada subset validasi.
- Simpan snapshot hasil mentah (`stance_results_before.csv` dan `stance_results_after.csv`) untuk bukti eksperimen.

Langkah Selanjutnya (direkomendasikan)
--------------------------------------
- Kumpulkan 500-1000 contoh ground truth (manual) untuk fine-tune model multilingual/Indonesian.
- Pertimbangkan ensemble dengan model multilingual dan layanan LLM (Gemini) untuk kasus sarkasme/ambigu.
- Tambah validasi per-topik (politics vs non-politics) untuk mengukur distribusi prediksi neutral yang lebih baik.

Catatan terakhir
----------------
Perubahan ini dimaksudkan sebagai "quick wins" untuk memperbaiki masalah overfit ke kelas Neutral. Untuk publikasi tesis, lampirkan script verifikasi dan contoh-contoh kesalahan yang diperbaiki sebagai bukti.
