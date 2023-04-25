import rubicon_parser as paradox
import re
from utils import rgb_to_hex, load_file_into_string, write_to_file, zip_on
import cv2

states_map_data_set: dict = paradox.load("map_data/state_regions/00_states.txt")
provinces_array = cv2.imread("map_data/provinces.png")
height, _, _ = provinces_array.shape

hub_types = ["port", "city"]
for hub_type in hub_types:
    # Load required stuff
    port_instances = paradox.loads(
        load_file_into_string(
            f"gfx/map/map_object_data/generated_map_object_locators_{hub_type}.txt"
        )
    )["game_object_locator"]["instances"]

    # Save the state for logging purposes
    for state, state_map_data in states_map_data_set.items():
        states_map_data_set[state]["state_id"] = state

    # Join data from locators and map_data sources
    merged_set = zip_on("id", states_map_data_set.values(), port_instances)

    # Join that data to the province map hex color
    for value in filter(lambda x: len(x) > 1, merged_set):
        port_coordinates = value[1]["position"]
        x = int(float(port_coordinates[0]))
        y = int(float(port_coordinates[2]))
        b, g, r = provinces_array[height - y, x]
        province_id = f"x{rgb_to_hex(r, g, b)}"
        value[0][hub_type] = province_id
        if province_id not in value[0]["provinces"]:
            print(f"State {value[0]['state_id']} has a misplaced {hub_type} hub")

    # Pass hubs data to parsed data
    hubs_data = {x[0]["id"]: x[0] for x in merged_set}
    for k, v in states_map_data_set.items():
        if v["id"] in hubs_data and hub_type in hubs_data[v["id"]]:
            v[hub_type] = hubs_data[v["id"]][hub_type]
        del v["state_id"]

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
        new_file.append(paradox.dumps({state: states_map_data_set[state]}))
new_string = "\n".join(new_file)

# Output to file
write_to_file("src/output/00_states.txt", new_string)
