import json
import rubicon_parser as paradox
from random import randint
from utils import load_file_into_string, write_to_file, yaml

def create_pops(country_abrev, state_name):
    result = ""
    pops = {}
    state_population: int = randint(500, 1_000_000)
    # Initialize pops with pop culture
    pops[country_data[country_abrev]["cultures"][-1]] = {
        "quantity": state_population
    }
    if state_name in state_details and "pops" in state_details[state_name]:
        # Delete existing data about pops
        pops = {}
        total_ratios: int = sum([int(pop["ratio"]) for pop in state_details[state_name]["pops"]])
        for pop in state_details[state_name]["pops"]:
            pops[pop["culture"]] = {
                "quantity": state_population/total_ratios
            }
            if "religion" in pop:
                pops[pop["culture"]]["religion"] = pop["religion"]
    for culture, pop in pops.items():
        result +=  "        create_pop = {\n"
        result += f'            culture = {culture}\n'
        if "religion" in pop:
            result += f'            religion = {pop["religion"]}\n'
        result += f'            size = {int(pop["quantity"])}\n'
        result +=  "        }\n"
    return result

# Loads Files
states = json.loads(load_file_into_string("src/input/states.json"))
split_states: dict = json.loads(load_file_into_string("src/input/split_states.json"))
state_data = load_file_into_string("map_data/state_regions/00_states.txt")
state_details = yaml.load(load_file_into_string("src/input/state_data.yml"))
country_data = paradox.load("common/country_definitions/00_countries.txt")

# Prepare the data
states = {state: country  for country, state_names in states.items() for state in state_names}

# Prepares Outputs
output = ""
pops = ""
buildings = ""

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

        # Generates pops file
        pops += f"s:{state_name} = {{\n"
        for country_abbreviation in countries:
            pops += f"    region_state:{country_abbreviation} = {{\n"
            pops += create_pops(country_abbreviation, state_name)
            pops +=  "    }\n"
        pops +=  "}\n"

        # Generates buildings file
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

            # Generates provinces file
            output += f"s:{state_name} = {{\n"
            for country in countries:
                output += "    create_state = {\n"
                output += f"        country = c:{country}\n"
                output += f"        owned_provinces = {{ {' '.join(provinces[country])} }}\n"
                output += "    }\n"
            output += "}\n"
            countries = {}

# Outputs stuff
write_to_file("src/output/state_history.txt", output)
write_to_file("src/output/pops.txt", pops)
write_to_file("src/output/buildings.txt", buildings)