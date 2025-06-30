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
  const data = JSON.parse(event.data);
  const players = data.players.map(p => `${p.name} (${p.generator}) — $${p.bid ?? 'No bid'}`).join('\\n');
  document.getElementById("state").textContent = players;
};

}


async function submitBid() {
  const gameId = document.getElementById("gameId").value;
  const player = document.getElementById("player").value;
  const bid = parseFloat(document.getElementById("bid").value);

  const res = await fetch("https://electricity-game.onrender.com/submit_bid", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      game_id: gameId,
      player: player,
      amount: bid  // send as 'amount'
    })
  });

  const data = await res.json();
  if (data.error) {
    alert(data.error);
    return;
  }

  console.log("Bid submitted");
}
