let messages = document.getElementById("messages");
let inputMessage = document.getElementById("input-message");
let typing = document.getElementById("typing");

function sendMessage() {
    let userMessage = inputMessage.value.trim();
    if (userMessage !== "") {
        displayMessage(userMessage, "user");
        inputMessage.value = "";

        typing.style.display = "block";
        setTimeout(() => {
            typing.style.display = "none";
            displayMessage("Respuesta de J.A.F.L.: " + userMessage, "jafl");
        }, 1500);
    }
}

function displayMessage(message, sender) {
    let messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);
    messageElement.textContent = message;
    messages.appendChild(messageElement);
    messages.scrollTop = messages.scrollHeight;
}

// Cambiar imagen de perfil usuario
document.getElementById("user-img").addEventListener("change", function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById("user-profile").src = e.target.result;
    };
    reader.readAsDataURL(file);
});

// Cambiar imagen de perfil J.A.F.L.
document.getElementById("jafl-img").addEventListener("change", function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById("jafl-profile").src = e.target.result;
    };
    reader.readAsDataURL(file);
});
