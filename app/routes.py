# routes.py

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.utils import get_recommendations  # Pastikan fungsi ini ada dan benar

# Membuat Blueprint untuk routing
index_bp = Blueprint('index_bp', __name__)

# 1. Route untuk menampilkan halaman utama (dashboard)
@index_bp.route('/')
def index():
    return render_template('dashboard.html')

# 2. Route untuk halaman form input rekomendasi karir
@index_bp.route('/input')
def input_form():
    return render_template('input.html')

# 3. Route API untuk menangani permintaan rekomendasi dari form
@index_bp.route('/api/recommend', methods=['POST'])
def api_recommend():
    if not request.form:
        return jsonify({"error": "Form data tidak boleh kosong"}), 400

    form_data_dict = request.form.to_dict()

    # Panggil fungsi rekomendasi dari model
    all_recommendations = get_recommendations(form_data_dict)

    if not all_recommendations:
        return jsonify({"error": "Tidak ada rekomendasi yang cocok ditemukan."}), 404

    # Simpan seluruh rekomendasi ke session untuk ditampilkan nanti
    session['recommendations'] = all_recommendations

    # Kembalikan satu hasil pertama untuk popup preview (misalnya)
    return jsonify(all_recommendations[0])

# 4. Route untuk menampilkan semua hasil rekomendasi di halaman baru
@index_bp.route('/rekomendasi')
def show_all_recommendations():
    recommendations_list = session.get('recommendations', [])

    if not recommendations_list:
        return redirect(url_for('index_bp.index'))

    return render_template('rekomendasi.html', jobs=recommendations_list)
