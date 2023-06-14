import rubicon_parser as paradox
import re
from utils import load_file_into_string, write_to_file, yaml

states_map_data: dict = paradox.load("map_data/state_regions/00_states.txt")
seas_map_data = paradox.load("map_data/state_regions/99_seas.txt")
states_data: dict = yaml.load(load_file_into_string("src/input/state_data.yml"))

# Add naval exit id
NAVAL_EXIT_ID = "naval_exit_id"
for state, state_data in states_data.items():
    if NAVAL_EXIT_ID in state_data:
        sea = state_data[NAVAL_EXIT_ID]
        sea_province = seas_map_data[sea]["id"]
        states_map_data[state][NAVAL_EXIT_ID] = sea_province

# Update existing entries
file_string = load_file_into_string("map_data/state_regions/00_states.txt").splitlines()
new_file = []
delete_flag = False
for line in file_string:
    state_match = re.match(r"^([\w_]+)", line)
    if state_match is None and delete_flag is False:
        if line.startswith("#"):
            new_file.append(line)
        continue
    if state_match is not None:
        state = state_match.group(0)
        line = line.replace(f"{state} = {{", "")
        new_file.append(paradox.dumps({state: states_map_data[state]}))
new_string = "\n".join(new_file)

# Output to file
write_to_file("src/output/00_states.txt", new_string)
