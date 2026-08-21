const API_URL = "http://127.0.0.1:8000/ask";

const chat = document.getElementById("chat");
const questionInput = document.getElementById("question");
const sendButton = document.getElementById("sendButton");
const micButton = document.getElementById("micButton");
const modeSelect = document.getElementById("mode");


function addMessage(type, text, sources = []) {

    const message = document.createElement("div");

    message.className = "message " + type;

    const name = type === "jarvis" ? "JARVIS" : "YOU";

    message.innerHTML = `<strong>${name}</strong><p>${text}</p>`;

    if (sources.length > 0) {

        const sourceDiv = document.createElement("div");

        sourceDiv.className = "sources";

        sourceDiv.innerHTML = "<strong>Sources:</strong>";

        sources.forEach(source => {

            const link = document.createElement("a");

            link.href = source.url;
            link.target = "_blank";
            link.textContent = source.title || source.url;

            sourceDiv.appendChild(link);

        });

        message.appendChild(sourceDiv);
    }

    chat.appendChild(message);

    chat.scrollTop = chat.scrollHeight;
}


async function askJarvis() {

    const question = questionInput.value.trim();

    if (!question) return;

    addMessage("user", question);

    questionInput.value = "";

    sendButton.disabled = true;

    addMessage("jarvis", "Processing request... 🌐🧠");

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question,
                mode: modeSelect.value
            })

        });

        const data = await response.json();

        chat.removeChild(chat.lastChild);

        if (data.error) {

            addMessage(
                "jarvis",
                "System Error: " + data.error
            );

        } else {

            addMessage(
                "jarvis",
                data.jarvis,
                data.sources || []
            );

            speak(data.jarvis);
        }

    } catch (error) {

        chat.removeChild(chat.lastChild);

        addMessage(
            "jarvis",
            "Sir, backend se connection nahi ho saka. Check karein ke JARVIS server chal raha hai."
        );

    }

    sendButton.disabled = false;
}


function speak(text) {

    if (!("speechSynthesis" in window)) return;

    speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "ur-PK";

    speech.rate = 1;

    speechSynthesis.speak(speech);
}


sendButton.addEventListener("click", askJarvis);

questionInput.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {
        askJarvis();
    }

});


const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


if (SpeechRecognition) {

    const recognition = new SpeechRecognition();

    recognition.lang = "ur-PK";

    recognition.continuous = false;

    recognition.interimResults = false;


    micButton.addEventListener("click", function() {

        recognition.start();

        micButton.innerText = "🔴";

    });


    recognition.onresult = function(event) {

        questionInput.value =
            event.results[0][0].transcript;

        micButton.innerText = "🎤";

        askJarvis();

    };


    recognition.onerror = function() {

        micButton.innerText = "🎤";

    };


    recognition.onend = function() {

        micButton.innerText = "🎤";

    };

} else {

    micButton.style.display = "none";

}

document.querySelectorAll(".trade-example").forEach(button => {
    button.addEventListener("click", () => {
        const question = button.dataset.question;

        const modeSelect = document.querySelector("select");

        if (modeSelect) {
            modeSelect.value = "trade";
        }

        const input = document.querySelector("input, textarea");

        if (input) {
            input.value = question;
            input.focus();
        }
    });
});


document.querySelectorAll(".trade-example").forEach(button => {
    button.addEventListener("click", () => {
        const question = button.dataset.question;
        const modeSelect = document.querySelector("select");

        if (modeSelect) {
            modeSelect.value = "trade";
        }

        const input = document.querySelector("input, textarea");

        if (input) {
            input.value = question;
            input.focus();
        }
    });
});

