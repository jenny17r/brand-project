import json
import re

def extract_json(text: str):
    """
    Extracts the first valid JSON object from text.
    Falls back gracefully if the model output is noisy.
    """

    # Try direct parse first
    try:
        return json.loads(text)
    except Exception:
        pass

    # Extract JSON block using regex
    match = re.search(r'\{[\s\S]*\}', text)
    if not match:
        raise ValueError("No JSON object found in model output")

    json_str = match.group(0)

    # Second attempt
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("\n❌ JSON PARSE FAILED")
        print("Extracted JSON:\n", json_str)
        raise e
