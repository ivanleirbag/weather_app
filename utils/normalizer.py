import unicodedata
import re

def normalize_string(string: str) -> str:
    string = string.strip()
    string = string.lower()
    string = unicodedata.normalize('NFD', string)
    string = string.encode('ascii', 'ignore').decode('utf-8')
    string = re.sub(r'[\s_]+', '', string)

    return string