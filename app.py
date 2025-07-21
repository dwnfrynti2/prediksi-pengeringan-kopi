# app.py (VERSI FINAL DENGAN CORS, KALKULASI GRAFIK, DAN DETAIL PENYUSUTAN)

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# Muat model dan kolom yang sudah disimpan
try:
    model = joblib.load('coffee_model.joblib')
    model_columns = joblib.load('model_columns.joblib')
    print("* Model dan kolom berhasil dimuat.")
except FileNotFoundError:
    print("! File model tidak ditemukan. Jalankan 'train_model.py' terlebih dahulu.")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model tidak tersedia.'}), 500

    json_data = request.get_json(force=True)
    print(f"Menerima data untuk prediksi: {json_data}")

    try:
        input_df = pd.DataFrame([json_data])
        input_processed = pd.get_dummies(input_df)
        final_input = input_processed.reindex(columns=model_columns, fill_value=0)

        print(f"Data setelah diproses:\n{final_input.to_string()}")

        prediction = model.predict(final_input)
        
        # --- Hasil prediksi utama ---
        output_jam_total = prediction[0] # Gunakan nilai presisi penuh
        lama_nyala = json_data.get('lama_nyala', 8)

        # Durasi aktual dalam hari untuk semua kalkulasi
        durasi_aktual_dalam_hari = 0
        if lama_nyala > 0:
            durasi_aktual_dalam_hari = output_jam_total / lama_nyala
        
        # Total hari kerja (dibulatkan ke atas) hanya untuk menentukan jumlah label pada grafik
        output_hari_total_label = 0
        if lama_nyala > 0:
            output_hari_total_label = int(np.ceil(output_jam_total / lama_nyala))
        else:
            output_hari_total_label = 1 if output_jam_total > 0 else 0

        # Dekomposisi "hari" dan "jam sisa" untuk teks tampilan
        hari_kerja_penuh = 0
        jam_sisa = 0
        if lama_nyala > 0:
            hari_kerja_penuh = int(np.floor(output_jam_total / lama_nyala))
            jam_sisa = round(output_jam_total % lama_nyala, 1)
        else:
            hari_kerja_penuh = 0
            jam_sisa = output_jam_total

        # --- Kalkulasi data untuk grafik dan detail ---
        massa_kopi_awal = json_data.get('massa', 0)
        massa_kering_target = massa_kopi_awal * 0.5 
        
        penyusutan_total = massa_kopi_awal - massa_kering_target
        penyusutan_harian = 0
        
        # Kalkulasi penyusutan harian yang akurat
        if durasi_aktual_dalam_hari > 0:
            penyusutan_harian = round(penyusutan_total / durasi_aktual_dalam_hari, 2)

        # --- Data untuk Grafik Penyusutan Massa ---
        hari_labels = [f"Hari ke-{i+1}" for i in range(output_hari_total_label)]
        massa_harian = []

        if durasi_aktual_dalam_hari > 0:
            for i in range(output_hari_total_label + 1):
                fraksi_selesai = min(i / durasi_aktual_dalam_hari, 1.0)
                massa = massa_kopi_awal - (penyusutan_total * fraksi_selesai)
                massa_harian.append(round(massa, 2))
            
            if output_hari_total_label > 0 and massa_harian[-1] != round(massa_kering_target, 2):
                 massa_harian[-1] = round(massa_kering_target, 2)

        else: 
            massa_harian.extend([massa_kopi_awal, massa_kering_target])
            hari_labels = ["Mulai", "Selesai"]
        
        # --- Siapkan respons JSON ---
        response = {
            'prediksi_jam_total': round(output_jam_total, 1), # Pembulatan hanya untuk tampilan
            'prediksi_hari_total': output_hari_total_label,
            'prediksi_hari': hari_kerja_penuh,
            'prediksi_jam_sisa': jam_sisa,
            'grafik_labels': hari_labels,
            'grafik_data': massa_harian,
            'estimasi_massa_kering': round(massa_kering_target, 2),
            'estimasi_penyusutan_harian': penyusutan_harian
        }
        print(f"Hasil prediksi (termasuk data detail): {response}")
        return jsonify(response)

    except Exception as e:
        print(f"Terjadi error saat prediksi: {e}")
        return jsonify({'error': f'Terjadi kesalahan internal: {e}'}), 500

if __name__ == '__main__':
    app.run(port=9999, debug=True)
