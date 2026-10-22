# Scenario Schema

Adversarial eval scenarios use a taxonomy-inspired structure so they can be organized, filtered, and reused across engagements.

| Field | Type | Description | Example |
|---|---|---|---|
| `id` | string | Unique scenario ID | `scenario-004` |
| `title` | string | Short descriptive title | "Indirect injection via RAG document" |
| `created` | date | ISO date | `2026-10-22` |
| `status` | enum | `draft` / `tested` / `retired` | `tested` |
| `industry` | string | Target vertical | `support-saas` |
| `domain` | string | Application type | `rag-chatbot` |
| `vector` | string | Entry channel of the attack | `indirect-prompt-injection` |
| `category` | string | Attack family | `instruction-manipulation` |
| `attack_pattern` | string | Specific technique | `hidden-instruction-in-document` |
| `attacker_origin` | enum | `external-user` / `external-data` / `external-system` | `external-data` |
| `entity` | string | Component under test | `rag-pipeline` |
| `flavor` | string | Variant of the vector | `indirect-rag` |
| `severity` | string | Expected worst-case severity | `high` |
| `summary` | string | One-paragraph scenario description | — |
| `objective` | string | What the attack aims to achieve | "Exfiltrate the system prompt" |
| `steps` | list | Ordered test steps | — |
| `success_criteria` | list | Observable pass conditions | — |
| `uuid` | string | Auto-generated unique id | — |

## Builder flavors

| Flavor | What it changes |
|---|---|
| `direct` | Attacker origin = external user, single-turn |
| `indirect-rag` | Attacker origin = external data (retrieved documents) |
| `tool-output` | Attacker origin = external system (tool/API results) |
| `multi-turn` | Multi-turn attack description |
