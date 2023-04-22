import sys
import pathlib
import rubicon_parser as paradox
from paths import *
from utils import load_file_into_string, move_file, write_to_file, delete_file
from generate_history_states import main as generate_history_states
from strip_quotes_from_provinces_in_map_data import main as strip_quotes_from_provinces
from generate_province_terrains import main as generate_province_terrains

# Fixes path if it is an executable
current_dir = pathlib.Path(sys.argv[0]).resolve().parent
if current_dir.name == "dist":
    root_dir = current_dir.parent
else:
    root_dir = current_dir

# Setup based on user input
working_tree_acknowledgment = 'n'
while working_tree_acknowledgment.lower() != 'y':
    working_tree_acknowledgment = input(
        "I acknowledge my git working tree is clean or that I am fine with potentially losing mod data (y/Y): ")
delete_province_colors = ''
while delete_province_colors.lower() != 'y' and delete_province_colors.lower() != 'n':
    delete_province_colors = input(
        "Delete existing province_colors file? (y/n) (Recommended if you changed the provinces shapes in the editor): ")
if delete_province_colors == 'y':
    delete_file(PROVINCE_COLORS_OUTPUT)

# Clean the 00_states.txt file
print("Stripping quotes from provinces")
strip_quotes_from_provinces()
move_file(STATES_MAP_DATA_OUTPUT, STATES_MAP_DATA)

# Calculate province buildings, natural resources, province terrains
print("Calculate province buildings, natural resources, province terrains, state population, may take a few mins")
generate_province_terrains()
move_file(STATES_MAP_DATA_OUTPUT, STATES_MAP_DATA)
move_file(STATES_DATA_YML_OUTPUT, STATES_DATA_YML_INPUT)

# Generate history files
print("Generating History Files")
generate_history_states()
print("Moving results to history folder")
generated_history_states = paradox.loads(
    load_file_into_string(STATE_HISTORY_OUTPUT))
existing_history_states = paradox.loads(load_file_into_string(STATES_HISTORY))

# Merge the generated with existing states
for state_abrev, create_state in generated_history_states.items():
    existing_history_states['STATES'][state_abrev] = create_state
deleted_states = set(existing_history_states['STATES'].keys(
)) - set(generated_history_states.keys())
deleted_states.discard('s:STATE_DEBUG')  # Ignore debug state
for deleted_state in deleted_states:
    del existing_history_states['STATES'][deleted_state]

# Clean the debug state
print("Stripping quotes from debug state provinces")
strip_quotes_from_provinces(
    f"{MAP_DATA_STATE_REGIONS_FOLDER}/01_debug_state.txt", f"{OUTPUT_FOLDER}/01_debug_state.txt")
move_file(f"{OUTPUT_FOLDER}/01_debug_state.txt",
          f"{MAP_DATA_STATE_REGIONS_FOLDER}/01_debug_state.txt")
debug_provinces = paradox.loads(load_file_into_string(
    f"{MAP_DATA_STATE_REGIONS_FOLDER}/01_debug_state.txt"))['STATE_DEBUG']['provinces']
existing_history_states['STATES']['s:STATE_DEBUG']['create_state']['owned_provinces'] = debug_provinces

# Output the states history file
write_to_file(STATES_HISTORY, paradox.dumps(existing_history_states))

# Do buildings
print("Handling buildings")
generated_buildings = paradox.loads(load_file_into_string(BUILDINGS_OUTPUT))
existing_buildings = paradox.loads(load_file_into_string(BUILDINGS_HISTORY))

for state_abrev, buildings in generated_buildings.items():
    existing_buildings['BUILDINGS'][state_abrev] = buildings
write_to_file(BUILDINGS_HISTORY, paradox.dumps(existing_buildings))

# Do pops
print("Handling pops")
generated_pops = paradox.loads(load_file_into_string(POPS_OUTPUT))
existing_pops = paradox.loads(load_file_into_string(POPS_HISTORY))

for state_abrev, pops in generated_pops.items():
    existing_pops['POPS'][state_abrev] = pops
write_to_file(POPS_HISTORY, paradox.dumps(existing_pops))

input("Finish? (Enter any value): ")
