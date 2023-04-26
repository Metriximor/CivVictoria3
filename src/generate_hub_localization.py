from pathlib import Path
import re
import random
import rubicon_parser as paradox
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as dq
from utils import load_file_into_string, write_to_file


def localization_yaml_to_dict(states: str):
    pattern = re.compile(r"(\w+):\d+ \"(.+?)\"")
    matches = pattern.finditer(states)
    state_dict = {}
    for match in matches:
        state, state_loc = match.groups()
        state_dict[state] = state_loc
    return state_dict

def main():
    # Declare consts
    yaml = YAML(typ="rt")
    yaml.default_flow_style = False
    random.seed(1)
    hub_types = ["city", "wood", "port", "mine", "farm"]
    hub_suffixes = {
        "city": [""],
        "port": ["Harbour", "Port", "Dockyards"],
        "wood": ["Woods", "Tree Farm", "Forest"],
        "mine": ["Mineshaft", "Mine", "Quarry"],
        "farm": ["Farm", "Fields", "Farmstead"],
    }

    # Read necessary values
    hub_names = yaml.load(load_file_into_string("src/input/city_names.yml"))
    state_localization = yaml.load(
        load_file_into_string("localization/english/civ_states_l_english.yml")
    )["l_english"]
    states = paradox.load("map_data/state_regions/00_states.txt")

    # Prepare data
    state_localization = localization_yaml_to_dict(state_localization)

    # Generate names
    unnamed_states: set[str] = set()
    for state in states.keys():
        for hub_type in hub_types:
            # If name already exists, skip
            if state in hub_names and hub_type in hub_names[state]:
                continue
            suffix = random.choice(hub_suffixes[hub_type])
            if state not in hub_names:
                hub_names[state] = {}
            if state not in state_localization:
                unnamed_states.add(state)
                continue
            is_plural = "'s "
            if state_localization[state].endswith("s"):
                is_plural = " "
            if hub_type == "city":
                is_plural = ""
            hub_names[state][hub_type] = f"{state_localization[state]}{is_plural}{suffix}"
    if unnamed_states:
        raise KeyError(f"States dont have localization in localization/english/civ_states_l_english.yml: {unnamed_states}")

    # Convert hub_names to output yaml
    output = {}
    for state_key, hub_type_names in hub_names.items():
        for hub_type, hub_name in hub_type_names.items():
            output[f"HUB_NAME_{state_key}_{hub_type}"] = dq(hub_name)
    output = {"l_english": output}

    # Write output
    path_str = "src/output/civ_hubs_l_english.yml"
    path = Path(path_str)
    yaml.dump(output, path)
    utf_8_localization = load_file_into_string(path_str, encoding=None)
    write_to_file(path_str, utf_8_localization)

if __name__ == "__main__":
    main()