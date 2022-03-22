import json
import unicodedata
import re
from platform import system as platform





def read_from_json(file) -> dict:
    with open(file, "r") as opened_file:
        return json.load(opened_file)
       

def write_to_json(file, data) -> None:
    with open(file, "w", encoding='utf-8') as file_opened:
        json.dump(data, file_opened, indent=4, ensure_ascii=False)


def is_unix() -> bool:
    return platform().lower() == "linux"


def remove_invalid_char(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')