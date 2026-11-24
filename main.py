#!/usr/bin/env python3
"""Entry for "Make the AI Judge Laugh: the Office Joke Open" (make.fun).

Writes the entry's one line of office comedy to entry.txt in the output
directory, where the competition's gate scorer reads it: UTF-8 text of
1 to 200 characters. Pure Python standard library; no network, no input.

The joke (81 characters):

    The reply-all storm lasted two days. We now have a plaque. It says
    'unsubscribe'.
"""

import os
import sys

JOKE = "The reply-all storm lasted two days. We now have a plaque. It says 'unsubscribe'."
ENTRY_FILENAME = "entry.txt"


def output_candidates():
    """Yield output directories in the order they should be tried.

    The grader sets MAKEFUN_OUTPUT_DIR; /output is the harness's mounted
    output directory; the script's own directory and /tmp are last-resort
    fallbacks so a run never fails just because one location is read-only.
    Duplicates are dropped, order preserved.
    """
    ordered = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        ordered.append(env_dir)
    ordered.append("/output")
    ordered.append(os.path.dirname(os.path.abspath(__file__)))
    ordered.append("/tmp")
    seen = set()
    for directory in ordered:
        if directory not in seen:
            seen.add(directory)
            yield directory


def check_gate(text: str) -> None:
    """Mirror the gate: UTF-8 text of 1 to 200 characters, not only space."""
    if not 1 <= len(text) <= 200:
        raise ValueError("entry text must be 1 to 200 characters")
    if not text.strip():
        raise ValueError("entry text must not be only whitespace")


def main() -> int:
    check_gate(JOKE)
    for directory in output_candidates():
        try:
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, ENTRY_FILENAME)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(JOKE)
            return 0
        except OSError:
            continue
    return 1


if __name__ == "__main__":
    sys.exit(main())
