from robyn import Robyn, jsonify, WebSocket, WebSocketConnector
import json
from typing import Dict, Set, Optional


app = Robyn(__file__)
websocket = WebSocket(app, "/chat")  # WebSocket endpoint at /chat

# In-memory storage (replace with a DB in production)
users: Dict[str, dict] = {}  # {username: {role, ws_id}}
rooms: Dict[str, Set[str]] = {}  # {room_name: set of usernames}
roles_permissions = {
    "admin": {"kick", "delete", "broadcast"},
    "moderator": {"kick", "delete"},
    "user": {"chat"}
}

# Helper function to check permissions
def has_permission(username: str, action: str) -> bool:
    user_role = users.get(username, {}).get("role", "user")
    return action in roles_permissions.get(user_role, set())

# WebSocket connect event
@websocket.on("connect")
async def on_connect(ws: WebSocketConnector) -> str:
    ws_id = ws.id
    print(f"Client connected: {ws_id}")
    await ws.async_send_to(ws_id, json.dumps({"status": "Connected to server"}))
    return ""

# WebSocket message event
@websocket.on("message")
async def on_message(ws: WebSocketConnector, msg: str, global_dependencies=None) -> str:
    ws_id = ws.id
    try:
        data = json.loads(msg)
        action = data.get("action")
        room = data.get("room")
        content = data.get("content")

        # Find username associated with this ws_id
        username = next((u for u, info in users.items() if info["ws_id"] == ws_id), None)

        # Handle user login
        if action == "login" and not username:
            username = data.get("username")
            role = data.get("role", "user")  # Default to "user"
            if username in users:
                await ws.async_send_to(ws_id, json.dumps({"error": "Username taken"}))
                ws.close()
                return "Username taken"
            users[username] = {"role": role, "ws_id": ws_id}
            await ws.async_send_to(ws_id, json.dumps({"status": "logged_in", "username": username}))
            await ws.async_broadcast(json.dumps({"status": f"{username} connected"}))
            return "Logged in"

        # All subsequent actions require a logged-in user
        if not username:
            await ws.async_send_to(ws_id, json.dumps({"error": "Not logged in"}))
            return "Not logged in"

        # Handle joining a room
        if action == "join":
            if room not in rooms:
                rooms[room] = set()
            rooms[room].add(username)
            await broadcast(room, {"status": f"{username} joined {room}"}, ws)

        # Handle chat messages
        elif action == "chat" and room in rooms:
            if has_permission(username, "chat"):
                await broadcast(room, {"username": username, "message": content}, ws)
            else:
                await ws.async_send_to(ws_id, json.dumps({"error": "No permission to chat"}))

        # Handle admin/moderator actions (e.g., kick)
        elif action == "kick" and room in rooms:
            target = data.get("target")
            if has_permission(username, "kick") and target in rooms[room]:
                rooms[room].remove(target)
                target_ws_id = users[target]["ws_id"]
                await ws.async_send_to(target_ws_id, json.dumps({"status": f"Kicked from {room}"}))
                await broadcast(room, {"status": f"{target} was kicked by {username}"}, ws)

        # Handle disconnect request
        elif action == "disconnect":
            ws.close()
            return "Closing connection"

    except Exception as e:
        print(f"Message handling error: {e}")
        await ws.async_send_to(ws_id, json.dumps({"error": "Invalid message"}))
    return ""

# WebSocket close event
@websocket.on("close")
async def on_close(ws: WebSocketConnector) -> str:
    ws_id = ws.id
    username = next((u for u, info in users.items() if info["ws_id"] == ws_id), None)
    if username:
        del users[username]
        for room_set in rooms.values():
            room_set.discard(username)
        await ws.async_broadcast(json.dumps({"status": f"{username} disconnected"}))
    print(f"Client disconnected: {ws_id}")
    return ""

# Broadcast message to all users in a room
async def broadcast(room: str, message: dict, ws: WebSocketConnector):
    if room not in rooms:
        return
    message_json = json.dumps(message)
    for username in rooms[room].copy():  # Use copy to avoid runtime changes
        try:
            target_ws_id = users[username]["ws_id"]
            await ws.async_send_to(target_ws_id, message_json)
        except Exception as e:
            print(f"Error broadcasting to {username}: {e}")

# Optional HTTP endpoint for status
@app.get("/status")
async def status(request):
    return {"status": "Server running", "connected_users": len(users), "rooms": len(rooms)}

# Start the server
if __name__ == "__main__":
    app.start(host="0.0.0.0", port=8080)
    # python ws_robyn.py --processes 20 --workers 20 --log-level WARN


'''
{
	"action": "login",
	"username": "u1"
}


{
	"action": "join",
	"room": "r1",
}



'''