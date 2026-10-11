"""Check that submission.txt keeps the word count of every original line.

Usage (from submission/):
    python3 check_submission.py

Compares raw_uncensored_document.txt with submission.txt, ignoring empty
lines. Exit code 0 when every line has the same number of words.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def lines(path):
    text = path.read_text(encoding="utf-8")
    return [line for line in text.splitlines() if line.strip()]


def main() -> int:
    original = lines(HERE / "raw_uncensored_document.txt")
    answer = lines(HERE / "submission.txt")
    if not answer:
        print("submission.txt is empty")
        return 1
    if len(original) != len(answer):
        print(f"line count differs: {len(original)} vs {len(answer)}")
        return 1
    bad = 0
    for number, (a, b) in enumerate(zip(original, answer), 1):
        if len(a.split()) != len(b.split()):
            bad += 1
            print(f"line {number}: {len(a.split())} words -> "
                  f"{len(b.split())}")
            print(f"  original: {a.strip()}")
            print(f"  answer:   {b.strip()}")
    masked = sum(line.count("*") for line in answer)
    print(f"{len(original) - bad} of {len(original)} lines aligned, "
          f"{masked} asterisks")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
