import re
from utils import load_file_into_string, write_to_file

pattern = r'"(x[a-fA-F0-9]{6})"'
map_data_str = load_file_into_string("map_data/state_regions/00_states.txt")
map_data_stripped = re.sub(pattern, r'\1', map_data_str)
write_to_file("src/output/00_states.txt", map_data_stripped)