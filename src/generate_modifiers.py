from collections import defaultdict
import rubicon_parser as paradox
import yaml_wrapper as yaml
from yaml_wrapper import dq
from utils import load_file_into_string, write_to_file
from pathlib import Path
from paths import OUTPUT_FOLDER

# Generate Goods Modifiers
generated_modifiers: dict = defaultdict(defaultdict)
localizations: dict = defaultdict(str)
for file in Path("common/goods").glob("*.txt"):
    goods = paradox.loads(load_file_into_string(file.as_posix()))
    for good in goods:
        building_output_good_add = generated_modifiers[f"building_output_{good}_add"]
        building_output_good_add["good"] = False
        building_output_good_add["percent"] = False

        building_output_good_mult = generated_modifiers[f"building_output_{good}_mult"]
        building_output_good_mult["good"] = True
        building_output_good_mult["percent"] = True

        building_input_good_add = generated_modifiers[f"building_input_{good}_add"]
        building_input_good_add["good"] = False
        building_input_good_add["percent"] = False

        building_throughput_good_mult = generated_modifiers[
            f"building_throughput_{good}_mult"
        ]
        building_throughput_good_mult["good"] = True
        building_throughput_good_mult["percent"] = True

        country_good_reserve_limit_mult = generated_modifiers[
            f"country_{good}_reserve_limit_mult"
        ]
        country_good_reserve_limit_mult["good"] = True
        country_good_reserve_limit_mult["percent"] = True

# Generate interest group modifiers
for file in Path("common/interest_groups").glob("*.txt"):
    interest_groups = paradox.loads(load_file_into_string(file.as_posix()))
    for interest_group in interest_groups:
        interest_group_pop_attraction_mult = generated_modifiers[
            f"interest_group_{interest_group}_pop_attraction_mult"
        ]
        interest_group_pop_attraction_mult["neutral"] = True
        interest_group_pop_attraction_mult["percent"] = True

        interest_group_pop_attraction_mult = generated_modifiers[
            f"interest_group_{interest_group}_pol_str_mult"
        ]
        interest_group_pop_attraction_mult["neutral"] = True
        interest_group_pop_attraction_mult["percent"] = True
        interest_group_pop_attraction_mult["num_decimals"] = 0

        interest_group_pop_attraction_mult = generated_modifiers[
            f"interest_group_{interest_group}_pol_attraction_mult"
        ]
        interest_group_pop_attraction_mult["neutral"] = True
        interest_group_pop_attraction_mult["percent"] = True

pop_type_list = []
for file in Path("common/pop_types").glob("*.txt"):
    pop_types = paradox.loads(load_file_into_string(file.as_posix()))
    for pop_type in pop_types:
        pop_type_list.append(pop_type)
        localizations[
            f"modifier_state_{pop_type}_investment_pool_contribution_add"
        ] = dq(f"${pop_type}$ [concept_investment_pool] contribution")
        localizations[
            f"modifier_state_{pop_type}_investment_pool_contribution_add_desc"
        ] = dq(f"How much of their profits ${pop_type}$ will invest")

        localizations[
            f"modifier_state_{pop_type}_investment_pool_efficiency_mult"
        ] = dq(f"${pop_type}$ [concept_investment_pool] contribution efficiency")
        localizations[
            f"modifier_state_{pop_type}_investment_pool_efficiency_mult"
        ] = dq(
            f"An increase or decrease to how much the invested profits from ${pop_type}$ will contribute to the [concept_investment_pool]"
        )


# Generate building groups modifiers
for file in Path("common/building_groups").glob("*.txt"):
    building_groups = paradox.loads(load_file_into_string(file.as_posix()))
    for bg_type in building_groups:
        country_subsidies_bg_type = generated_modifiers[f"country_subsidies_{bg_type}"]
        country_subsidies_bg_type["good"] = True
        country_subsidies_bg_type["boolean"] = True

        building_group_bg_type_employee_mult = generated_modifiers[
            f"building_group_{bg_type}_employee_mult"
        ]
        building_group_bg_type_employee_mult["good"] = False
        building_group_bg_type_employee_mult["percent"] = True

        building_group_bg_type_mortality_mult = generated_modifiers[
            f"building_group_{bg_type}_mortality_mult"
        ]
        building_group_bg_type_employee_mult["good"] = False
        building_group_bg_type_employee_mult["percent"] = True

        building_group_bg_type_standard_of_living_add = generated_modifiers[
            f"building_group_{bg_type}_standard_of_living_add"
        ]
        building_group_bg_type_standard_of_living_add["good"] = True
        building_group_bg_type_standard_of_living_add["percent"] = False

        building_group_bg_type_tax_mult = generated_modifiers[
            f"building_group_{bg_type}_tax_mult"
        ]
        building_group_bg_type_tax_mult["good"] = True
        building_group_bg_type_tax_mult["percent"] = True

        for pop_type in pop_type_list:
            building_group_bg_type_pop_type_mortality_mult = generated_modifiers[
                f"building_group_{bg_type}_{pop_type}_mortality_mult"
            ]
            building_group_bg_type_pop_type_mortality_mult["good"] = False
            building_group_bg_type_pop_type_mortality_mult["percent"] = True

            building_group_bg_type_pop_type_standard_of_living_add = (
                generated_modifiers[
                    f"building_group_{bg_type}_{pop_type}_standard_of_living_add"
                ]
            )
            building_group_bg_type_pop_type_standard_of_living_add["good"] = True
            building_group_bg_type_pop_type_standard_of_living_add["percent"] = False

generated_modifiers = {k: dict(v) for k, v in generated_modifiers.items()}
localizations = {"l_english": dict(localizations)}
write_to_file(
    f"common/modifier_types/civ_modifier_types.txt", paradox.dumps(generated_modifiers)
)
write_to_file(f"{OUTPUT_FOLDER}/civ_modifier_types.yml", yaml.dumps(localizations))
# Localization
