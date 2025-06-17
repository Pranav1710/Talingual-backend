
def inject_logo(html, show_logo=True):
    """
    Injects the Talingual logo as an <img> tag above the HTML content,
    if show_logo is True. Style is applied separately via inject_styles().
    """
    if not show_logo:
        return html
    try:
        with open("static/logo_base64.txt", "r") as f:
            base64_data = f.read().strip()
            logo_img = f'<img class="resume-logo" src="{base64_data}" alt="Talingual Logo" />'
        return f"{logo_img}\n{html}"
    except Exception as e:
        print("[LOGO ERROR]", e)
        return html


def inject_styles(html, config=None):
    config = config or {}
    font = config.get("fontFamily", "Arial")
    raw_px = config.get("fontSize", "13px").replace("px", "")
    try:
        px_val = float(raw_px)
        preview_px = round(px_val * 1.333, 2)
        size = f"{preview_px}px"
    except:
        size = "17.33px"

    line_height = config.get("lineSpacing", 1.4)
    logo_width = config.get("logoSize", "250px")

    css = f"""
    .resume-preview {{
      font-family: {font}, sans-serif;
      font-size: {size};
      line-height: {line_height};
      color: #000;
      max-width: 800px;
      margin: 40px auto;
    }}

    /* PERSONAL INFO */
    .resume-preview .info-field {{
      margin: 0 0 4px 0;
    }}

    /* PROFILE */
    .resume-preview .profile-paragraph {{
      margin: 12px 0 8px 0;
    }}
    .resume-preview .profile-paragraph-note {{
      margin: 0 0 14px 0;
    }}

    /* SECTION HEADINGS */
    .resume-preview .section {{
      margin-top: 26px;
    }}
    .resume-preview .section h2 {{
      font-size: 15px;
      font-weight: bold;
      margin: 0 0 10px 0;
    }}

    /* WORK EXPERIENCE */
    .resume-preview .work-dates {{
      margin: 12px 0 2px 0;
      font-weight: normal;
    }}
    .resume-preview .work-title {{
      margin: 0 0 8px 0;
      font-weight: normal;
    }}
    .resume-preview .work-bullet-list,
    .resume-preview .edu-bullet-list,{{
      margin: 0 0 8px 0;
      padding-left: 20px;
    }}
    .resume-preview .work-bullet,
    .resume-preview .edu-bullet{{
      margin-bottom: 5px;
    }}

    /* EDUCATION */
    .resume-preview .edu-line-2 {{
      margin: 4px 0;
    }}
     .resume-preview .edu-line-1{{
      margin: 12px 0 4px 0;
     }}

    /* ADDITIONAL INFO */
    .resume-preview .add-list {{
      padding-left: 20px;
      margin-top: 8px;
    }}
    .resume-preview .add-bullet {{
      margin-bottom: 5px;
    }}

    /* LOGO */
    .resume-preview .resume-logo {{
      width: {logo_width};
      display: block;
      margin-bottom: 16px;
    }}
    """
    return f"<style>{css}</style>\n<div class='resume-preview'>\n{html}\n</div>"
