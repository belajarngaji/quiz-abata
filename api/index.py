from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import re

app = FastAPI()

# --------------------------------------------
# Utilities
# --------------------------------------------
# Semua logika kuis dihapus dari sini.

# --------------------------------------------
# Routes
# --------------------------------------------

# Endpoint ini akan menampilkan halaman sederhana untuk menguji koneksi.
# Halaman kuis utama Anda sekarang ada di GitHub Pages.
@app.get("/api/index", response_class=HTMLResponse)
async def home():
    html = """
    <html>
      <head>
        <title>API Kuis Vercel</title>
      </head>
      <body>
        <h1>API Kuis Berjalan</h1>
        <p>API ini siap menerima data dari formulir kuis Anda.</p>
        <p>Kuis lengkap sekarang berjalan di GitHub Pages.</p>
      </body>
    </html>
    """
    return HTMLResponse(content=html)

# Endpoint ini akan menerima nama dan skor dari HTML.
# Anda perlu menambahkan kode untuk menyimpan data ke database di sini.
@app.
post("/api/index/submit", response_class=HTMLResponse)
async def submit(
    nama_murid: str = Form(""),
    skor: str = Form("")
):
    # Logika kuis dihapus. Sekarang hanya menerima data.

    # ------------------------------------------
    # TODO: Tambahkan kode untuk menyimpan data ke database di sini.
    # Contoh:
    # database.collection("hasil_quiz").add({
    #     "nama": nama_murid,
    #     "skor": skor,
    #     "tanggal": datetime.now()
    # })
    # ------------------------------------------

    html = f"""
    <html>
      <head><title>Hasil Quiz</title></head>
      <body style="font-family:sans-serif; line-height:1.6;">
        <h1>Data Diterima!</h1>
        <p>Nama Murid: {nama_murid}</p>
        <p>Skor: {skor}</p>
        <h3>Data ini sudah siap untuk disimpan ke database.</h3>
        <a href="/">Kembali</a>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
    
