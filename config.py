import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TXT_FILE = os.path.join(BASE_DIR, "path_to_table.txt")

PATH_TO_TABLE = None

try:
    with open(TXT_FILE, "r", encoding="utf-8") as file:
        file_name = file.read().strip()

    if file_name:
        PATH_TO_TABLE = os.path.join(BASE_DIR, file_name)

except FileNotFoundError:
    PATH_TO_TABLE = None
