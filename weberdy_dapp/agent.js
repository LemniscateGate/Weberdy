async function sendMessage() {
  const input = document.querySelector("input");
  const message = input.value;
  const chat = document.getElementById("chat");
  chat.innerHTML += "<p><b>You:</b> " + message + "</p>";
  try {
    const res = await fetch("http://127.0.0.1:8001/v/prompt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: message
      })
    });
    const data = await res.json();
    chat.innerHTML += "<p><b>Weberdy:</b> " + JSON.stringify(data) + "</p>";
  } catch (err) {
    chat.innerHTML += "<p><b>Error:</b> Could not reach Weberdy API</p>";
    console.error(err);
  }
  input.value = "";
}

document.querySelector("button").addEventListener("click", sendMessage);

document.querySelector("input").addEventListener("keypress", function(e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});
