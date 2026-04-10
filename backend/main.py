from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    q: str
    lang: str = "en"


def is_islamic(text):
    words = ["allah","quran","hadith","dua","islam","namaz","roza","zakat","fatwa"]
    return any(w in text.lower() for w in words)


def get_quran(text):
    try:
        url = f"https://api.quran.com/api/v4/search?q={text}"
        r = requests.get(url).json()

        if r.get("search", {}).get("results"):
            ayah = r["search"]["results"][0]
            return f"📖 {ayah['text']} ({ayah['verse_key']})"
    except:
        return None


def get_fatwa():
    return """⚖️ Hanafi Fatwa:
- https://darulifta-deoband.com
- https://askimam.org
"""


def ai_engine(q):
    if "dua" in q.lower():
        return "🤲 اللهم إنك عفو تحب العفو فاعف عني"

    ayah = get_quran(q)
    if ayah:
        return ayah

    if "fatwa" in q.lower():
        return get_fatwa()

    return "🕌 Actions are judged by intentions (Bukhari)"


@app.post("/ask")
def ask(data: Query):

    if not is_islamic(data.q):
        return {"answer": "⚠️ Only Islamic questions allowed"}

    return {"answer": ai_engine(data.q)}
