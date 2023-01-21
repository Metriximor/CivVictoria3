import bz2
from collections import defaultdict
from pathlib import Path
import pickle

UTF_8_BOM = 'utf-8-sig'

def load_file_into_string(path: str):
    print(f"Loading from {path}")
    string = ""
    file = Path(path)
    with file.open(encoding=UTF_8_BOM) as f:
        string = f.read()
    return string

def load_province_color_maps(path: str):
    if not Path(path).is_file:
        return Exception(f"{path} does not exist")
    print(f"Loading province color map at {path}")
    with bz2.BZ2File(path, 'rb') as provinces_colors:
        color_map = pickle.load(provinces_colors)
    return color_map

def rgb_to_hex(r, g, b):
    return '%02X%02X%02X' %(r,g,b)


def write_to_file(path: str, string: str, mode: str = 'w+'):
    print(f"Writing to {path}")
    output_file = Path(path)
    with open(output_file, mode, encoding=UTF_8_BOM) as output_file:
        output_file.write(string)

def zip_on(join_on: str, left_list: list, right_list: list):
    d = defaultdict(list)
    for l in (left_list, right_list):
        for elem in l:
            d[elem[join_on]].append(elem)
    return d.values()
    