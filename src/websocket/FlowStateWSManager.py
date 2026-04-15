import asyncio
from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections = []
        self.loop = None # Aquí guardaremos el "oro"

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Seteamos el loop global del hilo principal
        if not self.loop:
            self.loop = asyncio.get_running_loop()

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Uso normal desde rutas async de FastAPI"""
        for connection in self.active_connections[:]: # Copia de la lista para evitar errores al remover
            try:
                await connection.send_json(message)
            except Exception:
                self.active_connections.remove(connection)

    def broadcast_from_thread(self, message: dict):
        """
        ESTE ES EL QUE NECESITAS. 
        Llama a este desde tu cámara o servos.
        """
        if self.loop and self.loop.is_running():
            # Inyecta la corrutina de broadcast en el hilo principal
            asyncio.run_coroutine_threadsafe(self.broadcast(message), self.loop)
        else:
            # Fallback si el loop no está listo (útil para debug)
            print(f"⚠️ Loop no listo. Mensaje perdido: {message}")

manager = ConnectionManager()