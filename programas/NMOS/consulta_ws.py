import asyncio
import websockets

async def consultar_ws():
    uri = "ws://sb-docker.medusa.csur:81/x-nmos/query/v1.3/subscriptions/cae5bfa0-9f9e-48de-8d5c-c5a362403800"

    try:
        async with websockets.connect(uri) as websocket:
            print("Conectado al WebSocket")

            # Escuchar mensajes del servidor
            while True:
                message = await websocket.recv()
                print(f"Mensaje recibido: {message}")

    except Exception as e:
        print(f"Error: {e}")

asyncio.run(consultar_ws())
