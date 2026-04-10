import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

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


# 🕌 SIMPLE DUAS DATABASE
DUAS = {
    "sleep": "اللهم باسمك أموت وأحيا",
    "eat": "بِسْمِ ٱللّٰهِ وَعَلَىٰ بَرَكَةِ ٱللّٰهِ",
    "home": "بِسْمِ ٱللّٰهِ تَوَكَّلْتُ عَلَى ٱللّٰهِ",
}


def is_islamic(q):
    keywords = ["islam","quran","hadith","dua","pray","namaz","marriage","fasting","zakat"]
    return any(k in q.lower() for k in keywords)


# 🤖 REAL GPT-LIKE RESPONSE (Hugging Face)
def ask_ai(q):

    prompt = f"""
You are an Islamic scholar AI based on Qur'an and authentic Hadith.

Rules:
- Be accurate
- Use simple explanation
- Prefer Qur'an or Hadith if needed
- Follow Sunni (Hanafi-friendly) understanding
- Do not be extreme

Question: {q}
"""

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
            headers={"Content-Type": "application/json"},
            json={"inputs": prompt}
        )

        data = response.json()

        if isinstance(data, list):
            return "🕌 " + data[0].get("generated_text", "No response")

    except:
        pass

    return "🕌 AI temporarily unavailable, try again."


# 🧠 MAIN ENGINE
def ai_engine(q):

    q_lower = q.lower()

    # 🕌 DUAS FIRST
    for k in DUAS:
        if k in q_lower:
            return f"🤲 {DUAS[k]}"

    # ⚖️ MARRIAGE
    if "marry" in q_lower or "marriage" in q_lower:
        return """⚖️ Islamic View (Hanafi):
A man can marry up to 4 wives if he is just.

Conditions:
✔ Justice
✔ Financial support
✔ Equal treatment"""

    # 🤖 REAL AI
    if is_islamic(q):
        return ask_ai(q)

    return "⚠️ Please ask Islamic questions only"


@app.post("/ask")
def ask(data: Query):
    return {"answer": ai_engine(data.q)}
