import glob
from wand.image import Image
from pathlib import Path

root_dir = "./"

for png_image in glob.iglob(root_dir + "gfx/interface/**/*.png", recursive=True) and glob.iglob(root_dir + "gfx/coat_of_arms/**/*.png") and glob.iglob(root_dir + "gfx/models/**/*.png"):
    with Image(filename=png_image) as open_image:
        print(f"Converting {png_image} to .dds from .png")
        open_image.compression='dxt5'
        path = Path(png_image)
        open_image.save(filename=path.with_suffix('.dds'))