# Eval Scenario Builder

Generates structured, reusable adversarial scenarios from templates + flavor overrides. All output goes to `scenarios/synthetic/` (synthetic content only).

## Usage

```bash
python builder.py --template templates/prompt-injection.yaml \
                  --flavor indirect-rag \
                  --id scenario-004 \
                  --output ../../scenarios/synthetic/scenario-004.yaml
```

See [schema.md](schema.md) for the field reference.
