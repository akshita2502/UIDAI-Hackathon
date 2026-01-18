"""WebSocket server configuration for real-time alert streaming"""

import socketio

# Initialize the Async Server
# cors_allowed_origins='*' allows React to connect from a different port
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


# Define Event Handlers
@sio.event
async def connect(sid, _environ):
    """
    Handle client WebSocket connection events.

    Args:
        sid: Socket ID of the connecting client
        _environ: ASGI environment (unused)
    """
    print(f"Client connected: {sid}")


@sio.event
async def disconnect(sid):
    """
    Handle client WebSocket disconnection events.

    Args:
        sid: Socket ID of the disconnecting client
    """
    print(f"Client disconnected: {sid}")
