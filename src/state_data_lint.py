from utils import load_file_into_string, write_to_file
from paths import MAP_DATA_STATE_REGIONS_FOLDER
import rubicon_parser as paradox

debug_state = load_file_into_string(
    f"{MAP_DATA_STATE_REGIONS_FOLDER}/01_debug_state.txt"
)
states = load_file_into_string(f"{MAP_DATA_STATE_REGIONS_FOLDER}/00_states.txt")
out_of_bounds_states = load_file_into_string(
    f"{MAP_DATA_STATE_REGIONS_FOLDER}/02_out_of_bounds.txt"
)
seas_states = load_file_into_string(f"{MAP_DATA_STATE_REGIONS_FOLDER}/99_seas.txt")

seen_provinces = set()
seen_state_ids = set()
seen_states = set()

def check_states(data: str):
    states = paradox.loads(data)
    for state, state_data in states.items():
        if state in seen_states:
            print(f"{state} already exists!")
            raise Exception
        else:
            seen_states.add(state)

        state_id = state_data['id']

        if state_id in seen_state_ids:
            print(f"{state} has already existing id: {state_id}")
            raise Exception
        else:
            seen_state_ids.add(state_id)

        provinces = state_data['provinces']

        for province in provinces:
            if province in seen_provinces:
                print(f"{province} is already being used!")
                raise Exception
            else:
                seen_provinces.add(province)

check_states(debug_state)
check_states(states)
check_states(out_of_bounds_states)
check_states(seas_states)

print(f"Found {len(seen_state_ids)} states and {len(seen_provinces)} provinces")

        