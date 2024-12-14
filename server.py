from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


template = Jinja2Templates(directory="templates")


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name='static')



# Manage connected WebSocket clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"User says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("A user disconnected.")


# Simple HTML for testing
@app.get("/")
async def get(request: Request):
    return template.TemplateResponse("index.html", {"request": request})
