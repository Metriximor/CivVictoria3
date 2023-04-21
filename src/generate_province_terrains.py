from collections import defaultdict
from pathlib import Path
import re
from paths import PROVINCE_TERRAINS_OUTPUT, STATES_DATA_YML_OUTPUT, STATES_MAP_DATA, STATES_MAP_DATA_OUTPUT
import rubicon_parser as paradox
import pickle
import cv2
from bz2 import BZ2File
from utils import write_to_file, rgb_to_hex, file_exists, yaml, load_file_into_string


# Generates province_colors if it doesn't exist yet
# Provinces colors is a dict where the key is a tuple (r,g,b) and the values are the (x,y) locations
def extract_colors(image_file):
    img = cv2.imread(image_file)
    height, width, _ = img.shape
    mapped_colors = {}
    total_pixels = height * width
    processed_pixels = 0
    for x in range(width):
        for y in range(height):
            b, g, r = img[y][x]
            hex_val = rgb_to_hex(r, g, b)
            if hex_val not in mapped_colors:
                mapped_colors[hex_val] = []
            mapped_colors[hex_val].append([x, y])
            processed_pixels += 1
            if processed_pixels % (total_pixels // 100) == 0:
                print(
                    f"\r{processed_pixels / total_pixels * 100:.0f}% completed", end='')
    print("\nProcessing complete!")
    return mapped_colors


def calculate_state_population(state_biomes: list[tuple[str, int]], biome_data: dict) -> int:
    pop_count = 0
    total_state_pixels = 0
    unknown_size = 0
    for biome, size in state_biomes:
        if biome == 'unknown':
            unknown_size = size
        if biome not in biome_data['minecraft_biomes']:
            continue
        populational_density = biome_data['minecraft_biomes'][biome]['populational_density']
        pop_count += size * populational_density
        total_state_pixels += size
    if 'unknown' in biome_data['minecraft_biomes']:
        for biome, size in state_biomes:
            if biome not in biome_data['minecraft_biomes']:
                continue
            ratio = size / total_state_pixels
            populational_density = biome_data['minecraft_biomes'][biome]['populational_density']
            pop_count += int(ratio * unknown_size) * populational_density
    return pop_count

def main():
    # Prepares Inputs
    biome_data = yaml.load(load_file_into_string("src/input/biomes_mapping.yml"))
    state_data = yaml.load(load_file_into_string("src/input/state_data.yml"))
    minecraft_biomes_map = {str(biome_data['input_biomes'][input_biome]).upper(): minecraft_biome for minecraft_biome,
                            input_biomes in biome_data['minecraft_biomes'].items() for input_biome in input_biomes['input_biomes']}

    province_map = {}
    provinces_path = "src/output/provinces_colors"
    if file_exists(provinces_path):
        print("Loading existing province color terrains file")
        with BZ2File(provinces_path, 'rb') as provinces_colors:
            province_map = pickle.load(provinces_colors)
        print("Loaded province terrains file")
    else:
        province_map = extract_colors("map_data/provinces.png")
        print(f"Found {len(province_map)} provinces")
        print("Color map generated, zipping into file...")
        with BZ2File(provinces_path, 'wb') as config_dictionary_file:
            pickle.dump(province_map, config_dictionary_file)

    biomes_map = cv2.imread("src/input/biomes.png")
    map_states_data = paradox.loads(load_file_into_string(STATES_MAP_DATA))

    # Calculate arable land resources
    for state_name, map_state_data in map_states_data.items():
        provinces = map_state_data['provinces']
        state_resources = defaultdict(lambda: 0, {})
        for province in provinces:
            province = province[1:]  # remove the x from the province id
            # load all province coordinates
            province_coords = province_map[province]
            for x, y in province_coords:
                b, g, r = biomes_map[y][x]
                hex = rgb_to_hex(r, g, b)
                if hex not in minecraft_biomes_map:
                    state_resources['unknown'] += 1
                else:
                    state_resources[minecraft_biomes_map[hex]] += 1
        map_state_data['capped_resources'] = {}
        map_state_data['capped_resources']['bg_sand_pit'] = 5
        if len(state_resources) > 0:
            state_resources = sorted(
                dict(state_resources).items(), key=lambda x: x[1], reverse=True)
            pop_count = calculate_state_population(state_resources, biome_data)
            if state_name not in state_data:
                state_data[state_name] = {}
            state_data[state_name]['population'] = pop_count
            biggest_biome, biome_size = state_resources[0]
            if biggest_biome == 'desert':
                map_state_data['capped_resources']['bg_sand_pit'] = 80
            map_state_data['traits'] = [f'"state_trait_{state_resources[0][0]}"']
            map_state_data['arable_resources'] = [
                f'"{valid_farm}"' for valid_farm in biome_data['minecraft_biomes'][biggest_biome]['valid_farms']]

    # Update existing entries
    file_string = load_file_into_string(STATES_MAP_DATA).splitlines()
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
            line = line.replace(f"{state} = {{", '')
            new_file.append(paradox.dumps({state: map_states_data[state]}))
    new_string = '\n'.join(new_file)
    write_to_file(STATES_MAP_DATA_OUTPUT, new_string)

    print(f"Writing to {STATES_DATA_YML_OUTPUT}")
    yaml.dump(state_data,  Path(STATES_DATA_YML_OUTPUT))

    # Temporary province terrain
    output = "#This is a generated file, do not modify unless you know what you are doing!\n"
    for hex in [f"x{hex}" for hex in province_map]:
        output += f'{hex}="plains"\n'

    # Final output
    write_to_file(PROVINCE_TERRAINS_OUTPUT, output)

if __name__ == "__main__":
    main()