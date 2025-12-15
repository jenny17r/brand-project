import json
import re

def extract_json(text: str):
    # Remove markdown
    cleaned = text.replace("```json", "").replace("```", "").strip()

    # Try direct JSON
    try:
        return json.loads(cleaned)
    except:
        pass

    # Regex fallback
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        json_str = match.group()
        json_str = json_str.replace("'", '"')
        return json.loads(json_str)

    raise ValueError("Invalid JSON from LLM")

