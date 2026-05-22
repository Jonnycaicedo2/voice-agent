"""Entry point for the voice agent."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from aiohttp import web

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Voice Agent</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0; 
               display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { text-align: center; padding: 2rem; max-width: 500px; }
        h1 { font-size: 2rem; margin-bottom: 1rem; }
        .status { font-size: 1.2rem; padding: 0.5rem 1rem; border-radius: 8px; 
                  background: #1e293b; margin: 1rem 0; display: inline-block; }
        .status.listening { background: #166534; }
        button { padding: 0.75rem 2rem; font-size: 1.1rem; border: none; border-radius: 8px; 
                 cursor: pointer; margin: 0.5rem; }
        .start-btn { background: #16a34a; color: white; }
        .stop-btn { background: #dc2626; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Voice Agent</h1>
        <div id="status" class="status">Listo</div>
        <div>
            <button class="start-btn" onclick="send('start')">Iniciar</button>
            <button class="stop-btn" onclick="send('stop')">Detener</button>
        </div>
    </div>
    <script>
        const ws = new WebSocket('ws://localhost:8000/ws');
        ws.onmessage = (e) => {
            const d = JSON.parse(e.data);
            document.getElementById('status').textContent = d.status;
        };
        function send(action) { ws.send(JSON.stringify({action})); }
    </script>
</body>
</html>"""


async def index(request):
    return web.Response(text=HTML, content_type="text/html")


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            import json
            data = json.loads(msg.data)
            if data.get("action") == "start":
                await ws.send_json({"status": "Escuchando..."})
            elif data.get("action") == "stop":
                await ws.send_json({"status": "Listo"})

    return ws


async def main():
    print("Voice Agent starting...")

    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/ws", websocket_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8000)
    await site.start()

    print("Frontend running at http://localhost:8000")
    print("Press Ctrl+C to stop")

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nVoice Agent stopped.")