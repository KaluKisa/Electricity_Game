let gameId, player, socket;

localStorage.setItem("gameId", gameId);
localStorage.setItem("player", player);

const savedGameId = localStorage.getItem("gameId");
const savedPlayer = localStorage.getItem("player");

if (savedGameId && savedPlayer) {
  gameId = savedGameId;
  player = savedPlayer;
  joinGame(); // auto-reconnect
}


async function joinGame() {
  gameId = document.getElementById("gameId").value;
  player = document.getElementById("player").value;

  const res = await fetch(`https://electricity-game.onrender.com/join?game_id=${gameId}&player=${player}`, {
    method: "POST"
  });
  
  const data = await res.json();
  document.getElementById("generator").textContent = data.generator;

  socket = new WebSocket(`wss://electricity-game.onrender.com/ws/${gameId}/${player}`);
  socket.onmessage = (event) => {
    document.getElementById("state").textContent = event.data;
  };
}

async function submitBid() {
  const amount = parseFloat(document.getElementById("bid").value);
  await fetch("https://electricity-game.onrender.com/submit_bid", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id: gameId, player, amount })
  });
}
