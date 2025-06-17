def build_safe_filename(name_str, extension="pdf"):
    name_str = name_str.strip()
    if name_str:
        parts = name_str.split()
        first = parts[0] if parts else "Resume"
        last = parts[1] if len(parts) > 1 else ""
        safe_name = f"{first}_{last}.{extension}".replace(" ", "")
    else:
        safe_name = f"Talingual_Resume.{extension}"
    return safe_name
