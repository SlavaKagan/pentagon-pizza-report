
import re
from urllib.parse import unquote

def extract_place_name_from_url(url: str) -> str:
    # זיהוי תקני של /place/.../
    match = re.search(r'/place/([^/]+)/?', url)
    if match:
        name = match.group(1)
        name = name.replace('+', ' ')
        name = unquote(name)
        # מחיקת תווים שאינם אותיות/רווחים/מספרים
        name = re.sub(r'[^A-Za-zא-ת0-9\'" ]', '', name).strip()
        return name
    return ""
