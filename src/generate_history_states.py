import json
from pathlib import Path

UTF_8_BOM = 'utf-8-sig'

states_file = Path("src/input/states.json")

with open(states_file, encoding=UTF_8_BOM) as f:
    file_contents = f.read()

states = json.loads(file_contents)
# Inverts the list
states = {state: country  for country, state_names in states.items() for state in state_names}

state_data_file = Path("map_data/state_regions/00_states.txt")

with state_data_file.open(encoding=UTF_8_BOM) as f:
    state_data = f.read()

output = ""
output_file = Path("src/output/state_history.txt")

# # Iterate through each state in the states dictionary
# for abbreviation, names in states.items():
#     for name in names:
#         # Extract the state data from the state_data string
#         state_string = state_data.split(name)[0]
#         state_string = state_string.split("}")[0]
        
#         # Parse the state data to extract the state name and provinces
#         state_name = None
#         provinces = []
state_name = ""
country_abbreviation = ""
for string in state_data.split("\n"):
    if string.startswith("#"):
        continue
    if string.startswith("STATE_"):
        state_name = string.split(" ")[0]
        country_abbreviation = states.get(state_name, "")
    if "=" in string and country_abbreviation != "":
        key, value = string.strip().split("=")
        key = key.strip()
        value = value.strip()
        if key == "provinces":
            provinces = value.strip("{}").split()
            provinces = [province.strip('"') for province in provinces]
            # Construct the output string for this state
            output += f"s:{state_name} = {{\n"
            output += "    create_state = {\n"
            output += f"        country = c:{country_abbreviation}\n"
            output += f"        owned_provinces = {{ {' '.join(provinces)} }}\n"
            output += "    }\n"
            output += "}\n"
            country_abbreviation = ""

with open(output_file, 'w+', encoding=UTF_8_BOM) as output_file:
    output_file.write(output)
