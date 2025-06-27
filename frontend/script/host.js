async function createGame() {
  const res = await fetch("https://YOUR_BACKEND_URL/create_game", { method: "POST" });
  const data = await res.json();
  document.getElementById("gameId").textContent = data.game_id;
}
