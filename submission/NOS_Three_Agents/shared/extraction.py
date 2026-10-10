"""PDF text extraction and canonical-source creation.

Method: PyMuPDF ``page.get_text()`` with default arguments, pages joined
in order with no separator. This is the first step of the organisers'
tutorial (tutorials/pdf__to__txt.ipynb). The tutorial's second step
(``remove_all_special_characters``) is NOT applied: it strips accents,
punctuation and line breaks, which contradicts the brief's own sample of
a correct output.

Canonicalisation is limited to the newline convention (CRLF/CR -> LF).
Accents, punctuation and all spaces, including the space PyMuPDF emits at
the end of each line of this PDF, are left untouched.
"""
from __future__ import annotations


def extract_raw(pdf_path) -> dict:
    import fitz

    with fitz.open(str(pdf_path)) as doc:
        pages = [page.get_text() for page in doc]
        meta = dict(doc.metadata or {})
    return {
        "text": "".join(pages),
        "page_count": len(pages),
        "chars_per_page": [len(p) for p in pages],
        "pdf_metadata": meta,
        "pymupdf_version": fitz.VersionBind,
    }


def canonicalize(raw_text: str) -> str:
    """Normalise the newline convention only."""
    return raw_text.replace("\r\n", "\n").replace("\r", "\n")
