import glob
from pathlib import Path

BOM_UTF8 = b'\xef\xbb\xbf'

def is_utf8_with_bom(file_path):
    with open(file_path, 'rb') as file:
        bom = file.read(3)
    return bom == BOM_UTF8

def save_as_utf8_with_bom(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    with open(file_path, 'w', encoding='utf-8-sig') as file:
        file.write(content)

for txt_file in glob.iglob("**/*.txt", recursive=True):
    if is_utf8_with_bom(txt_file):
        continue
    utf8_file = Path(txt_file).with_suffix('.txt')
    save_as_utf8_with_bom(utf8_file)
    print(f"File '{txt_file}' has been saved as UTF-8 with BOM in '{utf8_file}'.")
