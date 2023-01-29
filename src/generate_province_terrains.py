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
                print(f"\r{processed_pixels / total_pixels * 100:.0f}% completed", end='')
    print("\nProcessing complete!")
    return mapped_colors

# Prepares Inputs
color_map = {}
provinces_path = "src/output/provinces_colors"
if file_exists(provinces_path):
  print("Loading existing province color terrains file")
  with BZ2File(provinces_path, 'rb') as provinces_colors:
    color_map = pickle.load(provinces_colors)
else:
    color_map = extract_colors("map_data/provinces.png")
    print("Color map generated, zipping into file\n")
    print(len(color_map))
    with BZ2File(provinces_path, 'wb') as config_dictionary_file:
        pickle.dump(color_map, config_dictionary_file)

biome_data = yaml.load(load_file_into_string("src/input/biomes_mapping.yml"))
biomes_map = cv2.imread("map_data/provinces.png")

# Temporary
output = "#This is a generated file, do not modify unless you know what you are doing!\n"
for hex in [ f"x{hex}" for hex in color_map ]:
    output += f'{hex}="plains"\n'

# Final output
write_to_file("src/output/province_terrains.txt", output)