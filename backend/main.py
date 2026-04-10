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

    q_lower = q.lower()

    # 🛡️ ISLAMIC SAFETY CHECK
    allowed_keywords = [
        "islam", "quran", "qur'an", "hadith", "dua",
        "pray", "namaz", "zakat", "fasting", "ramadan",
        "marriage", "halal", "haram", "fiqh", "fatwa"
    ]

    if not any(word in q_lower for word in allowed_keywords):
        return "⚠️ Please ask only Islamic questions (Qur’an, Hadith, Dua, Fiqh)."

    # 🤖 REAL AI PROMPT (Scholar Style)
    prompt = f"""
You are a knowledgeable Islamic assistant based on Qur'an and authentic Hadith.

Rules:
- Answer in simple language (Urdu/English mix allowed)
- Use Qur'an or Hadith when possible
- Follow general Sunni/Hanafi understanding
- Do NOT give extreme or unsafe opinions
- Keep answer short and clear

Question: {q}
"""

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-large",
            headers={"Content-Type": "application/json"},
            json={"inputs": prompt}
        )

        data = response.json()

        if isinstance(data, list) and "generated_text" in data[0]:
            return "🕌 " + data[0]["generated_text"]

    except:
        pass

    # 📖 FALLBACK: QURAN SEARCH
    ayah = get_quran(q)
    if ayah:
        return ayah

    return "🕌 Please try again or ask a clearer Islamic question."


@app.post("/ask")
def ask(data: Query):

    if not is_islamic(data.q):
        return {"answer": "⚠️ Only Islamic questions allowed"}

    return {"answer": ai_engine(data.q)}
