"""PDF extraction and the whole chain, with Gemini replaced by a stub."""
from agent import __main__ as cli
from agent.extraction import DEFAULT_PDF, extract_pdf
from agent.prompt import EXAMPLES


def test_extraction_keeps_text_exact(tmp_path):
    out = tmp_path / "raw.txt"
    text = extract_pdf(DEFAULT_PDF, out)
    assert out.read_bytes().decode("utf-8") == text
    assert "\r" not in text
    first = text.split("\n")[0]
    assert first.startswith("Relatório de Admissão")
    assert first.endswith(" ")  # PyMuPDF's line-end space is kept


def stub(monkeypatch, tmp_path, payload):
    monkeypatch.setattr(cli, "extract_pdf",
                        lambda pdf: extract_pdf(pdf, tmp_path / "raw.txt"))
    monkeypatch.setattr(cli, "api_key", lambda: "TESTKEY")
    monkeypatch.setattr(cli, "call_gemini", lambda *a: payload)


def run(tmp_path):
    out = tmp_path / "answer.txt"
    code = cli.main(["--prompt", str(EXAMPLES / "system_prompt.txt"),
                     "--out", str(out)])
    return code, out


def test_answer_is_written_exactly_as_returned(tmp_path, monkeypatch):
    text = "Nome: * \n  odd   spacing kept\n"
    stub(monkeypatch, tmp_path, {"candidates": [{
        "finishReason": "STOP", "content": {"parts": [{"text": text}]}}]})
    code, out = run(tmp_path)
    assert code == 0
    assert out.read_bytes().decode("utf-8") == text


def test_truncated_answer_writes_nothing(tmp_path, monkeypatch):
    stub(monkeypatch, tmp_path, {"candidates": [{
        "finishReason": "MAX_TOKENS",
        "content": {"parts": [{"text": "partial"}]}}]})
    code, out = run(tmp_path)
    assert code == 1 and not out.exists()
