let gameId, player, socket;

async function joinGame() {
  gameId = document.getElementById("gameId").value;
  player = document.getElementById("player").value;

  const res = await fetch(`https://YOUR_BACKEND_URL/join?game_id=${gameId}&player=${player}`, {
    method: "POST"
  });
  const data = await res.json();
  document.getElementById("generator").textContent = data.generator;

  socket = new WebSocket(`wss://YOUR_BACKEND_URL/ws/${gameId}/${player}`);
  socket.onmessage = (event) => {
    document.getElementById("state").textContent = event.data;
  };
}

async function submitBid() {
  const amount = parseFloat(document.getElementById("bid").value);
  await fetch("https://YOUR_BACKEND_URL/submit_bid", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id: gameId, player, amount })
  });
}
