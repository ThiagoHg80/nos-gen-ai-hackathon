"""Gera site/index.html com o texto do PDF e o submission.txt.

Uso (a partir da raiz do repositorio):
    python3 submission/interface/build_site.py
    python3 submission/interface/build_site.py FICHEIRO_DE_TESTE
O segundo exemplo usa um ficheiro de teste em vez do submission.txt
(por exemplo, o criado por make_demo_data.py).
"""
import html
import re
import sys

import pymupdf

PDF = "raw_data/document_to_anonymize.pdf"
SUBMISSION = "submission/submission.txt"
TEMPLATE = "submission/interface/template.html"
OUTPUT = "submission/interface/index.html"


def extract_text(path):
    """Texto do PDF, extraido como no notebook dos organizadores."""
    text = ""
    with pymupdf.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def mark_asterisks(text):
    """Escapa o HTML e poe cada * num bloco escuro."""
    safe = html.escape(text)
    return re.sub(r"\*", '<span class="m">*</span>', safe)


def highlight_original(original, submission):
    """Escapa o original e realça as palavras que viraram * no resultado.

    Compara linha a linha, palavra a palavra. Se uma linha tiver um
    numero de palavras diferente no resultado, nao a realça.
    """
    orig_lines = [ln for ln in original.splitlines() if ln.strip()]
    sub_lines = [ln for ln in submission.splitlines() if ln.strip()]
    if len(orig_lines) != len(sub_lines):
        print("Aviso: numero de linhas diferente; sem realces.")
        return html.escape("\n".join(orig_lines))
    out = []
    skipped = 0
    for orig, sub in zip(orig_lines, sub_lines):
        o_parts = re.split(r"(\s+)", orig.rstrip())
        s_words = sub.split()
        o_words = orig.split()
        if len(o_words) != len(s_words):
            skipped += 1
            out.append(html.escape(orig.rstrip()))
            continue
        index = 0
        for i, part in enumerate(o_parts):
            if part.strip():
                masked = "*" in s_words[index] and part != s_words[index]
                index += 1
                piece = html.escape(part)
                o_parts[i] = f"<mark>{piece}</mark>" if masked else piece
            else:
                o_parts[i] = html.escape(part)
        out.append("".join(o_parts))
    total = len(orig_lines)
    print(f"Linhas alinhadas: {total - skipped} de {total}.")
    if skipped:
        print(f"Aviso: {skipped} linha(s) sem realce (palavras diferentes).")
    return "\n".join(out)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else SUBMISSION
    with open(path, encoding="utf-8") as f:
        submission = f.read()
    if not submission.strip():
        sys.exit(f"{path} esta vazio. Corre primeiro o agente.")
    with open(TEMPLATE, encoding="utf-8") as f:
        page = f.read()
    original = highlight_original(extract_text(PDF), submission)
    anonymized = mark_asterisks(submission.rstrip("\n"))
    page = page.replace("{{ORIGINAL}}", original)
    page = page.replace("{{ANONYMIZED}}", anonymized)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Escrito {OUTPUT}")


if __name__ == "__main__":
    main()