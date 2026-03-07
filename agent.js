async function sendMessage() {
  const input = document.querySelector("input");
  const msg = input.value;

  const res = await fetch("http://127.0.0.1:8000/v/prompt", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: msg})
  });

  const data = await res.json();
  alert(data.response || JSON.stringify(data));
}

document.querySelector("button")?.addEventListener("click", sendMessage);
