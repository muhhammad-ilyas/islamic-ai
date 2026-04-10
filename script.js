
const chat = document.getElementById("chat");
const input = document.getElementById("input");
const sendBtn = document.getElementById("sendBtn");
const voiceBtn = document.getElementById("voiceBtn");

// ADD MESSAGE
function addMsg(text, type){
    const div = document.createElement("div");
    div.className = "msg " + type;
    div.innerText = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

// SEND async function send(){
    const text = input.value.trim();
    if(!text) return;

    addMsg(text, "user");
    input.value = "";

    try {
        const res = await fetch("https://your-app-name.onrender.com/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ q: text, lang: "en" })
        });

        const data = await res.json();

        addMsg(data.answer, "bot");

    } catch (error) {
        addMsg("⚠️ Server not responding", "bot");
    }
}


// BUTTON CLICK FIX
sendBtn.addEventListener("click", send);

// ENTER KEY FIX
input.addEventListener("keypress", function(e){
    if(e.key === "Enter"){
        send();
    }
});

// VOICE FIX
voiceBtn.addEventListener("click", ()=>{
    const rec = new webkitSpeechRecognition();
    rec.lang = "ur-PK";

    rec.onresult = e=>{
        input.value = e.results[0][0].transcript;
    };

    fetch("https://islamic-ai-lkej.onrender.com/ask")
