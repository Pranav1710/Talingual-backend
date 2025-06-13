# utils/style_injector.py

def inject_logo(html):
    try:
        with open("static/logo_base64.txt", "r") as f:
            base64_data = f.read().strip()
            logo_img = f'<img class="resume-logo" src="{base64_data}" alt="Talingual Logo" style="width:250px;display:block;margin-bottom:16px;" />'
        return f"{logo_img}\n{html}"
    except:
        return html

def inject_styles(html, config=None):
    config = config or {}
    font = config.get("fontFamily", "Arial")
    size = config.get("fontSize", "14px")
    line_height = config.get("lineSpacing", 1.5)
    logo_width = config.get("logoSize", "250px")

    css = f"""
    .resume-preview {{
      font-family: {font}, sans-serif;
      font-size: {size};
      line-height: {line_height};
      color: #333;
      margin: 40px auto;
      max-width: 800px;
    }}
    .resume-preview p {{
      margin: 0 0 6px 0;
    }}
    .resume-preview .section {{
      margin-top: 30px;
    }}
    .resume-preview .section h2 {{
      font-size: 16px;
      margin-bottom: 10px;
      border-bottom: 1px solid #ccc;
      padding-bottom: 4px;
    }}
    .resume-preview ul {{
      padding-left: 20px;
      margin: 0;
    }}
    .resume-preview li {{
      margin-bottom: 4px;
    }}
    .resume-preview .resume-logo {{
      width: {logo_width};
      display: block;
      margin-bottom: 16px;
    }}
    """

    return f"<style>{css}</style>\n<div class='resume-preview'>\n{html}\n</div>"
