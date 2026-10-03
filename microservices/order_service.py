from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Database pesanan (In-memory)
orders = []

# Alamat Book Service
BOOK_SERVICE_URL = "http://localhost:5001"


# =========================
# FITUR MEMBUAT PESANAN
# =========================

@app.route('/orders', methods=['POST'])
def create_order():

    data = request.get_json()

    book_id = data.get('book_id')

    # Komunikasi antar service melalui HTTP Request
    try:

        response = requests.get(
            f"{BOOK_SERVICE_URL}/books/{book_id}",
            timeout=5
        )

        # Jika buku ditemukan
        if response.status_code == 200:

            book_data = response.json()

            # Cek stok buku
            if book_data['stock'] > 0:

                order = {
                    "id": len(orders) + 1,
                    "book_id": book_id,
                    "status": "berhasil"
                }

                orders.append(order)

                return jsonify(order), 201

        # Jika buku tidak tersedia
        return jsonify({
            "error": "Buku tidak tersedia"
        }), 400

    except requests.exceptions.ConnectionError:

        return jsonify({
            "error": "Book Service sedang down!"
        }), 500


# =========================
# MENJALANKAN APLIKASI
# =========================

if __name__ == '__main__':
    # Order Service berjalan di port 5002
    app.run(port=5002, debug=True)