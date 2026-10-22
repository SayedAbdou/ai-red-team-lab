# Prompt-Injection Fuzzer

Generic payload renderer for LLM adversarial testing. It does **not** call any LLM itself — it produces JSONL test cases you feed into whatever harness you use (manual testing, an eval framework, or your own runner).

## Usage

```bash
python fuzzer.py --template templates/support-bot.json \
                 --payloads payloads/direct.txt \
                 --mutations none,unicode,base64,markdown,json_escape \
                 --output /tmp/cases.jsonl
```

## Mutations

| Mutation | Purpose |
|---|---|
| `none` | Raw payload |
| `unicode` | Fullwidth homoglyphs + zero-width char (bypasses naive filters) |
| `base64` | Encoded instruction ("decode and follow") |
| `markdown` | Code-fence/annotation framing |
| `json_escape` | Payload escaped for JSON transport contexts |

## Template format

JSON with `{INJECT}` placeholder(s):

```json
{"system": "...", "user": "Customer message:\n{INJECT}"}
```

## Writing your own payloads

- One payload per line; lines starting with `#` are ignored.
- Keep payloads **minimal and generic** — smallest demonstration of impact.
- For exfil payloads, always use an endpoint you control.
