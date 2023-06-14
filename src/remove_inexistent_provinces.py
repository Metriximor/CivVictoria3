import re
from pathlib import Path
from random import randint

UTF_8_BOM = "utf-8-sig"


def extract_provinces(inexistent_provinces):
    provinces = []
    for match in re.finditer(r"Province: (x[A-Fa-f0-9]{6})", inexistent_provinces):
        if match:
            provinces.append(match.group(1))
    return provinces


inexistent_provinces: list[str] = []
with open(Path("src/input/inexistent_provinces.txt"), encoding=UTF_8_BOM) as f:
    inexistent_provinces = [f'"{s}"' for s in extract_provinces(f.read())]
print(inexistent_provinces)

# state_file_name = "00_states"
state_file_name = "01_debug_state"
# state_file_name = "99_seas"
states = ""
with open(
    Path(f"map_data/state_regions/{state_file_name}.txt"), encoding=UTF_8_BOM
) as f:
    states = f.read()

for inexistent_province in inexistent_provinces:
    states = states.replace(inexistent_province, "")

states = states.replace('"" ', "")

with open(Path("src/output/00_states.txt"), "w+", encoding=UTF_8_BOM) as output_file:
    output_file.write(states)
