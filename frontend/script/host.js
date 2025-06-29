async function createGame() {
  const res = await fetch("https://electricity-backend.onrender.com/create_game", {
    method: "POST"
  });
  const data = await res.json();
  document.getElementById("gameId").textContent = data.game_id;
}