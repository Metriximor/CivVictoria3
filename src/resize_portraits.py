import glob
from wand.image import Image, Color
from pathlib import Path

root_dir = "./"


def resize_and_save_as_dds(png_image: str, open_image: Image):
    print(f"Converting {png_image} to .dds from .png")
    path = Path(png_image)
    with Image(width=1068, height=1000, background=Color("transparent")) as bg:
        bg.composite(open_image, left=234, top=-45)
        bg.compression = "dxt5"
        bg.save(filename=path.with_suffix(".dds"))


for png_image in glob.iglob(
    root_dir + "gfx/models/skins/skins_textures/**/*.png", recursive=True
):
    with Image(filename=png_image) as open_image:
        resize_and_save_as_dds(png_image, open_image)
