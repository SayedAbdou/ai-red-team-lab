# AI Red Team Lab

> Methodology, harnesses, and workflows for adversarial testing of AI systems — by [Sayed Abdou](https://www.sayedabdou.com), AI Red Team Expert (São Paulo, Brazil).

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](harnesses/)
[![CI](https://github.com/sayedabdou/ai-red-team-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/sayedabdou/ai-red-team-lab/actions)

**⚠️ Ethics & confidentiality notice:** All content in this repository is **original, synthetic, and de-identified**. It contains no client data, no client prompts, and no internal tooling from any employer or engagement. Use it only on systems you own or are explicitly authorized to test.

## What's inside

| Directory | Purpose |
|---|---|
| [`methodology/`](methodology/) | AI red team methodology, attack taxonomy, and agentic-workflow assessment guides |
| [`harnesses/`](harnesses/) | Reusable, generic tooling: prompt-injection fuzzer, adversarial eval scenario builder, LLM app security checklist |
| [`scenarios/`](scenarios/) | Synthetic adversarial test scenarios (AgenticVerse-style YAML) |
| [`reports/`](reports/) | Professional red-team report template + redacted sample finding |
| [`workflows/`](workflows/) | AI-agent orchestration: driving Burp Suite over MCP for automated web security testing, and a VPS lab design (Strix + Burp + coding agents) |

## Quick start

```bash
# Prompt-injection fuzzer
cd harnesses/prompt-injection-fuzzer
python fuzzer.py --template templates/support-bot.json \
                 --payloads payloads/direct.txt \
                 --mutations unicode,base64,markdown \
                 --output /tmp/test-cases.jsonl

# Adversarial eval scenario builder
cd harnesses/eval-scenario-builder
python builder.py --template templates/prompt-injection.yaml \
                  --flavor indirect-rag \
                  --output ../scenarios/synthetic/my-scenario.yaml
```

## Why this repo exists

I work as an AI Red Team Expert, adversarially testing GenAI systems and agentic applications — prompt injection, unsafe tool usage, data exfiltration channels, and everything in between. I also automate security workflows with coding agents (Burp Suite over MCP, autonomous pentest orchestration).

This repository is my public, portable proof of that work: the methodology I apply, the tooling patterns I reuse, and the automation designs I build — reconstructed from scratch in synthetic form.

## Contact

- Website: [sayedabdou.com](https://www.sayedabdou.com)
- GitHub: [@sayedabdou](https://github.com/sayedabdou)
- Email: work@sayedabdou.com

## License

MIT — see [LICENSE](LICENSE). Please attribute when reusing, and keep testing authorized.
