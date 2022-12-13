import glob
from PIL import Image
from pathlib import Path

root_dir = "./"

for filename in glob.iglob(root_dir + "gfx/interface/**/*.png", recursive=True):
    with Image.open(filename) as open_image:
        if open_image.mode != 'RGB':
            open_image = open_image.convert('RGB')
        print(f"Converting {filename} to .dds from .png")
        path = Path(filename)
        open_image.save(path.with_suffix('.dds'), 'DDS')