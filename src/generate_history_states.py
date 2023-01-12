import json
from pathlib import Path
from random import randint

UTF_8_BOM = 'utf-8-sig'

def load_file_into_string(path: str):
    string = ""
    file = Path(path)
    with file.open(encoding=UTF_8_BOM) as f:
        string = f.read()
    return string

# Loads Files
states = json.loads(load_file_into_string("src/input/states.json"))
states = {state: country  for country, state_names in states.items() for state in state_names}
split_states: dict = json.loads(load_file_into_string("src/input/split_states.json"))
state_data = load_file_into_string("map_data/state_regions/00_states.txt")

# Prepares Outputs
output = ""
output_file = Path("src/output/state_history.txt")
pops = ""
pops_file = Path("src/output/pops.txt")
buildings = ""
buildings_file = Path("src/output/buildings.txt")

# Does the thing
state_name = ""
countries: dict = {}
for string in state_data.split("\n"):
    if string.startswith("#"):
        continue
    if string.startswith("STATE_"):
        state_name = string.split(" ")[0]
        if state_name in split_states:
            countries = split_states[state_name]
        else:
            countries = {states.get(state_name, ""):[]}

        pops += f"s:{state_name} = {{\n"
        for country_abbreviation in countries:
            pops += f"    region_state:{country_abbreviation} = {{\n"
            pops +=  "        create_pop = {\n"
            pops +=  "            culture = lusitan\n"
            pops +=	f"            size = {randint(500, 1_000_000)}\n"
            pops +=  "        }\n"
            pops +=  "    }\n"
        pops +=  "}\n"

        buildings += f"s:{state_name} = {{\n"
        for country_abbreviation in countries:
            buildings += f"    region_state:{country_abbreviation} = {{\n"
            buildings +=  "    }\n"
        buildings +=  "}\n"
        
    if "=" in string and len(countries) != 0:
        key, value = string.strip().split("=")
        key = key.strip()
        value = value.strip()
        if key == "provinces":
            if len(countries) > 1:
                provinces = {}
                for country in countries:
                    provinces[country] = map(lambda p: f"x{p.upper()}", countries[country])
            else:
                country = next(iter(countries.items()))[0]
                provinces = {}
                provinces[country] = map(lambda p: p.strip('"'), value.strip("{}").split())
            # Construct the output string for this state
            output += f"s:{state_name} = {{\n"
            for country in countries:
                output += "    create_state = {\n"
                output += f"        country = c:{country}\n"
                output += f"        owned_provinces = {{ {' '.join(provinces[country])} }}\n"
                output += "    }\n"
            output += "}\n"
            countries = {}

# Outputs stuff
with open(output_file, 'w+', encoding=UTF_8_BOM) as output_file:
    output_file.write(output)

with open(pops_file, 'w+', encoding=UTF_8_BOM) as pops_file:
    pops_file.write(pops)

with open(buildings_file, 'w+', encoding=UTF_8_BOM) as buildings_file:
    buildings_file.write(buildings)