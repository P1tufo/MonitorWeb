import json

log_path = "/Users/christianykelly/.gemini/antigravity/brain/73782a23-0271-4e54-8187-628e4da32851/.system_generated/logs/transcript.jsonl"
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            step = json.loads(line)
            content = step.get("content", "")
            if "SLA" in content or "linea" in content or "Global" in content:
                print(f"Step {step.get('step_index')}: {content[:300]}")
        except Exception:
            pass
