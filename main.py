from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

CLIENTS = {}

# index.htmlファイルをHTMLResponseに渡すためにテキストに変換
with open("index.html", "rt") as f:
    html = f.read()

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # 接続しているソケットをキーで識別する
    key = websocket.headers.get('sec-websocket-key')
    CLIENTS[key] = websocket
    
    try:
        while True:
            data = await websocket.receive()

            # 送信されてきたデータ部分を取り出して辞書に変換
            data = data['text']
            data = json.loads(data)

            # 接続しているすべてのクライアントにメッセージを送信
            for client in CLIENTS.values():
                user = data["user"]
                message = data["messageText"]
                await client.send_text(f"User: {user} | Message: {message}")
    except:
        await websocket.close()
        del CLIENTS[key]