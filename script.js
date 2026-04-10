const chat = document.getElementById("chat");
const input = document.getElementById("input");
const sendBtn = document.getElementById("sendBtn");

// 💬 ADD MESSAGE
function addMsg(text, type){
    const div = document.createElement("div");
    div.className = "msg " + type;
    div.innerText = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

// ⏳ TYPING INDICATOR
function typing(){
    const div = document.createElement("div");
    div.className = "msg bot";
    div.id = "typing";
    div.innerText = "typing...";
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function removeTyping(){
    const t = document.getElementById("typing");
    if(t) t.remove();
}

// 🚀 SEND MESSAGE
async function send(){
    const text = input.value.trim();
    if(!text) return;

    addMsg(text, "user");
    input.value = "";

    typing();

    try {
        const res = await fetch("https://islamic-ai-lkej.onrender.com/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ q: text, lang: "en" })
        });

        const data = await res.json();

        removeTyping();
        addMsg(data.answer, "bot");

    } catch (error) {
        removeTyping();
        addMsg("⚠️ Server not responding", "bot");
    }
}

// 🖱️ CLICK
sendBtn.addEventListener("click", send);

// ⌨️ ENTER
input.addEventListener("keypress", function(e){
    if(e.key === "Enter"){
        send();
    }
});
