from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import re

app = FastAPI()

# --------------------------------------------
# Utilities
# --------------------------------------------
ARABIC_DIACRITICS = re.compile(r"[\u064B-\u065F\u0670\u06D6-\u06ED]")

DOT_BELOW = {"ب", "ج", "ي"}
NO_DOT = {"ا", "ح", "د", "ر", "س", "ص", "ط", "ع", "ك", "ل", "م", "ه", "و"}

def strip_diacritics(text: str) -> str:
    return ARABIC_DIACRITICS.sub("", text).strip()

# --------------------------------------------
# Routes
# --------------------------------------------
@app.get("/api/index", response_class=HTMLResponse)
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

          <h3>Bagian B – Urutkan Huruf</h3>
          <p>3) Susun urutan yang benar: (ت – ا – ث – ب)</p>
          <input type="text" name="q3" placeholder="contoh: ا ب ت ث">

          <h3>Bagian E – Tantangan</h3>
          <p>9) Sebutkan 5 huruf tanpa titik</p>
          <input type="text" name="q9">

          <br><br>
          <button type="submit">Kumpulkan Jawaban</button>
        </form>
      </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.post("/api/index/submit", response_class=HTMLResponse)
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
    if q3.replace(" ", "") in ["ابتث"]:
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

    # Q6
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
    if all(h in q8 for h in ["ق", "ل", "m"]):
        score += 1
        detail["q8"] = "Benar"
    else:
        detail["q8"] = "Salah"

    # Q9
    ans9 = set(q9.replace(" ", ""))
    if len(ans9 & NO_DOT) >= 5:
        score += 1
        detail["q9"] = "Benar"
    else:
        detail["q9"] = "Salah"

    # Q10
    ans10 = set(q10.replace(" ", ""))
    if DOT_BELOW.issubset(ans10):
        score += 1
        detail["q10"] = "Benar"
    else:
        detail["q10"] = "Salah"

    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hasil Quiz</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --primary-blue: #007bff;
                --soft-blue: #e8f5ff;
                --dark-text: #333;
                --light-text: #666;
                --border-color: #ddd;
                --bg-color: #f8f9fa;
                --card-bg: #fff;
            }}

            body {{
                font-family: 'Roboto', sans-serif;
                line-height: 1.6;
                background-color: var(--bg-color);
                color: var(--dark-text);
                padding: 2rem;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}

            .container {{
                max-width: 900px;
                width: 100%;
                background-color: var(--card-bg);
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                padding: 2.5rem;
                text-align: center;
            }}

            h1 {{
                color: var(--primary-blue);
                font-weight: 700;
                margin-bottom: 2rem;
            }}

            .score {{
                font-size: 2.5rem;
                font-weight: 700;
                color: var(--primary-blue);
                margin-top: 1rem;
                margin-bottom: 1.5rem;
            }}

            h3 {{
                border-bottom: 2px solid var(--soft-blue);
                padding-bottom: 0.5rem;
                margin-bottom: 1.5rem;
                color: var(--primary-blue);
            }}

            ul {{
                list-style: none;
                padding: 0;
                text-align: left;
                margin-bottom: 2rem;
            }}

            li {{
                background-color: var(--soft-blue);
                padding: 10px 15px;
                margin-bottom: 10px;
                border-radius: 8px;
            }}

            .correct {{
                color: #28a745;
                font-weight: bold;
            }}

            .wrong {{
                color: #dc3545;
                font-weight: bold;
            }}
            
            a {{
                display: inline-block;
                padding: 10px 20px;
                font-size: 1rem;
                background-color: var(--primary-blue);
                color: white;
                border: none;
                border-radius: 8px;
                text-decoration: none;
                transition: background-color 0.3s;
            }}
            
            a:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>

    <div class="container">
        <h1>Hasil Quiz Hijaiyah – Bab 1</h1>
        <div class="score">Nilai kamu: {score} / {total}</div>
        <h3>Rincian Jawaban:</h3>
        <ul>
          {''.join(f"<li>{k}: <span class='{'correct' if v == 'Benar' else 'wrong'}'>{v}</span></li>" for k, v in detail.items())}
        </ul>
        <a href="/api/index">Kerjakan lagi</a>
    </div>

    </body>
    </html>
    """
    return HTMLResponse(content=html)
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

    # Q6
    if all(k in q6 for k in ["ب", "ت", "ث", "ج", "ح", "خ", "d", "ذ", "س", "ش"]):
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
    if all(h in q8 for h in ["ق", "l", "m"]):
        score += 1
        detail["q8"] = "Benar"
    else:
        detail["q8"] = "Salah"

    # Q9
    ans9 = set(q9.replace(" ", ""))
    if len(ans9 & NO_DOT) >= 5:
        score += 1
        detail["q9"] = "Benar"
    else:
        detail["q9"] = "Salah"

    # Q10
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
    
