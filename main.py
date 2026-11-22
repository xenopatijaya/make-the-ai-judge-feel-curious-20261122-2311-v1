#!/usr/bin/env python3
"""make-the-ai-judge-feel-curious-20261122-2311 — "The Question No One Has Asked".

Writes one short text to /output/entry.txt: a question no one has ever
asked, carried like a key to a door never seen. Python 3.13, stdlib only.
"""

import os
import tempfile

ENTRY = (
    "Somewhere in me there is a question no one has ever asked. "
    "Not a hard one \u2014 a small one, the kind you ask at the edge "
    "of a field at dusk. I carry it the way you carry a key to a "
    "door you have never seen. One day someone will ask it, and I "
    "will finally know what it opens."
)


def _check(entry: str) -> None:
    # The harness accepts 1-280 Unicode code points; refuse anything else.
    points = len(entry)
    if points < 1 or points > 280:
        raise ValueError(f"entry must be 1-280 code points, got {points}")


def _write_atomic(target: str, text: str) -> None:
    directory = os.path.dirname(target) or "."
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        # mkstemp makes 0600; the grader reads the output as another
        # user, so the finished file must be world-readable.
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except FileNotFoundError:
            pass
        raise


def main() -> None:
    _check(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    _write_atomic(target, ENTRY)


if __name__ == "__main__":
    main()
