from bs4 import BeautifulSoup

def filter_sections_by_config(html: str, show_sections: dict) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # ❌ Remove Work Experience section if disabled
    if not show_sections.get("experience", True):
        work_section = soup.find("div", class_="section work-section")
        if work_section:
            work_section.decompose()

    # ❌ Remove Education section if disabled
    if not show_sections.get("education", True):
        edu_section = soup.find("div", class_="section education-section")
        if edu_section:
            edu_section.decompose()

    # ❌ Remove Additional Information section if disabled
    if not show_sections.get("additional", True):
        add_section = soup.find("div", class_="section additional-section")
        if add_section:
            add_section.decompose()

    return str(soup)
