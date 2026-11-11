from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SourceChunk:
    ordinal: int
    text: str
    locator: str


class SourceParser:
    def chunk(self, content: str, *, locator_prefix: str = "body", max_chars: int = 1200) -> list[SourceChunk]:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", content) if p.strip()]
        chunks: list[SourceChunk] = []
        ordinal = 0

        for paragraph in paragraphs or [content.strip()]:
            if not paragraph:
                continue
            start = 0
            while start < len(paragraph):
                piece = paragraph[start:start + max_chars].strip()
                if piece:
                    chunks.append(SourceChunk(
                        ordinal=ordinal,
                        text=piece,
                        locator=f"{locator_prefix}#chunk-{ordinal}",
                    ))
                    ordinal += 1
                start += max_chars
        return chunks
