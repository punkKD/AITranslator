import re

def parse_translation_response(raw_text: str) -> dict:
    """
    Splits a Cohere response formatted as:
        **Translation:**
        ...
        **Translator's Notes:**
        ...
    into separate translation and notes strings.
    """
    parts = re.split(r"\*\*(.+?):\*\*", raw_text.strip())
    sections = {}
    for i in range(1, len(parts) - 1, 2):
        header = parts[i].strip().lower()
        content = parts[i + 1].strip()
        sections[header] = content
    # if "translation" not in sections:
    #     raise ValueError("Missing 'Translation' section in the response.")
    # else:
    translation = sections.get("translation", "")
    notes = sections.get("translator's notes", "")
    print(f"Translation: {translation}, Notes: {notes}")
    return translation, notes

    # # Collapse the translation's line breaks into a single readable string
    # translation = " ".join(line.strip() for line in translation.splitlines() if line.strip())

