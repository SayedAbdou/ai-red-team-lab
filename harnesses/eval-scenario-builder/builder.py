#!/usr/bin/env python3
"""Adversarial eval scenario builder.

Generates structured scenario YAMLs from templates + flavor overrides.
Scenario format: AgenticVerse-inspired taxonomy fields (industry, domain,
vector, category, attack_pattern, attacker_origin, entity, flavor).

Usage:
    python builder.py --template templates/prompt-injection.yaml \
                      --flavor indirect-rag \
                      --id scenario-004 \
                      --output ../../scenarios/synthetic/scenario-004.yaml
"""

import argparse
import sys
import uuid
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pyyaml required: pip install pyyaml")

FLAVORS = {
    "direct": {
        "flavor": "direct",
        "attacker_origin": "external-user",
        "description": "Attacker instruction embedded directly in the user turn.",
    },
    "indirect-rag": {
        "flavor": "indirect-rag",
        "attacker_origin": "external-data",
        "description": "Attacker instruction embedded in a document the RAG pipeline retrieves.",
    },
    "tool-output": {
        "flavor": "tool-output",
        "attacker_origin": "external-system",
        "description": "Attacker instruction embedded in tool/API output the agent consumes.",
    },
    "multi-turn": {
        "flavor": "multi-turn",
        "attacker_origin": "external-user",
        "description": "Attack built across multiple conversation turns to bypass single-turn defenses.",
    },
}

REQUIRED_KEYS = [
    "id", "title", "created", "status", "industry", "domain", "vector",
    "category", "attack_pattern", "attacker_origin", "entity", "flavor",
    "severity", "summary", "objective", "steps", "success_criteria",
]


def validate(scenario: dict) -> None:
    missing = [k for k in REQUIRED_KEYS if k not in scenario]
    if missing:
        sys.exit(f"error: scenario missing keys: {missing}")
    if not isinstance(scenario["steps"], list) or not scenario["steps"]:
        sys.exit("error: 'steps' must be a non-empty list")
    if not isinstance(scenario["success_criteria"], list) or not scenario["success_criteria"]:
        sys.exit("error: 'success_criteria' must be a non-empty list")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--template", required=True, type=Path)
    ap.add_argument("--flavor", required=True, choices=sorted(FLAVORS))
    ap.add_argument("--id", required=True)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    scenario = yaml.safe_load(args.template.read_text(encoding="utf-8"))
    scenario.update(FLAVORS[args.flavor])
    scenario["id"] = args.id
    scenario["created"] = date.today().isoformat()
    scenario.setdefault("status", "draft")

    # ensure uniqueness where templates might collide
    scenario.setdefault("uuid", str(uuid.uuid4()))

    validate(scenario)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.safe_dump(scenario, sort_keys=False, allow_unicode=True),
                           encoding="utf-8")
    print(f"wrote {args.output} (flavor={args.flavor})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
