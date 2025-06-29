async function createGame() {
  const res = await fetch("https://electricity-game.onrender.com/create_game", {
    method: "POST"
  });
  const data = await res.json();
  document.getElementById("gameId").textContent = data.game_id;
}