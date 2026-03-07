async function sendMessage() {

let input = document.getElementById("message");
let chat = document.getElementById("chat");

let msg = input.value;

if (!msg) return;

chat.innerHTML += "<p><b>You:</b> " + msg + "</p>";

input.value = "";

try {

let res = await fetch("http://127.0.0.1:8001/ask", {
method: "POST",
headers: {
"Content-Type": "application/json"
},
body: JSON.stringify({message: msg})
});

let data = await res.json();

chat.innerHTML += "<p><b>Weberdy:</b> " + JSON.stringify(data) + "</p>";

chat.scrollTop = chat.scrollHeight;

} catch (err) {

chat.innerHTML += "<p><b>Error:</b> " + err + "</p>";

}

}
