import re
from utils import load_file_into_string, write_to_file
from paths import STATES_MAP_DATA, STATES_MAP_DATA_OUTPUT


def main(
    file_to_strip: str = STATES_MAP_DATA, output_path: str = STATES_MAP_DATA_OUTPUT
):
    pattern = r'"(x[a-fA-F0-9]{6})"'
    map_data_str = load_file_into_string(file_to_strip)
    map_data_stripped = re.sub(pattern, r"\1", map_data_str)
    write_to_file(output_path, map_data_stripped)


if __name__ == "__main__":
    main()
