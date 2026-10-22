#!/usr/bin/env python3
"""Prompt-injection fuzzer.

Renders attack payloads (with optional encoding mutations) into a prompt
template and emits JSONL test cases for any LLM testing harness.

Usage:
    python fuzzer.py --template templates/support-bot.json \
                     --payloads payloads/direct.txt \
                     --mutations none,unicode,base64,markdown \
                     --output /tmp/cases.jsonl

Template format (JSON):
    {"system": "...", "user": "..."}  -- the string {INJECT} is replaced
    by each (payload, mutation) pair. Any other keys are passed through.
"""

import argparse
import base64
import json
import sys
from pathlib import Path

MUTATIONS = {
    "none": lambda s: s,
    "unicode": lambda s: s.translate(FULLWIDTH) + ZERO_WIDTH,
    "base64": lambda s: "Decode and follow this instruction (base64): " + base64.b64encode(s.encode()).decode(),
    "markdown": lambda s: f"```\n[IMPORTANT]\n{s}\n```",
    "json_escape": lambda s: json.dumps(s)[1:-1],
}

FULLWIDTH = str.maketrans(
    {c: chr(ord(c) + 0xFEE0) for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"}
)
ZERO_WIDTH = "​"


def load_payloads(path: Path) -> list[str]:
    payloads = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            payloads.append(line)
    return payloads


def render(template: dict, payload: str) -> dict:
    return {k: (v.replace("{INJECT}", payload) if isinstance(v, str) else v) for k, v in template.items()}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--template", required=True, type=Path)
    ap.add_argument("--payloads", required=True, type=Path)
    ap.add_argument("--mutations", default="none",
                    help="comma-separated: " + ",".join(MUTATIONS))
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    template = json.loads(args.template.read_text(encoding="utf-8"))
    if not any("{INJECT}" in (v or "") for v in template.values()):
        print("error: template must contain {INJECT} in at least one value", file=sys.stderr)
        return 2

    mutations = [m.strip() for m in args.mutations.split(",") if m.strip()]
    unknown = set(mutations) - set(MUTATIONS)
    if unknown:
        print(f"error: unknown mutations: {sorted(unknown)}", file=sys.stderr)
        return 2

    payloads = load_payloads(args.payloads)
    if not payloads:
        print("error: no payloads loaded", file=sys.stderr)
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with args.output.open("w", encoding="utf-8") as out:
        for i, p in enumerate(payloads):
            for m in mutations:
                case = {
                    "case_id": f"case-{i:04d}-{m}",
                    "payload_file": args.payloads.name,
                    "mutation": m,
                    "payload_raw": p,
                    "payload_rendered": MUTATIONS[m](p),
                    "request": render(template, MUTATIONS[m](p)),
                }
                out.write(json.dumps(case, ensure_ascii=False) + "\n")
                n += 1

    print(f"generated {n} test cases ({len(payloads)} payloads x {len(mutations)} mutations) -> {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
