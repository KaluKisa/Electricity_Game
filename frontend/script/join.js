let gameId, player, socket;

async function joinGame() {
  gameId = document.getElementById("gameId").value;
  player = document.getElementById("player").value;

  const res = await fetch("https://electricity-game.onrender.com/join", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      game_id: gameId,
      player: player
    })
  });

  const data = await res.json();
  if (data.error) {
    alert(data.error);
    return;
  }

  document.getElementById("generator").textContent = data.generator;

  socket = new WebSocket(`wss://electricity-game.onrender.com/ws/${gameId}/${player}`);
  socket.onmessage = (event) => {
    document.getElementById("state").textContent = event.data;
  };
}
