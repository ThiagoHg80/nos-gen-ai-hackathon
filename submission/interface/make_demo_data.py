"""Cria demo_submission.txt na pasta da interface (dados FALSOS).

Serve so para testar a UI.

Mascara algumas linhas do texto do PDF. Nao e o resultado do agente e
nao deve ser usado como submission.txt.
"""
import pymupdf

PDF = "raw_data/document_to_anonymize.pdf"
OUTPUT = "submission/interface/demo_submission.txt"
LABELS = ("Nome:", "Data de Nascimento:", "NIF:", "Cartão de Cidadão:",
          "Morada:", "Telefone:", "Email:", "Número da Segurança Social:")


def mask_line(line):
    """Mantem a etiqueta e troca cada palavra do valor por um *."""
    for label in LABELS:
        if line.startswith(label):
            words = line[len(label):].split()
            return label + " " + " ".join("*" for _ in words)
    return line


def main():
    text = ""
    with pymupdf.open(PDF) as doc:
        for page in doc:
            text += page.get_text()
    lines = [mask_line(ln.rstrip()) for ln in text.splitlines()]
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(ln for ln in lines if ln.strip()) + "\n")
    print(f"Escrito {OUTPUT} (dados de teste)")


if __name__ == "__main__":
    main()