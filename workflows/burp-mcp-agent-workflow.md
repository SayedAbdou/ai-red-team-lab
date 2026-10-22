# AI-Agent Web Security Workflow (Burp Suite over MCP)

A battle-tested design for orchestrating coding agents (Claude Code / OpenCode) with Burp Suite over MCP to automate security analysis — traffic ingestion, auth-flow reconstruction, differential vulnerability testing, and evidence-backed reporting.

## Architecture

```
Browser traffic ──▶ Burp Suite (proxy) ──MCP──▶ Coding agent
                                                │  skills:
                                                │  • ingest & parse history
                                                │  • reconstruct auth flows
                                                │  • differential vuln tests
                                                │  • evidence + report
                                                ▼
                                           workspace/ (JSONL evidence, reports)
```

## Core MCP tools used

| Tool | Purpose |
|---|---|
| `get_proxy_http_history` | Pull captured traffic (paginated) |
| `send_http1_request` / `send_http2_request` | Replay/modify requests (Repeater-style) |
| `create_repeater_tab` | Hand off requests to the human in Burp UI |
| `get_scanner_issues` | Correlate with Burp Scanner results |

## The loop (from real sessions)

1. **Ingest** — pull proxy history in pages; parse into structured records (method, host, path, params, cookies, status).
2. **Map** — group endpoints into an attack-surface table; extract tokens (CSRF, session), auth endpoints, state-changing actions.
3. **Reconstruct auth** — replay the full login chain step-by-step (OAuth `form_post`, state/nonce, session cookies), threading every `Set-Cookie` into the next request.
4. **Differential test** — for each candidate: baseline request → modified request → compare status/body/timing. A finding needs a demonstrated delta.
5. **Report** — only evidence-backed findings; separate "tested, not vulnerable" and hardening notes.

## Hard-won design rules

These are failures I hit and turned into rules:

1. **Parse defensively.** Tool layers truncate large outputs (~5 KB/record). Build a lenient, per-record parser that survives truncation — never trust the transport.
2. **Thread session state.** Targets that rotate session tokens on every response invalidate cookie replays. Always chain each response's `Set-Cookie` into the next request; never parallelize against a rolling session.
3. **Detect challenge walls early.** WAFs (e.g., Cloudflare managed challenges) fingerprint non-browser clients. Detect the challenge response, then pivot: browser-assisted validation for challenge-gated paths, agent replay for the rest.
4. **Respect state-machine checks.** "Page expired" style server-side validation means the token alone isn't the whole story — replay must include the exact page-state sequence.
5. **Stop before side effects.** Never let automation advance real transactions (payments, deletions). The agent's permission model must gate irreversible actions.

## Repo layout for a campaign

```
workspace/<target>/
├── history-YYYYMMDD.json      # exported proxy history
├── surface.md                 # attack-surface table
├── auth-flow.md               # reconstructed auth chain
├── tests/                     # one file per test: baseline + variant + verdict
└── report.md                  # findings + tested-not-vulnerable + notes
```

## Extending to an autonomous stack

Pair this with an autonomous pentest agent (e.g., Strix) on a VPS: point the agent's traffic at Burp's proxy so *every* request it makes lands in the same history — one brain (the coding agent), one source of truth (Burp), one workspace. Full lab design: [vps-pentest-lab.md](vps-pentest-lab.md).
