import glob
from pathlib import Path

root_dir = "./"

for txt_file in glob.iglob(root_dir + "/**/*.txt", recursive=True):
    path = Path(txt_file)
    path.write_text(path.read_text(), encoding="utf-8-sig")