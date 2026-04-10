function addMsg(text, type){
    const div = document.createElement("div");
    div.className = "msg " + type;
    div.innerText = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

/* ISLAMIC FILTER */
function isIslamic(text){
    const words = ["allah","quran","hadith","dua","islam","namaz","roza","zakat","fatwa"];
    return words.some(w => text.toLowerCase().includes(w));
}

/* RESPONSE ENGINE */
function reply(text, lang){

    if(!isIslamic(text)){
        return lang==="ur"
        ? "⚠️ صرف اسلامی سوالات"
        : "⚠️ Only Islamic questions allowed";
    }

    if(text.includes("dua")){
        return "🤲 اللهم إنك عفو تحب العفو فاعف عني";
    }

    if(text.includes("sad") || text.includes("stress")){
        return "📖 Qur’an 94:6 — Indeed, with hardship comes ease";
    }

    if(text.includes("fatwa")){
        return "⚖️ Hanafi Fatwa:\nhttps://darulifta-deoband.com\nhttps://askimam.org";
    }

    return "🕌 Hadith: Actions are judged by intentions (Bukhari)";
}

/* SEND */
async function send(){
    const input = document.getElementById("input");
    const lang = document.getElementById("lang").value;

    if(!input.value) return;

    addMsg(input.value, "user");

    const text = input.value;
    input.value = "";

    try {
        const res = await fetch("https://YOUR-BACKEND.onrender.com/ask", {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body: JSON.stringify({q:text, lang})
        });

        const data = await res.json();
        addMsg(data.answer, "bot");

    } catch {
        addMsg(reply(text, lang), "bot");
    }
}

/* VOICE */
function voice(){
    const rec = new webkitSpeechRecognition();
    rec.lang = "ur-PK";

    rec.onresult = e => {
        document.getElementById("input").value =
        e.results[0][0].transcript;
    };

    rec.start();
}
