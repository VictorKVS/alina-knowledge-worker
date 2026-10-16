"""Offline append-only Telegram event projection for ALINA. No Telegram API access."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any

@dataclass
class MessageState:
    chat_id: str
    message_id: str
    revision: int = 0
    current_hash: str | None = None
    deleted: bool = False
    events: list[dict[str, Any]] = field(default_factory=list)

class MessageHistory:
    def __init__(self):
        self.messages: dict[tuple[str, str], MessageState] = {}
    def apply(self, event: dict[str, Any]) -> dict[str, Any]:
        kind = event.get("type")
        if kind not in {"new", "edit", "delete"}:
            raise ValueError("event type must be new, edit or delete")
        if event.get("authorized") is not True:
            raise PermissionError("source authorization required")
        chat_id, message_id = str(event.get("chat_id", "")), str(event.get("message_id", ""))
        if not chat_id or not message_id:
            raise ValueError("missing IDs")
        key = (chat_id, message_id)
        state = self.messages.get(key)
        if kind == "new" and state is not None:
            raise ValueError("message already registered")
        if kind != "new" and state is None:
            raise ValueError("cannot edit/delete unknown message")
        if state is None:
            state = MessageState(chat_id, message_id)
            self.messages[key] = state
        if kind == "edit" and state.deleted:
            raise ValueError("cannot edit deleted message")
        body = event.get("text", "")
        if kind in {"new", "edit"} and not isinstance(body, str):
            raise ValueError("text must be string")
        digest = None if kind == "delete" else sha256(body.encode("utf-8")).hexdigest()
        if kind == "edit" and digest == state.current_hash:
            return {"change": "unchanged", "revision": state.revision}
        state.revision += 1
        state.current_hash = digest
        state.deleted = kind == "delete"
        record = {"type": kind, "revision": state.revision,
                  "sha256": digest, "timestamp": event.get("timestamp"),
                  "source_ref": event.get("source_ref")}
        state.events.append(record)
        return {"change": kind, "revision": state.revision}
