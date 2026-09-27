from flask import Flask, jsonify

app = Flask(__name__)

# Database khusus Book Service (In-memory)
books = [
    {
        "id": 1,
        "title": "Belajar Flask",
        "stock": 5
    }
]


# =========================
# FITUR DAFTAR BUKU
# =========================

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)


# =========================
# FITUR DETAIL BUKU
# =========================

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for b in books:
        if b['id'] == book_id:
            return jsonify(b)

    return jsonify({
        "error": "Buku tidak ditemukan"
    }), 404


# =========================
# MENJALANKAN APLIKASI
# =========================

if __name__ == '__main__':
    # Book Service berjalan di port 5001
    app.run(port=5001, debug=True)