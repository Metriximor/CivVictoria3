import re
from pathlib import Path

UTF_8_BOM = 'utf-8-sig'

languages = ['english']
generated_goods = []

for file in Path('common/goods').glob('*.txt'):
    output_file_path = Path(f"common/modifier_types/building_{file.stem}_modifier_types.txt")
    output_file_path.parent.mkdir(exist_ok=True, parents=True)
    with open(file, encoding=UTF_8_BOM) as goods_file, open(output_file_path, 'w+', encoding=UTF_8_BOM) as output_file:
        for line in goods_file:
            match = re.search(r"^\w+", line)
            if match:
                goods = match.group(0)
                print(f"Generating building inputs and outputs for {goods}")
                output_file.write(f'''building_output_{goods}_add = {{
    good = yes
    percent = no
}}

building_input_{goods}_add = {{
    good = no
    percent = no
}}

building_output_{goods}_mult = {{
    good = yes
    percent = yes
}}

''')
                generated_goods.append(goods)
            else:
                continue
    for language in languages:
        localization_file_path = Path(f"localization/{language}/modifiers_l_{language}.yml")
        localization_file_path.parent.mkdir(exist_ok=True, parents=True)
        with open(localization_file_path, 'w+', encoding=UTF_8_BOM) as localization_file:
            if generated_goods:
                localization_file.write(f'''l_{language}:
''')
            for goods in generated_goods:
                print(f"Generating building inputs and outputs localization for {goods}")
                # TODO Sanitize the second goods in each line for user readable text
                localization_file.write(f''' modifier_building_input_{goods}_add: "@{goods}! ${goods}$ input per level"
 modifier_building_input_{goods}_add_desc: "The amount of @{goods}! ${goods}$ consumed by buildings"
 modifier_building_output_{goods}_add: "@{goods}! {goods} output per level"
 modifier_building_output_{goods}_add_desc: "The amount of @{goods}! ${goods}$ produced by buildings"
 modifier_building_output_{goods}_mult: "Building @{goods}! ${goods}$ output"
 modifier_building_output_{goods}_mult_desc: "A bonus or penalty to the amount of @{goods}! ${goods}$ produced by buildings"
''')
