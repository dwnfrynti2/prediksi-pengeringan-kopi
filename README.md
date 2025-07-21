==============================
Aplikasi Prediksi Pengeringan Kopi
==============================

📌 Deskripsi:
--------------
Aplikasi ini memprediksi durasi waktu pengeringan kopi (dalam jam dan hari) berdasarkan input suhu, kelembaban, cuaca, massa kopi, dan lama nyala pemanas per hari. Model yang digunakan adalah Random Forest yang telah dilatih sebelumnya dan disimpan dalam file .joblib.

Aplikasi terdiri dari:
- Backend: Flask API (file: app.py)
- Frontend: HTML interaktif (file: index.html) yang menampilkan formulir input, hasil prediksi, dan grafik visualisasi.

==============================
📁 Struktur Folder
==============================

├── app.py                  # Backend Flask
├── index.html              # Frontend UI (bisa digunakan secara statis)
├── coffee_model.joblib     # File model prediksi terlatih
├── model_columns.joblib    # Daftar kolom yang digunakan model
├── requirements.txt        # Daftar dependensi Python
├── README.txt              # Dokumentasi singkat

==============================
▶️ Menjalankan Secara Lokal
==============================

1. Buat virtual environment (opsional):
   python -m venv venv
   source venv/bin/activate  (Linux/macOS)
   venv\Scripts\activate     (Windows)

2. Instal semua dependensi:
   pip install -r requirements.txt

3. Jalankan server Flask:
   python app.py

4. Buka file 'index.html' di browser (klik ganda atau buka dengan Live Server).

5. Pastikan endpoint Flask berjalan di http://127.0.0.1:9999
   dan file 'index.html' melakukan fetch ke URL tersebut.

==============================
🌐 Deployment ke Hosting
==============================


==============================
📌 Catatan Penting
==============================
- Jangan lupa mengganti endpoint `fetch()` di index.html sesuai platform hosting Anda.
- File model `.joblib` harus selalu cocok dengan struktur kolom dari `model_columns.joblib`.
- Frontend sudah mendukung Chart.js dan localStorage untuk menyimpan riwayat prediksi.

==============================
🧑‍💻 Pengembang:
Duwi Nofriyanti – Tugas Akhir 2025
Fokus: Prediksi Waktu Pengeringan Kopi dengan ML
Jurusan: Teknik Elektro – Telekomunikasi

Untuk pertanyaan teknis atau perbaikan silakan hubungi pengembang melalui repositori atau email.
