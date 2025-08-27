# api/index.py
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from typing import List
import re

app = FastAPI()

# --------------------------------------------
# Utilities
# --------------------------------------------
ARABIC_DIACRITICS = re.compile(r"[\u064B-\u065F\u0670\u06D6-\u06ED]")

DOT_BELOW = {"ب", "ج", "ي"}   # huruf bertitik bawah
NO_DOT = {"ا", "ح", "د", "ر", "س", "ص", "ط", "ع", "ك", "ل", "م", "ه", "و"}

def strip_diacritics(text: str) -> str:
    return ARABIC_DIACRITICS.sub("", text).strip()

# --------------------------------------------
# Routes
# --------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def home():
    html = """
    <html>
      <head><title>Quiz Hijaiyah – Bab 1</title></head>
      <body style="font-family:sans-serif; line-height:1.6;">
        <h1>Quiz Huruf Hijaiyah – Bab 1 (Level Tinggi)</h1>
        <form method="post" action="/api/index/submit">
          <h3>Bagian A – Tebak Huruf</h3>
          <p>1) Huruf ini mirip خ tapi tanpa titik. Apa itu?</p>
          <label><input type="radio" name="q1" value="ج"> ج</label>
          <label><input type="radio" name="q1" value="ح"> ح</label>
          <label><input type="radio" name="q1" value="خ"> خ</label>

          <p>2) Huruf mirip و tapi ada titik di atas?</p>
          <label><input type="radio" name="q2" value="ر"> ر</label>
          <label><input type="radio" name="q2" value="ز"> ز</label>
          <label><input type="radio" name="q2" value="ذ"> ذ</label>

          <h3>Bagian B – Urutkan Huruf</h3>
          <p>3) Susun urutan yang benar: (ت – ا – ث – ب)</p>
          <input type="text" name="q3" placeholder="contoh: ا ب ت ث">

          <p>4) Urutkan huruf ini: (ض – ص – ط – ظ)</p>
          <input type="text" name="q4" placeholder="contoh: ص ض ط ظ">

          <h3>Bagian C – Pasangan Mirip</h3>
          <p>5) Huruf yang mirip ط tapi ada titik di atas?</p>
          <input type="text" name="q5" placeholder="Jawab huruf">

          <p>6) Pasangkan kelompok mirip: (ب ت ث), (ج ح خ), (د ذ), (س ش)</p>
          <input type="text" name="q6" placeholder="Tuliskan semua pasangan">

          <h3>Bagian D – Tebak Kata</h3>
          <p>7) Gabungkan huruf ini: ب + ا + ب = ?</p>
          <input type="text" name="q7">

          <p>8) Sebutkan huruf penyusun kata قَلَم</p>
          <input type="text" name="q8" placeholder="contoh: ق ل م">

          <h3>Bagian E – Tantangan</h3>
          <p>9) Sebutkan 5 huruf tanpa titik</p>
          <input type="text" name="q9">

          <p>10) Ada berapa huruf dengan titik di bawah? Sebutkan!</p>
          <input type="text" name="q10">

          <br><br>
          <button type="submit">Kumpulkan Jawaban</button>
        </form>
      </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.post("/submit", response_class=HTMLResponse)
async def submit(
    q1: str = Form(""),
    q2: str = Form(""),
    q3: str = Form(""),
    q4: str = Form(""),
    q5: str = Form(""),
    q6: str = Form(""),
    q7: str = Form(""),
    q8: str = Form(""),
    q9: str = Form(""),
    q10: str = Form(""),
):
    score = 0
    total = 10
    detail = {}

    # Q1
    if q1 == "ح":
        score += 1
        detail["q1"] = "Benar"
    else:
        detail["q1"] = "Salah"

    # Q2
    if q2 == "ز":
        score += 1
        detail["q2"] = "Benar"
    else:
        detail["q2"] = "Salah"

    # Q3
    if q3.replace(" ", "") in ["ابتث", "ا ب ت ث".replace(" ", "")]:
        score += 1
        detail["q3"] = "Benar"
    else:
        detail["q3"] = "Salah"

    # Q4
    if q4.replace(" ", "") in ["صضطظ"]:
        score += 1
        detail["q4"] = "Benar"
    else:
        detail["q4"] = "Salah"

    # Q5
    if strip_diacritics(q5) == "ظ":
        score += 1
        detail["q5"] = "Benar"
    else:
        detail["q5"] = "Salah"

    # Q6 (open, asal menyebut semua kelompok)
    if all(k in q6 for k in ["ب", "ت", "ث", "ج", "ح", "خ", "د", "ذ", "س", "ش"]):
        score += 1
        detail["q6"] = "Benar"
    else:
        detail["q6"] = "Salah"

    # Q7
    if strip_diacritics(q7) == "باب":
        score += 1
        detail["q7"] = "Benar"
    else:
        detail["q7"] = "Salah"

    # Q8
    if all(h in q8 for h in ["ق", "ل", "م"]):
        score += 1
        detail["q8"] = "Benar"
    else:
        detail["q8"] = "Salah"

    # Q9 (minimal 5 huruf tanpa titik)
    ans9 = set(q9.replace(" ", ""))
    if len(ans9 & NO_DOT) >= 5:
        score += 1
        detail["q9"] = "Benar"
    else:
        detail["q9"] = "Salah"

    # Q10 (huruf titik bawah)
    ans10 = set(q10.replace(" ", ""))
    if DOT_BELOW.issubset(ans10):
        score += 1
        detail["q10"] = "Benar"
    else:
        detail["q10"] = "Salah"

    html = f"""
    <html>
      <head><title>Hasil Quiz</title></head>
      <body style="font-family:sans-serif; line-height:1.6;">
        <h1>Hasil Quiz Hijaiyah – Bab 1</h1>
        <p>Nilai kamu: {score} / {total}</p>
        <h3>Rincian Jawaban:</h3>
        <ul>
          {''.join(f"<li>{k}: {v}</li>" for k,v in detail.items())}
        </ul>
        <a href="/api/index">Kerjakan lagi</a>
      </body>
    </html>
    """
    return HTMLResponse(content=html)
