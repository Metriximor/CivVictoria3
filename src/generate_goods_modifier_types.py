import re
import inflect
from pathlib import Path

UTF_8_BOM = 'utf-8-sig'

languages = ['english']
generated_goods: list[str] = []
p = inflect.engine()

for file in Path('common/goods').glob('*.txt'):
    output_file_path = Path(f"common/modifier_types/building_{file.stem}_modifier_types.txt")
    output_file_path.parent.mkdir(exist_ok=True, parents=True)
    with open(file, encoding=UTF_8_BOM) as goods_file, open(output_file_path, 'w+', encoding=UTF_8_BOM) as output_file:
        for line in goods_file:
            match = re.search(r"^\w+", line)
            if match:
                good = match.group(0)
                print(f"Generating building inputs and outputs for {good}")
                output_file.write(f'''building_output_{good}_add = {{
    good = yes
    percent = no
}}

building_input_{good}_add = {{
    good = no
    percent = no
}}

building_output_{good}_mult = {{
    good = yes
    percent = yes
}}

''')
                generated_goods.append(good)
            else:
                continue
    for language in languages:
        localization_file_path = Path(f"localization/{language}/civ_modifiers_l_{language}.yml")
        localization_file_path.parent.mkdir(exist_ok=True, parents=True)
        with open(localization_file_path, 'w+', encoding=UTF_8_BOM) as localization_file:
            if generated_goods:
                localization_file.write(f'''l_{language}:
''')
            for good in generated_goods:
                indefinite_article = p.a(good, count=1).split(' ')[0]
                print(f"Generating building inputs and outputs localization for {good}")
                # TODO Sanitize the second goods in each line for user readable text
                localization_file.write(f''' modifier_building_input_{good}_add: "@{good}! ${good}$ input per level"
 modifier_building_input_{good}_add_desc: "The amount of @{good}! ${good}$ consumed by buildings"
 modifier_building_output_{good}_add: "@{good}! {good} output per level"
 modifier_building_output_{good}_add_desc: "The amount of @{good}! ${good}$ produced by buildings"
 modifier_building_output_{good}_mult: "Building @{good}! ${good}$ output"
 modifier_building_output_{good}_mult_desc: "A bonus or penalty to the amount of @{good}! ${good}$ produced by buildings"
 trade_route_export_lens_option_{good}_tooltip: "Establish {indefinite_article} ${good}$ export trade route"
 trade_route_import_lens_option_{good}_tooltip: "Establish {indefinite_article} ${good}$ import trade route"
''')
