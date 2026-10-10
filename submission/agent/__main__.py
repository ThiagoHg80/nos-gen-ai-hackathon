"""Anonymization agent.

    PDF -> raw_uncensored_document.txt -> prompt -> Gemini -> answer file

One Gemini call returns the whole document with personal data masked.
The answer is written exactly as returned. The agent does not check or
score it: use benchmark/ for that.

Usage (from submission/):
    python -m agent                          # writes submission.txt
    python -m agent --prompt benchmark/prompt_examples/system_prompt.txt
    python -m agent --pdf input.pdf --out answer.txt
    python -m agent --dry-run                # show the prompt, no call

Exit code: 0 answer written, 1 API failure, 2 not run.
"""
import argparse
import sys
from pathlib import Path

from langchain_core.runnables import RunnablePassthrough

from . import SUBMISSION
from .extraction import DEFAULT_PDF, extract_pdf
from .gemini import MODEL, api_key, call_gemini, response_text
from .prompt import DEFAULT_PROMPT, build_messages, load_prompt

DEFAULT_OUT = SUBMISSION / "submission.txt"

# Each step adds one key to the state dict and passes the rest along.
prepare = (
    RunnablePassthrough.assign(document=lambda s: extract_pdf(s["pdf"]))
    | RunnablePassthrough.assign(
        messages=lambda s: build_messages(s["system"], s["document"]))
)
answer = (
    RunnablePassthrough.assign(
        payload=lambda s: call_gemini(*s["messages"], s["key"]))
    | RunnablePassthrough.assign(output=lambda s: response_text(s["payload"]))
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT,
                        help="instructions file (default: submission/"
                        "prompt.txt)")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="answer file (default: submission/"
                        "submission.txt)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    try:
        system = load_prompt(args.prompt)
    except ValueError as exc:
        print(exc)
        return 2
    state = prepare.invoke({"pdf": args.pdf, "system": system})
    system, user = state["messages"]
    if args.dry_run:
        print(system + "\n" + user[:200] + "...")
        print(f"\nmodel {MODEL}, {len(system) + len(user)} prompt chars")
        return 0

    key = api_key()
    if not key:
        print("no GEMINI_API_KEY in the environment or submission/.env")
        return 2
    try:
        state = answer.invoke({**state, "key": key})
    except RuntimeError as exc:
        print("FAILED: " + str(exc).replace(key, "[KEY]"))
        return 1

    args.out.write_bytes(state["output"].encode("utf-8"))
    print(f"wrote {args.out}")
    if (args.out.resolve() == DEFAULT_OUT
            and args.prompt.resolve() != DEFAULT_PROMPT):
        # prompt.txt must hold the prompt that produced submission.txt.
        DEFAULT_PROMPT.write_bytes(system.encode("utf-8"))
        print(f"wrote {DEFAULT_PROMPT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
