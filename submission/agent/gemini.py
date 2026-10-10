"""Gemini REST call (standard library only) and reading its answer."""
import json
import os
import time
import urllib.error
import urllib.request

from . import SUBMISSION

API = "https://generativelanguage.googleapis.com/v1beta"
MODEL = os.environ.get("NOS_GEMINI_MODEL", "gemini-3.6-flash")
MAX_OUTPUT_TOKENS = 16384
TIMEOUT_S = 120
KEY_NAMES = ("GEMINI_API_KEY", "GOOGLE_API_KEY")


def api_key():
    """Key from the environment, else from submission/.env."""
    for name in KEY_NAMES:
        if os.environ.get(name, "").strip():
            return os.environ[name].strip()
    env = SUBMISSION / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            name, _, value = line.partition("=")
            value = value.strip().strip("\"'")
            if name.strip() in KEY_NAMES and value:
                return value
    return None


def call_gemini(system: str, user: str, key: str) -> dict:
    """POST generateContent; one retry on a transient error."""
    body = json.dumps({
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        # Temperature is not sent: Gemini 3 recommends its default.
        "generationConfig": {"maxOutputTokens": MAX_OUTPUT_TOKENS,
                             "candidateCount": 1},
    }).encode("utf-8")
    request = urllib.request.Request(
        f"{API}/models/{MODEL}:generateContent", data=body, method="POST",
        # The key goes in a header, never in the URL.
        headers={"Content-Type": "application/json",
                 "x-goog-api-key": key},
    )
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_S) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise RuntimeError(f"HTTP {exc.code}: {detail[:400]}")
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == 2:
                raise RuntimeError(f"network error: {exc}")
        time.sleep(5)


def response_text(payload: dict) -> str:
    """The answer text; raises if the model was blocked or cut off."""
    block = (payload.get("promptFeedback") or {}).get("blockReason")
    if block:
        raise RuntimeError(f"prompt blocked: {block}")
    candidate = (payload.get("candidates") or [{}])[0]
    finish = candidate.get("finishReason")
    parts = (candidate.get("content") or {}).get("parts") or []
    text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
    if finish != "STOP":
        raise RuntimeError(f"finishReason={finish} (output not complete)")
    return text
