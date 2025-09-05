from __future__ import annotations
from flask_socketio import SocketIO, emit

def register_socket_events(socketio: SocketIO) -> None:
    @socketio.on("connect")
    def _connect():
        emit("connected", {"message": "socket connected"})

    @socketio.on("join")
    def _join(data):
        # room = data.get("room")
        # join_room(room)
        emit("joined", {"ok": True})

    # Server push examples
    def push_schedule_update(schedule):
        socketio.emit("schedule_update", schedule)

    def push_notification(payload):
        socketio.emit("notification", payload)

    # Expose helpers
    socketio.push_schedule_update = push_schedule_update  # type: ignore
    socketio.push_notification = push_notification  # type: ignore
