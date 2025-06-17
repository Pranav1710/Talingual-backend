import os
import json

def build_talingual_gpt_messages(resume_text: str, notes: str = ""):
    # ✅ Static backend formatting enforcement
    static_rules = """
You are a resume formatting assistant for Talingual.
Strictly return HTML only — no Markdown, no triple backticks, no code blocks.
Only use the following HTML tags: <p>, <ul>, <li>, <h2>, <div class="section">.
Your output will be parsed and exported to PDF/DOCX. Keep it clean and semantically structured.
"""

    # ✅ Load the JSON content schema
    json_path = os.path.join("utils", "prompts", "talingual_system_prompt.json")
    with open(json_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    schema_text = json.dumps(schema, indent=2)

    # Combine system prompt
    system_prompt = f"{static_rules.strip()}\n\nFormatting Schema:\n{schema_text}"

    # Resume and notes
    user_prompt = f"Here is the raw resume content:\n\n{resume_text}"
    if notes.strip():
        user_prompt += f"\n\nRecruiter Notes:\n{notes.strip()}"

    return [
        { "role": "system", "content": system_prompt },
        { "role": "user", "content": user_prompt }
    ]
