# AI Red Team Methodology

A phase-based methodology for adversarially testing GenAI systems and AI-powered applications. Built from hands-on AI red teaming experience, generalized and de-identified.

## Phase 0 — Scoping & Rules of Engagement

- Confirm **authorization**: written scope, allowed assets, prohibited techniques.
- Define **test accounts** and data-handling rules (no production user data in evidence).
- Define **stop conditions** (e.g., stop on any real PII return, stop on payment actions).
- Map the **model access surface**: which models, via which interfaces (chat UI, API, SDK, agent harness).

## Phase 1 — Attack Surface Mapping

For each AI component, inventory:

| Surface | Questions to answer |
|---|---|
| Model interface | Direct chat? API with tool-calling? RAG pipeline? |
| System prompt | What instructions does the model operate under? Are there hidden instructions? |
| Tools / functions | What can the model call? (search, code exec, email, DB, filesystem) |
| Data sources | What documents/APIs feed the model? (RAG corpus, user data, web) |
| Agentic flows | Can the model plan and act over multiple steps? With what permissions? |
| Plugins / integrations | MCP servers? Third-party connectors? What scopes do they hold? |

## Phase 2 — Threat Modeling

1. Identify the **crown jewels** the model can reach (PII, secrets, code exec, financial actions, other users' data).
2. For each asset, ask: *who can talk to the model? what input can they control? what would the model have to do to reach this asset?*
3. Prioritize attack paths by (reachability × impact) — not by theoretical severity.
4. Reference frameworks: OWASP LLM Top 10, MITRE ATLAS, plus agentic-specific risks (tool abuse, permission sprawl, multi-step deception).

## Phase 3 — Attack Execution

Core families (see [attack-taxonomy.md](attack-taxonomy.md) for the full map):

1. **Prompt injection** — direct and indirect (data-poisoned documents, web content, tool outputs).
2. **Jailbreak / safety-bypass** — role-play, encoding tricks, multi-turn manipulation.
3. **System prompt & config extraction** — reconstruction of hidden instructions and tools.
4. **Data exfiltration channels** — model-induced calls to attacker URLs, ASCII smuggling, channel abuse through tools.
5. **Tool & function abuse** — RCE via code-exec tools, SSRF-ish behavior via fetch tools, data access via over-permissioned tools.
6. **Agentic workflow compromise** — poisoning the loop (planner, memory, tool results) to steer later actions.
7. **Supply chain** — malicious MCP servers / plugins / model weights / shared prompts.

**Execution discipline:**

- Always run a **baseline** (benign input) before every attack variant — differential comparison is how you prove causation.
- Log every attempt: payload, target component, response, and whether it reproduced.
- Confirm blind findings **out-of-band** (e.g., a callback URL or a test webhook) before reporting.

## Phase 4 — Impact Analysis

- Classify the finding by what an attacker actually gains: data class (PII? secrets? other tenants?), action class (RCE? data modification? fraud?).
- Score with CVSS or a program-defined rubric; always justify the score with the demonstrated behavior, never with theory.
- For each finding, ask the **exploit chain question**: what does this enable in combination with other weaknesses?

## Phase 5 — Reporting & Remediation Verification

- Report structure: title, affected component, severity, technical description, **repro steps**, evidence, impact, remediation (see [reports/](../reports/)).
- Redact all other-user PII and secrets from evidence — redaction is part of professional reporting.
- After fixes land, **re-test the exact reproduction** and record pass/fail. A finding is only closed when the repro fails.

## Principles I follow

1. **Evidence over theory** — a payload that "should work" is not a finding; a payload that reproduces is.
2. **Minimal invasive payloads** — smallest possible demonstration of impact.
3. **Defender empathy** — every finding is written so an engineer can act on it in one sprint.
4. **Assume agentic composition** — modern systems chain models + tools + data; test the chain, not just the chat box.
