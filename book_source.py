"""Local source-view helpers for book study.

The original copyrighted PDF stays on the user's machine. This module renders
requested source pages locally so ALINA can show the exact page (including
figures/tables) next to derived knowledge without copying the book into Git.
"""
from __future__ import annotations

from pathlib import Path
import hashlib


class BookSourceError(ValueError):
    pass


def source_hash(path: Path) -> str:
    path=Path(path)
    with path.open("rb") as f:
        return hashlib.file_digest(f,"sha256").hexdigest()


def render_pdf_page(path: Path, page_number: int, output_dir: Path, scale: float=1.5) -> Path:
    """Render one 1-based PDF page as PNG."""
    import pypdfium2 as pdfium
    path=Path(path)
    output_dir=Path(output_dir)
    if page_number < 1:
        raise BookSourceError("page_number must be >= 1")
    if not path.is_file() or path.suffix.lower() != ".pdf":
        raise BookSourceError("source must be an existing PDF")
    output_dir.mkdir(parents=True,exist_ok=True)
    with pdfium.PdfDocument(str(path)) as pdf:
        if page_number > len(pdf):
            raise BookSourceError(f"page {page_number} exceeds PDF length {len(pdf)}")
        page=pdf[page_number-1]
        try:
            bitmap=page.render(scale=scale)
            try:
                image=bitmap.to_pil()
                target=output_dir/f"page-{page_number:04d}.png"
                image.save(target,"PNG")
            finally:
                bitmap.close()
        finally:
            page.close()
    return target


def extract_page_text(path: Path, page_number: int) -> dict:
    """Return exact local page text and source locator; does not infer meaning."""
    import pypdfium2 as pdfium
    path=Path(path)
    if page_number < 1:
        raise BookSourceError("page_number must be >= 1")
    with pdfium.PdfDocument(str(path)) as pdf:
        if page_number > len(pdf):
            raise BookSourceError(f"page {page_number} exceeds PDF length {len(pdf)}")
        page=pdf[page_number-1]
        try:
            textpage=page.get_textpage()
            try:
                text=textpage.get_text_range()
            finally:
                textpage.close()
        finally:
            page.close()
    return {"page":page_number,"locator":f"page {page_number}","text":text}


def chapter_source_bundle(path: Path, start_page: int, end_page: int, output_dir: Path) -> dict:
    """Create a local visual bundle for a bounded chapter range."""
    if start_page < 1 or end_page < start_page:
        raise BookSourceError("invalid chapter page range")
    rendered=[]
    for page in range(start_page,end_page+1):
        rendered.append(str(render_pdf_page(path,page,output_dir)))
    return {
        "source_sha256":source_hash(path),
        "start_page":start_page,
        "end_page":end_page,
        "rendered_pages":rendered,
        "public_export_allowed":False,
        "note":"Rendered originals are local review artifacts and must not be committed to public Git."
    }
