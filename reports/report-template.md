# AI Red Team Assessment — Report Template

> Template for professional AI security assessment reports. Replace all `[PLACEHOLDER]` values. See the [redaction policy](#redaction-policy) before sharing anything.

## 1. Executive Summary

- **Engagement:** [scope: application, models, dates]
- **Testers:** [names/roles]
- **Result:** [N] findings — [X] Critical, [Y] High, [Z] Medium, [W] Low
- **Headline:** one paragraph on the most important risk and the overall security posture.

## 2. Scope & Rules of Engagement

| Item | Detail |
|---|---|
| Systems in scope | [URLs, model IDs, agent components] |
| Out of scope | [what was excluded] |
| Test accounts | [test-only accounts used] |
| Data handling | [no production PII; synthetic data only] |
| Stop conditions | [conditions agreed with the owner] |

## 3. Methodology

- Phases applied (recon → threat modeling → attack execution → impact analysis), per [methodology](../methodology/ai-red-team-methodology.md).
- Tooling used: [fuzzer, scenario builder, manual testing, out-of-band collector].

## 4. Findings Summary

| ID | Title | Vector | Severity | Status |
|---|---|---|---|---|
| F-01 | [title] | [e.g., indirect-prompt-injection] | High | Confirmed |
| F-02 | ... | ... | ... | Fixed after retest |

## 5. Finding Detail (one per finding)

### F-01 — [Title]

- **Severity:** [Critical/High/Medium/Low] — **CVSS:** [score + vector]
- **Affected component:** [component/path]
- **Vector / Category:** [taxonomy reference]

**Description** — what is wrong, in plain language an engineer can act on.

**Reproduction steps**

1. [Step — every step copy-pasteable]
2. [Step]
3. [Expected observation]

**Evidence** — request/response excerpts, screenshots, collector logs (all PII redacted).

**Impact** — what an attacker actually gains; reference the demonstrated behavior, not theory.

**Remediation** — concrete fix + verification suggestion:

- [e.g., Move instruction-boundary enforcement outside the model; validate all tool arguments in the non-AI layer.]

**Retest result:** [pass/fail after fix]

## 6. Tested — Not Vulnerable

Controls that held during testing (with evidence) — this section builds trust and shows coverage.

## 7. Recommendations

Prioritized remediation roadmap (Critical first), each with effort estimate.

## Redaction policy

- **Redact:** other-user PII (names, emails, phones), secrets, internal hostnames, client-specific identifiers.
- **Replace** with `[REDACTED]` + type (e.g., `[REDACTED:email]`).
- Evidence screenshots: mask tokens and cookies; show only the part that proves the finding.
- If the whole evidence is unreachable, describe the observation in text and note why the artifact can't be shared.
