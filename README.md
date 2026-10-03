# Flask Monolith vs Microservices

Project ini merupakan praktik perbandingan arsitektur **Monolith** dan **Microservices** menggunakan Python Flask.

##  Teknologi

* Python
* Flask
* Requests
* REST API
* Git & GitHub

---

#  Struktur Project

```text
belajar/
├── monolith/
│   └── monolith_app.py
│
└── microservices/
    ├── book_service.py
    └── order_service.py
```

---

# 1. MONOLITH

Arsitektur Monolith menjalankan seluruh fungsi aplikasi dalam satu aplikasi Flask.

##  File

```text
monolith/monolith_app.py
```

##  Source Code

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Database bohongan (In-memory)
books = [
    {
        "id": 1,
        "title": "Belajar Flask",
        "stock": 5
    }
]

orders = []

# =========================
# FITUR BUKU
# =========================

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)


# =========================
# FITUR ORDER
# =========================

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    book_id = data.get('book_id')

    for book in books:
        if book['id'] == book_id:

            if book['stock'] > 0:

                # Mengurangi stock
                book['stock'] -= 1

                order = {
                    "id": len(orders) + 1,
                    "book_id": book_id,
                    "status": "berhasil"
                }

                orders.append(order)

                return jsonify(order), 201

            return jsonify({
                "error": "Stock buku habis"
            }), 400

    return jsonify({
        "error": "Buku tidak ditemukan"
    }), 404


# =========================
# MENJALANKAN SERVER
# =========================

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

##  Menjalankan Monolith

Masuk ke folder:

```powershell
cd monolith
```

Install Flask jika belum tersedia:

```powershell
pip install flask
```

Jalankan:

```powershell
python monolith_app.py
```

Server berjalan pada:

```text
http://127.0.0.1:5000
```

##  Test GET Books

```powershell
curl.exe http://127.0.0.1:5000/books
```

Response:

```json
[
    {
        "id": 1,
        "stock": 5,
        "title": "Belajar Flask"
    }
]
```

##  Test POST Order

```powershell
$body = '{"book_id":1}'
```

```powershell
curl.exe -X POST "http://127.0.0.1:5000/orders" -H "Content-Type: application/json" -d $body
```

Response:

```json
{
    "book_id": 1,
    "id": 1,
    "status": "berhasil"
}
```

Setelah order berhasil, stock buku berkurang dari `5` menjadi `4`.

---

# 2. MICROSERVICES

Pada arsitektur Microservices, aplikasi Monolith dipecah menjadi beberapa service.

Project ini menggunakan dua service:

```text
Book Service
Port 5001

Order Service
Port 5002
```

Struktur:

```text
microservices/
│
├── book_service.py
└── order_service.py
```

---

# 2.1 BOOK SERVICE

Book Service bertanggung jawab menyediakan data buku.

##  File

```text
microservices/book_service.py
```

##  Source Code

```python
from flask import Flask, jsonify

app = Flask(__name__)

books = [
    {
        "id": 1,
        "title": "Belajar Flask",
        "stock": 5
    }
]


# =========================
# GET SEMUA BUKU
# =========================

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)


# =========================
# GET BUKU BERDASARKAN ID
# =========================

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):

    for book in books:

        if book['id'] == book_id:
            return jsonify(book)

    return jsonify({
        "error": "Buku tidak ditemukan"
    }), 404


# =========================
# MENJALANKAN SERVER
# =========================

if __name__ == '__main__':
    app.run(port=5001, debug=True)
```

##  Menjalankan Book Service

Masuk ke folder:

```powershell
cd microservices
```

Install Flask:

```powershell
pip install flask
```

Jalankan:

```powershell
python book_service.py
```

Server berjalan pada:

```text
http://127.0.0.1:5001
```

## Test Semua Buku

```powershell
curl.exe http://127.0.0.1:5001/books
```

## Test Satu Buku

```powershell
curl.exe http://127.0.0.1:5001/books/1
```

Response:

```json
{
    "id": 1,
    "stock": 5,
    "title": "Belajar Flask"
}
```

---

# 2.2 ORDER SERVICE

Order Service bertanggung jawab menangani pemesanan.

Order Service mengambil data buku dari Book Service menggunakan HTTP Request.

##  File

```text
microservices/order_service.py
```

##  Source Code

```python
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

orders = []

BOOK_SERVICE_URL = "http://127.0.0.1:5001"


# =========================
# MEMBUAT ORDER
# =========================

@app.route('/orders', methods=['POST'])
def create_order():

    data = request.get_json()
    book_id = data.get('book_id')

    try:

        # Meminta data buku ke Book Service
        response = requests.get(
            f"{BOOK_SERVICE_URL}/books/{book_id}"
        )

        if response.status_code == 200:

            book_data = response.json()

            if book_data['stock'] > 0:

                order = {
                    "id": len(orders) + 1,
                    "book_id": book_id,
                    "status": "berhasil"
                }

                orders.append(order)

                return jsonify(order), 201

        return jsonify({
            "error": "Buku tidak tersedia"
        }), 400

    except requests.exceptions.ConnectionError:

        return jsonify({
            "error": "Book Service sedang down!"
        }), 500


# =========================
# MENJALANKAN SERVER
# =========================

if __name__ == '__main__':
    app.run(port=5002, debug=True)
```

##  Menjalankan Order Service

Buka **terminal baru**.

Masuk ke folder:

```powershell
cd microservices
```

Install Requests:

```powershell
pip install requests
```

Jalankan:

```powershell
python order_service.py
```

Server berjalan pada:

```text
http://127.0.0.1:5002
```

---

#  Test Order Service

Pastikan:

```text
Book Service  → Port 5001 → RUNNING
Order Service → Port 5002 → RUNNING
```

Kemudian:

```powershell
$body = '{"book_id":1}'
```

Jalankan:

```powershell
curl.exe -X POST "http://127.0.0.1:5002/orders" -H "Content-Type: application/json" -d $body
```

Response:

```json
{
    "book_id": 1,
    "id": 1,
    "status": "berhasil"
}
```

---

#  KOMUNIKASI MICROSERVICES

Alur komunikasi:

```text
Client
   │
   │ POST /orders
   ▼
┌──────────────────┐
│  Order Service   │
│     Port 5002    │
└────────┬─────────┘
         │
         │ GET /books/1
         ▼
┌──────────────────┐
│   Book Service   │
│     Port 5001    │
└────────┬─────────┘
         │
         │ Data buku
         ▼
┌──────────────────┐
│  Order Service   │
└────────┬─────────┘
         │
         ▼
       Client
```

Order Service berkomunikasi dengan Book Service menggunakan:

```text
HTTP GET
http://127.0.0.1:5001/books/1
```

---

#  FAULT ISOLATION

Fault Isolation digunakan untuk menguji kondisi ketika Book Service mengalami gangguan.

## 1. Matikan Book Service

Pada terminal Book Service:

```text
Ctrl + C
```

## 2. Pastikan Order Service Tetap Berjalan

Order Service tetap berjalan pada:

```text
http://127.0.0.1:5002
```

## 3. Kirim Order

```powershell
$body = '{"book_id":1}'
```

```powershell
curl.exe -X POST "http://127.0.0.1:5002/orders" -H "Content-Type: application/json" -d $body
```

Response:

```json
{
    "error": "Book Service sedang down!"
}
```

Order Service tetap aktif dan menangani kegagalan koneksi ke Book Service.

---

