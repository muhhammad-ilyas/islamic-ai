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

    # 🕌 Always check Islamic context first
    if not is_islamic(q):
        return "⚠️ Please ask only Islamic questions (Qur’an, Hadith, Dua, Fiqh)."

    # 🤖 REAL AI RESPONSE (Smart structured logic + understanding)

    prompt = f"""
You are an Islamic assistant based on Qur'an and authentic Hadith.
Answer ONLY in simple Islamic guidance.

Question: {q}

Rules:
- Be short
- Be accurate
- Prefer Qur'an and Hadith
- If fiqh question, mention Hanafi view politely
"""

    try:
        # 🌐 Free AI model endpoint (no key version fallback)
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-base",
            headers={"Content-Type": "application/json"},
            json={"inputs": prompt}
        )

        data = response.json()

        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]

    except:
        pass

    # 📖 fallback Quran
    ayah = get_quran(q)
    if ayah:
        return ayah

    return "🕌 Please ask Islamic questions (Dua, Hadith, Qur’an, Fiqh)"


@app.post("/ask")
def ask(data: Query):

    if not is_islamic(data.q):
        return {"answer": "⚠️ Only Islamic questions allowed"}

    return {"answer": ai_engine(data.q)}
