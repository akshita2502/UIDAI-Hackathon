import socketio

# Initialize the Async Server
# cors_allowed_origins='*' allows React to connect from a different port
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# Define Event Handlers
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")