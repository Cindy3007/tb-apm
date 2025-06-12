# Pastikan Anda mengimpor semua modul yang dibutuhkan
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
# Pastikan nama fungsinya benar sesuai dengan file utils.py Anda
from app.utils import get_recommendations 

index_bp = Blueprint('index_bp', __name__)

@index_bp.route('/')
def index():
    # Fungsi ini menampilkan halaman input utama, sudah benar.
    return render_template('input.html')

@index_bp.route('/api/recommend', methods=['POST'])
def api_recommend():
    """
    API untuk menangani permintaan dari popup.
    """
    # PERBAIKAN: Ambil semua data dari form sebagai dictionary, bukan hanya 'deskripsi'.
    if not request.form:
        return jsonify({"error": "Form data tidak boleh kosong"}), 400
        
    form_data_dict = request.form.to_dict()
    
    # Panggil fungsi model Anda dengan dictionary data form
    all_recommendations = get_recommendations(form_data_dict)
    
    if not all_recommendations:
        # Kirim error 404 Not Found jika model tidak mengembalikan apa pun
        return jsonify({"error": "Tidak ada rekomendasi yang cocok ditemukan."}), 404
        
    # Simpan semua hasil ke dalam session untuk halaman berikutnya
    session['recommendations'] = all_recommendations
    
    # Kembalikan hanya hasil pertama untuk ditampilkan di popup
    first_recommendation = all_recommendations[0]
    return jsonify(first_recommendation)

@index_bp.route('/rekomendasi')
def show_all_recommendations():
    """
    Halaman untuk menampilkan semua 5 rekomendasi.
    """
    # Ambil hasil dari session yang sudah disimpan
    recommendations_list = session.get('recommendations', [])
    
    if not recommendations_list:
        # Jika tidak ada apa-apa di session, kembali ke halaman utama
        return redirect(url_for('index_bp.index'))
        
    # Tampilkan halaman rekomendasi.html dengan semua data
    # Ganti 'jobs' dengan 'recommendations' jika template Anda menggunakan itu
    return render_template('rekomendasi.html', jobs=recommendations_list)