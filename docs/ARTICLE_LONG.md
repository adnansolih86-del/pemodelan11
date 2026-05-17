Deteksi Stance pada Komentar Postingan: Pendekatan Leksikon + Sinyal (Versi Publikasi)
======================================================================================

Abstrak
-------
Deteksi stance pada komentar postingan sosial media memainkan peran penting dalam analisis opini dan penelitian kebijakan. Studi ini mengusulkan pipeline deteksi stance berbahasa Indonesia yang menggabungkan leksikon domain-spesifik, preservasi sinyal intensitas, deteksi sarkasme sederhana, dan konteks post-level. Eksperimen awal menunjukkan peningkatan F1 pada kelas non-neutral dibandingkan baseline yang cenderung over-prediksi label Netral.

1. Pendahuluan
--------------
Komentar pada platform sosial media sering berisi opini singkat yang sulit dikategorikan oleh model umum. Di bahasa Indonesia, fenomena slang, idiom, dan retorika informal memperkuat kebutuhan solusi khusus. Sebagai contoh, label "gak becus" jelas menunjukkan kritik, sementara "keren banget" menandai dukungan. Tanpa penyesuaian, model konvensional mudah salah mengklasifikasikan komentar ini sebagai netral.

Stance detection berbeda dari sentiment analysis biasa. Di sini fokus bukan sekadar emosi positif atau negatif, tetapi sikap terhadap suatu topik atau entitas. Komentar yang tampak netral dapat memiliki stance tersirat, terutama ketika menggunakan sarkasme, ironi, atau frasa ambigu. Oleh karena itu, penelitian ini mengeksplorasi kombinasi aturan bahasa dan sinyal tekstual untuk meningkatkan akurasi pada domain Indonesia.

2. Tantangan Bahasa Indonesia
-----------------------------
Bahasa Indonesia di media sosial dipenuhi oleh:
- Slang: "goblog", "tolol", "gak becus".
- Idiom: "kurang makan sekolahan", "bikin hati lega".
- Singkatan/abreviasi: "gk", "bgt", "dgn".
- Pola retoris: "maaf ya ... tapi".

Penggunaan aksara kapital secara berlebihan, beberapa tanda seru, dan elongasi kata juga mengkomunikasikan intensitas. Sistem yang menghapus semua sinyal ini kehilangan informasi penting untuk memutuskan stance.

3. Framework Approached
------------------------
Pipeline yang diusulkan memiliki lima komponen utama:

3.1 Preprocessing sinyal-preserving
------------------------------------
Modul preprocessing tidak hanya membersihkan teks, tetapi juga mengekstrak sinyal intensitas:
- ALL CAPS sebagai indikator penekanan.
- "!!!" atau "???" sebagai tanda emosi kuat.
- Repetisi karakter seperti "gakkk".
- Ekspansi singkatan seperti "gk" → "gak", "bgt" → "banget".

Informasi ini disimpan dalam fitur tambahan dan digunakan untuk menguatkan skor sentiment/stance.

3.2 Leksikon Bahasa Indonesia
-----------------------------
Leksikon terdiri dari kata dan frasa berpolaritas yang relevan dengan domain politik dan opini publik. Contoh kategori:
- Negatif kuat: "goblog", "maling", "tidak independen".
- Positif kuat: "keren banget", "mantap jiwa", "bangga".
- Idiom: "kurang makan sekolah", "bikin hati lega".

Leksikon ini disusun untuk menangkap ekspresi lokal yang sering luput dari model sentiment umum.

3.3 Booster, Reducer, dan Negation
----------------------------------
Skor dasar leksikon dimodifikasi oleh intensifier dan reducer:
- Booster: "banget", "sangat", "sekali".
- Reducer: "agak", "sedikit", "mungkin".

Negasi seperti "tidak" dan "gak" mempengaruhi polaritas lokal: positif yang dinegasi cenderung turun, sedangkan negatif yang dinegasi dapat dilemahkan.

3.4 Deteksi Sarkasme dan Retorika
---------------------------------
Pattern-based detection digunakan untuk kasus berikut:
- "maaf ya ... tapi"
- "mohon dimaklumi"
- "gmana ... bs ...??"
- "ya sudahlah", "terserah"

Jika pola ini terdeteksi bersama kata-kata kritis, sistem condong ke kelas Negative.

3.5 Konteks Post-Level
----------------------
Komentar dianalisis bersama konteks post. Bila sebuah post cenderung positif tetapi komentar mengandung kontradiksi seperti "tapi" atau "namun", sistem memberi bobot tambahan pada interpretasi kritik. Ini penting untuk membedakan komentar yang tampak netral secara leksikal tetapi sebenarnya menentang gagasan postingan.

4. Implementasi Reproducible
-----------------------------
Seluruh pipeline dan eksperimen direproduksi dengan skrip berikut:
- `scripts/run_stance_experiment.py`
- `scripts/generate_report.py`
- `scripts/plot_results.py`
- `scripts/compute_inter_annotator_kappa.py`
- `notebooks/thesis_results_analysis.ipynb`

Dokumentasi perubahan pipeline tersedia di `docs/THESIS_PIPELINE_CHANGES.md`, sedangkan template ground-truth ada di `data/ground_truth_template.csv`.

5. Evaluasi dan Hasil
---------------------
Evaluasi awal menggunakan ground-truth subset 23 komentar menghasilkan:
- Positive — Precision 0.889, Recall 1.000, F1 0.941
- Negative — Precision 1.000, Recall 0.800, F1 0.889
- Neutral — Precision 0.667, Recall 0.800, F1 0.727

Distribusi hasil dan confusion matrix dapat dilihat pada `results/gt_experiment/`.

6. Analisis Kesalahan
---------------------
Kesalahan utama muncul pada:
- Sarkasme kompleks yang memerlukan world knowledge.
- Komentar pendek dengan frasa ambigu.
- Komentar faktual negatif tanpa kata sentiment eksplisit.

Contoh error case tersimpan di `results/gt_experiment/error_examples.csv`, yang ideal untuk analisis manual dalam bab tesis.

7. Diskusi Trade-off
--------------------
Kelebihan pendekatan:
- Explainable via leksikon dan signal reasoning.
- Reproducible tanpa dependensi model besar.
- Cepat dijalankan pada CPU dengan dataset kecil.

Kekurangan:
- Leksikon memerlukan update berkala untuk slang baru.
- Rule-based sarcasm detection terbatas.
- Memerlukan ground-truth besar untuk validasi statistik yang kuat.

Model multilingual atau LLM seperti Gemini dapat meningkatkan hasil, tetapi menimbulkan trade-off biaya, latensi, dan reproducibility.

8. Rekomendasi untuk Tesis
-------------------------
1. Gunakan pipeline improved sebagai baseline.
2. Kumpulkan 500–1000 contoh ground-truth berlabel.
3. Lakukan per-topik evaluation.
4. Bandingkan baseline improved dengan transformer/fine-tuned dan ensemble.
5. Sertakan analisis distribusi label untuk menilai bias Netral.

9. Ground-Truth dan Validasi Labeler
-----------------------------------
Ground-truth harus berisi minimal:
- `post_id`, `post_text`, `comment_id`, `comment_text`
- `label_expected` (Positive/Negative/Neutral)
- `labeler_id`
- `notes`

Protokol label:
- Label minimal 2 annotator per contoh.
- Gunakan adjudication bila terjadi ketidaksepakatan.
- Hitung inter-annotator agreement dengan Cohen's/Fleiss' kappa.

10. Kesimpulan
--------------
Pipeline ini menyediakan baseline practical yang cocok untuk tesis dengan fokus pada bahasa Indonesia. Dengan ground-truth yang lebih besar dan perbandingan model, pendekatan ini siap dikembangkan menjadi kontribusi publikasi.

Lampiran
--------
- Notebook: `notebooks/thesis_results_analysis.ipynb`
- Laporan: `results/gt_experiment/REPORT.md`
- Template labeling: `data/ground_truth_template.csv`
- Panduan: `docs/GROUND_TRUTH_LABELING_GUIDE.md`

