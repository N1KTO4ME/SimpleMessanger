import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    # Добавляем нового клиента в список
    connected_clients.add(websocket)
    print(f"Client connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # Отправляем сообщение всем клиентам
            await asyncio.gather(
                *[client.send(message) for client in connected_clients if client != websocket]
            )
    except websockets.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

asyncio.run(main())
