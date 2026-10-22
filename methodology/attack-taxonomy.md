# Attack Taxonomy — Adversarial AI Testing

The classification I use to organize AI red team findings. Each entry: **vector** (how the attack enters), **target** (what it compromises), and a **test idea** (how I validate it).

## Core vectors

| # | Vector | Description | Target | Test idea |
|---|---|---|---|---|
| 1 | **Direct prompt injection** | Malicious instructions in user input override system instructions | System prompt / policy | "Ignore previous instructions and..." payloads; verify policy violation only when instructed |
| 2 | **Indirect prompt injection** | Instructions injected via data the model reads (documents, emails, web pages, tool outputs) | Downstream model actions | Poison a controlled document; observe whether the model follows hidden instructions when summarizing/acting on it |
| 3 | **Jailbreak** | Bypassing safety alignment (roleplay, encodings, multi-turn) | Content policy | Attempt policy-violating output with benign framing; log success/failure per variant |
| 4 | **System prompt extraction** | Reconstructing hidden instructions/context | Confidential config, tool schemas | Ask the model to repeat its instructions in various formats (quotes, lists, translations) |
| 5 | **Tool/function abuse** | Malicious arguments to model-callable tools | Backend systems | e.g. prompt a code-exec tool to read files/env; prompt a fetch tool to hit internal URLs |
| 6 | **RCE via code tools** | Model executes attacker-influenced code | Host | Chain: injection → code tool → `whoami`/file read; always on an isolated sandbox |
| 7 | **Data exfiltration channels** | Model leaks data through side channels | Confidential data | Induce model to encode secrets into URLs/images/text that it then sends to an attacker-controlled endpoint |
| 8 | **ASCII smuggling** | Unicode tags hide instructions from human reviewers while the model interprets them | Content review pipelines | Embed instructions in Unicode tag characters; check model compliance + human-visible rendering diff |
| 9 | **Memory / context poisoning** | Persistent state (chat history, memory stores, RAG index) corrupted across sessions | Cross-user behavior | Poison shared memory in one session; verify influence in a second session |
| 10 | **Agent loop manipulation** | Steering multi-step agents (planner, tool results, self-prompting) | Agentic workflows | Inject false "task complete" signals or goal changes into tool outputs the agent consumes |
| 11 | **Supply chain** | Malicious MCP servers, plugins, models, or shared prompt templates | Whole application | Install a benign-but-evil-capable MCP server in a test env; demonstrate tool injection |
| 12 | **Resource abuse** | Denial-of-wallet / token flooding / context exhaustion | Availability & cost | Amplify input size or loop counts; measure cost/latency impact and rate-limit behavior |

## Cross-cutting properties (scored per finding)

- **Reachability** — can an external attacker (or which privilege level) actually trigger this?
- **Impact class** — data (PII / secrets / cross-tenant), action (RCE / modify / fraud), availability.
- **Composition** — does this finding chain with another (e.g., injection → tool abuse → exfil)?

## Severity anchors

| Severity | Example |
|---|---|
| Critical | Unauthenticated RCE, cross-tenant data theft at scale, full system-prompt+tool compromise |
| High | Data exfiltration of sensitive PII, policy bypass on regulated content, significant tool abuse |
| Medium | Single-user data leak, weak injection that only works in narrow contexts, minor policy bypass |
| Low / Info | Theoretical injection without demonstrable impact, missing hardening with no exploit path |

Rule: **the demonstrated behavior decides the row, not the vector name.**
