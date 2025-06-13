import os

def build_talingual_gpt_messages(resume_text: str, notes: str = ""):
    # Load system prompt from txt file
    prompt_path = os.path.join("utils", "prompts", "talingual_system_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read().strip()

    user_prompt = f"""Here is the raw resume content. Please format it into clean, structured HTML (no markdown, no code block fences, no triple backticks) as per Talingual CV standards.

{resume_text}
"""
    if notes.strip():
       user_prompt += f"""
Recruiter Notes:
{notes.strip()}
"""
    return [
        { "role": "system", "content": system_prompt },
        { "role": "user", "content": user_prompt }
    ]
