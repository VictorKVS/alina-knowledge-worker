from __future__ import annotations

import hashlib
from pathlib import Path


class ObjectStore:
    def put_text(self, key: str, content: str) -> str:
        raise NotImplementedError

    def get_text(self, key: str) -> str:
        raise NotImplementedError


class LocalObjectStore(ObjectStore):
    def __init__(self, root: str = ".ak01_objects") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put_text(self, key: str, content: str) -> str:
        safe = hashlib.sha256(key.encode("utf-8")).hexdigest()
        path = self.root / safe
        path.write_text(content, encoding="utf-8")
        return str(path)

    def get_text(self, key: str) -> str:
        safe = hashlib.sha256(key.encode("utf-8")).hexdigest()
        return (self.root / safe).read_text(encoding="utf-8")
