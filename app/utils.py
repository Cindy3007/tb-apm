import pandas as pd
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- BAGIAN 1: PERSIAPAN MODEL (HANYA DIJALANKAN SEKALI SAAT APLIKASI START) ---

def preprocess_text(text):
    """Fungsi untuk membersihkan teks."""
    if pd.isna(text) or not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Variabel global untuk menyimpan model yang sudah dilatih
df = None
tfidf_matrix = None
vectorizer = None

try:
    # 1. Load dataset (asumsikan nama file CSV Anda adalah all.csv)
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'all.csv')
    df_temp = pd.read_csv(csv_path, delimiter='|')

    # 2. Gabungkan kolom-kolom penting menjadi satu fitur teks
    # Pastikan nama kolom ini ada di file CSV Anda
    feature_columns = ['job_title', 'career_level', 'experience_level', 'education_level', 
                         'employment_type', 'job_function', 'job_description']
    
    df_temp['combined_features'] = df_temp[feature_columns].astype(str).agg(' '.join, axis=1)

    # 3. Preprocessing teks pada fitur gabungan
    df_temp['combined_features'] = df_temp['combined_features'].apply(preprocess_text)

    # 4. Buat dan latih TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df_temp['combined_features'])
    
    # Simpan DataFrame yang sudah diproses ke variabel global
    df = df_temp
    print("✅ Model dan data berhasil dimuat dan dilatih sekali.")

except Exception as e:
    print(f"❌ ERROR saat memuat model: {e}")
    print("Pastikan file 'all.csv' ada di 'app/data/' dan memiliki kolom yang diperlukan.")


# --- BAGIAN 2: FUNGSI REKOMENDASI (DIJALANKAN SETIAP KALI ADA REQUEST) ---

def get_recommendations(form_data_dict):
    """
    Fungsi ini menggunakan model yang sudah dilatih untuk memberikan rekomendasi.
    """
    if df is None or vectorizer is None:
        print("Model tidak siap. Rekomendasi tidak dapat diberikan.")
        return []

    # Gabungkan input dari form pengguna menjadi satu string profil
    user_profile = ' '.join(str(v) for v in form_data_dict.values() if v)

    # Preprocessing input pengguna
    user_profile_processed = preprocess_text(user_profile)

    # Transform input pengguna menggunakan vectorizer yang sudah ada (jangan di-fit lagi)
    user_input_vector = vectorizer.transform([user_profile_processed])

    # Hitung cosine similarity
    cosine_similarities = cosine_similarity(user_input_vector, tfidf_matrix)[0]

    # Dapatkan 5 indeks teratas
    top_indices = cosine_similarities.argsort()[-5:][::-1]

    # Ambil hasil dari DataFrame dan tambahkan skor kecocokan
    results_df = df.iloc[top_indices].copy()
    
    # --- PERBAIKAN DI SINI ---
    # Kita menetapkan skor langsung ke DataFrame 'results_df'.
    # Ini akan memastikan skor kecocokan ditempatkan pada baris yang benar
    # tanpa terpengaruh oleh indeks yang tidak sejajar.
    results_df['match'] = [f"{(score * 100):.2f}%" for score in cosine_similarities[top_indices]]
    # -------------------------
    
    # Ubah nama kolom agar sesuai dengan yang diharapkan frontend
    results_df = results_df.rename(columns={
        'job_title': 'title',
        'company_industry': 'company',
        'job_description': 'description'
    })
    
    # Pilih hanya kolom yang dibutuhkan dan ubah ke format list of dictionaries
    output_columns = ['title', 'company', 'match', 'description']
    final_columns = [col for col in output_columns if col in results_df.columns]
    
    final_results_df = results_df[final_columns]
    
    # Ganti nilai NaN dengan string kosong sebelum konversi
    final_results_df = final_results_df.fillna('')

    return final_results_df.to_dict('records')
