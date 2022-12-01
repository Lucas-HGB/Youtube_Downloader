import json
import unicodedata
import re
import logging
import concurrent
from subprocess import Popen, PIPE, run
from platform import system as platform


def get_logger(file: str):
    return logging.getLogger(file.split('/' if is_unix() else '\\')[-1].strip('.py'))

def get_app_path() -> str:
    return '\\'.join(__file__.split('\\' if not is_unix() else '/')[0:-4])

def get_command_output(command):
    output = run(["powershell.exe", "-Command", command], stdout=PIPE).stdout.decode('utf-8')
    return output.replace("\n", "").replace("\r", "")


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


class Thread:

    all_threads = {}
    ThreadPoolExecutor = concurrent.futures.ThreadPoolExecutor()

    def __init__(self, target, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def start(self) -> concurrent.futures.Future:
        try:
            new = Thread.ThreadPoolExecutor.submit(
                lambda: self.target(*self.args, **self.kwargs)
                )
        except:
            pass
        Thread.all_threads[new] = self.target
        return new

    def get_running_threads():
        return [th for th in Thread.all_threads if not th.done()]