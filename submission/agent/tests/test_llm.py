"""Model selection and reading replies, without network calls."""
import pytest
from langchain_core.messages import AIMessage

from agent import llm


def test_unfinished_reply_is_refused():
    done = AIMessage(content=[{"type": "thinking", "thinking": "hm"},
                              {"type": "text", "text": "Nome: *"}],
                     response_metadata={"finish_reason": "STOP"})
    assert llm.answer_text(done) == "Nome: *"  # thinking is dropped
    for finish in ("MAX_TOKENS", "length", None):
        cut = AIMessage(content="Nome:",
                        response_metadata={"finish_reason": finish})
        with pytest.raises(RuntimeError):
            llm.answer_text(cut)


def test_gemini_needs_a_key(monkeypatch):
    monkeypatch.setattr(llm, "api_key", lambda: None)
    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        llm.get_llm("gemini")


def test_models_leave_temperature_unset(monkeypatch):
    monkeypatch.setattr(llm, "api_key", lambda: "TESTKEY")
    assert llm.get_llm("gemini").temperature is None
    local = llm.get_llm("local", base_url="http://127.0.0.1:1/v1")
    assert local.temperature is None and local.model_name == "local"
