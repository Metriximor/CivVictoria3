import json
import rubicon_parser as paradox
from random import randint
from models import CreateBuilding, MapDataState
from utils import load_file_into_string, write_to_file, yaml
from paths import BUILDINGS_OUTPUT, POPS_OUTPUT, STATE_HISTORY_OUTPUT, STATES_MAP_DATA, SPLIT_STATES_INPUT, STATES_DATA_INPUT, STATES_INPUT, COUNTRY_DEFINITIONS


def create_pops(country_abrev: str, state_name: str, state_details: dict, country_data: dict):
    result = ""
    pops = {}
    # Define population size based on pre-set data
    state_population: int = randint(500, 50_000)
    if state_name in state_details and 'population' in state_details[state_name]:
        state_population = state_details[state_name]['population']

    # Initialize pops with pop culture
    pops[country_data[country_abrev]["cultures"][-1]] = {
        "quantity": state_population
    }
    if state_name in state_details and "pops" in state_details[state_name]:
        # Delete existing data about pops
        pops = {}
        total_ratios: int = sum([int(pop["ratio"])
                                for pop in state_details[state_name]["pops"]])
        for pop in state_details[state_name]["pops"]:
            ratio = pop["ratio"]
            pops[pop["culture"]] = {
                "quantity": (ratio/total_ratios) * state_population
            }
            if "religion" in pop:
                pops[pop["culture"]]["religion"] = pop["religion"]
    for culture, pop in pops.items():
        result += "        create_pop = {\n"
        result += f'            culture = {culture}\n'
        if "religion" in pop:
            result += f'            religion = {pop["religion"]}\n'
        result += f'            size = {int(pop["quantity"])}\n'
        result += "        }\n"
    return result


def main():
    # Loads Files
    states = json.loads(load_file_into_string(STATES_INPUT))
    split_states: dict = json.loads(
        load_file_into_string(SPLIT_STATES_INPUT))
    state_details = yaml.load(
        load_file_into_string(STATES_DATA_INPUT))
    country_data = paradox.load(COUNTRY_DEFINITIONS)
    states_data = {state: MapDataState.parse_obj(inner_state_data) for state, inner_state_data in paradox.load(
        STATES_MAP_DATA).items()}

    # Prepare the data
    states = {state: country for country, state_names in states.items()
              for state in state_names}
    capital_states = {country_data[country]['capital']
                      for country in country_data}

    # Prepares Outputs
    provinces = ""
    pops = ""
    buildings = ""

    for state_name, state_data in states_data.items():
        # Determine countries that have a stake in the state
        if state_name in split_states:
            countries = split_states[state_name]
        elif state_name in states:
            countries = {states[state_name]: []}
        else:
            raise Exception(
                f"{state_name} is not defined in {STATES_INPUT}")

        # Generate pops file
        pops += f"s:{state_name} = {{\n"
        for country_abbreviation in countries:
            pops += f"    region_state:{country_abbreviation} = {{\n"
            pops += create_pops(country_abbreviation,
                                state_name, state_details, country_data)
            pops += "    }\n"
        pops += "}\n"

        # Generate buildings file
        buildings += f"s:{state_name} = {{\n"
        for country_abbreviation in countries:
            buildings += f"    region_state:{country_abbreviation} = {{\n"
            if state_name in capital_states:
                gov_admin = CreateBuilding(
                    building='building_government_administration',
                    level=1,
                    activate_production_methods={"pm_simple_organization_government_administration"})
                buildings += paradox.dumps(
                    {'create_building': dict(gov_admin)}, indent_lvl=2)
            buildings += "    }\n"
        buildings += "}\n"

        # Determine provinces of region states (mainly for split states)
        state_provinces = {}
        if len(countries) > 1:
            for country in countries:
                state_provinces[country] = map(
                    lambda p: f"x{p.upper()}", countries[country])
        else:
            country = next(iter(countries.items()))[0]  # Get the only country
            state_provinces[country] = states_data[state_name].provinces

        # Generate provinces file
        provinces += f"s:{state_name} = {{\n"
        for country in countries:
            provinces += "    create_state = {\n"
            provinces += f"        country = c:{country}\n"
            provinces += f"        owned_provinces = {{ {' '.join(state_provinces[country])} }}\n"
            provinces += "    }\n"
        provinces += "}\n"

    # Outputs stuff
    write_to_file(STATE_HISTORY_OUTPUT, provinces)
    write_to_file(POPS_OUTPUT, pops)
    write_to_file(BUILDINGS_OUTPUT, buildings)


if __name__ == '__main__':
    main()
