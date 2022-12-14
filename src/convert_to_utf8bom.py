import glob
from pathlib import Path

root_dir = "./"

for txt_file in glob.iglob(root_dir + "/**/*.txt", recursive=True):
    with open(txt_file, 'rb') as f:
        data = f.read(3)

        if data == b'\xef\xbb\xbf':
            continue
        
        f.seek(0)
        data = f.read()

    print(f"Converting {txt_file} to UTF-8-BOM")
    text = data.decode('utf-8')
    data = text.encode('utf-8-sig')

    with open(txt_file, 'wb') as f:
        f.write(data)