import rubicon_parser as paradox
import re
from utils import (
    rgb_to_hex,
    load_file_into_string,
    write_to_file,
    zip_on,
    copy_file,
    move_file,
)
import cv2
from paths import OUTPUT_FOLDER

hub_types = ["port", "city"]


def move_generated_locators():
    for hub_type in hub_types:
        # Move files from generated folder to mod folder
        output_file_name = (
            f"{OUTPUT_FOLDER}/generated_map_object_locators_{hub_type}.txt"
        )
        copy_file(
            f"../../generated/generated_map_object_locators_{hub_type}.txt",
            output_file_name,
        )
        # Load locator instances
        locator_instances = load_file_into_string(output_file_name)
        pattern = r"instances={(.*)}"
        match = re.search(pattern, locator_instances, re.DOTALL)
        new_content = ""
        if match:
            new_content = match.group(1)
        else:
            raise Exception(f"No match 'instances' found inside {locator_instances}")
        # Read existing instances
        existing_file_name = (
            f"gfx/map/map_object_data/generated_map_object_locators_{hub_type}.txt"
        )
        existing_instances_str: str = load_file_into_string(existing_file_name)
        # use regex to match everything inside the curly braces of instances
        match = re.search(pattern, existing_instances_str, re.DOTALL)
        # if a match was found, replace the old content with the new content
        if match:
            old_content = match.group(1)
            existing_instances_str = existing_instances_str.replace(
                old_content, new_content
            )
        else:
            raise Exception(f"No match 'instances' found inside {existing_file_name}")
        # Writes back into source
        write_to_file(
            output_file_name,
            existing_instances_str,
        )
        move_file(output_file_name, existing_file_name)


def main():
    states_map_data_set = paradox.load("map_data/state_regions/00_states.txt")
    provinces_array = cv2.imread("map_data/provinces.png")
    height, _, _ = provinces_array.shape

    for hub_type in hub_types:
        # Load required stuff
        locator_file_name = (
            f"gfx/map/map_object_data/generated_map_object_locators_{hub_type}.txt"
        )
        port_instances = paradox.loads(load_file_into_string(locator_file_name))[
            "game_object_locator"
        ]["instances"]

        # Save the state for logging purposes
        for state, state_map_data in states_map_data_set.items():
            states_map_data_set[state]["state_id"] = state

        # Join data from locators and map_data sources
        merged_set = zip_on("id", states_map_data_set.values(), port_instances) # type: ignore

        # Join that data to the province map hex color
        no_position_states: set[str] = set()
        for value in filter(lambda x: len(x) > 1, merged_set):
            if len(value) > 2:
                raise Exception(f"There are 2 states with the id {value[1]['id']}")
            if "position" not in value[1]:
                no_position_states.add(f"{value[1]['id']}")
                continue
            port_coordinates = value[1]["position"]
            x = int(float(port_coordinates[0]))
            y = int(float(port_coordinates[2]))
            b, g, r = provinces_array[height - y, x]
            province_id = f"x{rgb_to_hex(r, g, b)}"
            value[0][hub_type] = province_id
            if province_id not in value[0]["provinces"]:
                print(f"State {value[0]['state_id']} has a misplaced {hub_type} hub")
        if no_position_states:
            print(
                f"States without position defined in {locator_file_name}: {no_position_states}"
            )
            no_position_states.clear()
            return False

        # Pass hubs data to parsed data
        hubs_data = {x[0]["id"]: x[0] for x in merged_set}
        for k, v in states_map_data_set.items():
            if v["id"] in hubs_data and hub_type in hubs_data[v["id"]]:
                v[hub_type] = hubs_data[v["id"]][hub_type]
            del v["state_id"]

    # Update existing entries
    file_string = load_file_into_string(
        "map_data/state_regions/00_states.txt"
    ).splitlines()
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

    return True


if __name__ == "__main__":
    main()
