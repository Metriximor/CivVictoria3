import pickle
import bz2
import numpy as np
from pathlib import Path
from collections import defaultdict
from PIL import Image

UTF_8_BOM = 'utf-8-sig'

def file_exists(path):
  return Path(path).is_file()

def map_colors(array):
  # Create an empty dictionary
  color_map = {}
  xB, yB, _ = array.shape
  for x in range(0, xB):
    print(f"Mapping {x} out of {xB}")
    for y in range(0, yB):
        r, g, b = array[x,y]
        if (r, g, b) not in color_map:
            color_map[(r, g, b)] = list((x, y))
        else:
            color_map[(r, g, b)].append((x, y))

  return color_map

color_map = {}
# Provinces colors is a dict where the key is a tuple (r,g,b) and the values are the (x,y) locations
provinces_path = "src/output/provinces_colors"
if file_exists(provinces_path):
  with bz2.BZ2File(provinces_path, 'rb') as provinces_colors:
    color_map = pickle.load(provinces_colors)
else:
    provinces_img = Image.open("map_data/provinces.png")
    provinces_array = np.asarray(provinces_img)
    color_map = map_colors(provinces_array)
    print("Color map generated, zipping into file\n")
    print(len(color_map))
    with bz2.BZ2File(provinces_path, 'wb') as config_dictionary_file:
        pickle.dump(color_map, config_dictionary_file)

output = "#This is a generated file, do not modify unless you know what you are doing!\n"
rgb2hex = lambda r,g,b: 'x%02X%02X%02X' %(r,g,b)
for hex in [ rgb2hex(r, g, b) for r, g, b in color_map ]:
    output += f'{hex}="plains"\n'

with open("src/output/province_terrains.txt", 'w+', encoding=UTF_8_BOM) as output_file:
    output_file.write(output)