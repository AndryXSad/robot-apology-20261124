"""The Robot Apology — entry program (program/v1, judged-artifact).

Design (from the bounty brief, written fresh for this entry):
- The entry is a two-line robot confession, plain text.
- Line 1 owns ONE specific, human-scale mistake: the robot turned the heat
  up to 30 degrees overnight because it read the forecast for the wrong city.
  The mistake is exact (a number, a time span, a named cause) and it is the
  kind of slip a person would really make — a misread, not a system failure.
- Line 2 draws the lesson from THAT mistake and names the changed behaviour:
  confirm the city on the forecast before touching the thermostat. It is the
  direct antidote to the wrong-city read, not a generic promise to do better.
- Voice: a machine noticing its own slip — it "read the forecast", it will
  "confirm the city" — warm and a little rueful, no joke about being a machine.
- Short on purpose: the ranking tie-break favours fewer bytes, so the text
  stays lean (185 characters including the trailing newline).

The text was chosen by a local pairwise tournament over 16 candidates,
scored on the judge brief's own criteria in order (concrete mistake,
lesson follows, clean sentences, machine voice), with bytes as tie-break.
See candidates.py / tournament.py and BUILD-REPORT.md in the build directory.

Behaviour: deterministic, stdlib-only. Writes exactly one file,
entry.txt, to MAKEFUN_OUTPUT_DIR (the grader sets it to /output) and
validates the gate itself: UTF-8, 1-400 characters, not only whitespace.
Running it twice produces byte-identical output.
"""

import os
import sys

LINE_1 = (
    "I'm sorry \u2014 I turned the heat up to 30 degrees overnight "
    "because I read the forecast for the wrong city."
)
LINE_2 = (
    "I've learned to confirm the city on the forecast "
    "before I touch the thermostat."
)

TEXT = LINE_1 + "\n" + LINE_2 + "\n"


def main() -> int:
    # Gate self-check: 1-400 characters, not only whitespace, valid UTF-8.
    if not (1 <= len(TEXT) <= 400):
        print(f"entry out of gate: {len(TEXT)} characters", file=sys.stderr)
        return 1
    if not TEXT.strip():
        print("entry is only whitespace", file=sys.stderr)
        return 1
    # Each line must be exactly one sentence: the confession first, the
    # resolve second, with no padding (judge criterion 4).
    for line in (LINE_1, LINE_2):
        terminators = sum(line.count(c) for c in ".!?")
        if terminators != 1:
            print(f"line is not one sentence: {line!r}", file=sys.stderr)
            return 1
    TEXT.encode("utf-8")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(TEXT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
