const out = document.getElementById('out');

async function post(url, payload){
  const r = await fetch(url, {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  });
  return r.json();
}

if (window.APP_MODE === "chat"){
  document.getElementById('send').addEventListener('click', async () => {
    out.textContent = "Procesando...";
    const message = document.getElementById('msg').value;
    const j = await post('/api/chat', {message});
    out.textContent = j.ok ? j.answer : ("Error: " + (j.error || "desconocido"));
  });
}

if (window.APP_MODE === "options"){
  document.getElementById('go').addEventListener('click', async () => {
    out.textContent = "Procesando...";
    const tool = document.getElementById('tool').value;
    let args = {};
    try { args = JSON.parse(document.getElementById('args').value || "{}"); } catch(e) {}
    const j = await post('/api/mcp', {tool, args});
    out.textContent = JSON.stringify(j, null, 2);
  });
}
