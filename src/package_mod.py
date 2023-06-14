import glob
import zipfile
import os
import shutil
from pathlib import Path

folders_to_not_copy: list[Path] = [
    Path(".vscode"),
    Path("build"),
    Path("dist"),
    Path("src"),
    Path("tools"),
    Path("__pycache__"),
    Path("gfx/editor_terrain"),
    Path("content_source"),
    Path("release")
]
disallowed_extensions = [
    ".spec",
    ".lnk",
    ".psd",
    ".pdn",
    ".gitignore",
    ".dvc"
]
disallowed_files = [
    "tasklist.txt"
]
folders_to_keep_pngs: list[Path] = [
    Path("gfx/map/terrain"),
    Path("map_data")
]

files_to_package = []


def compress_to_zip(source_folder: str, zip_file: str) -> None:
    with zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(
                    file_path, source_folder))


def copy_files_to_release_folder(file_paths: list[str], release_folder: str) -> None:
    for file_path in file_paths:
        shutil.copy2(file_path, release_folder)


for file in glob.iglob("./**/*", recursive=True):
    path = Path(file)
    is_disallowed_folder = any(
        disallowed_folder == path for disallowed_folder in folders_to_not_copy)
    is_inside_disallowed_folder = any(
        disallowed_folder in path.parents for disallowed_folder in folders_to_not_copy)
    if is_inside_disallowed_folder or is_disallowed_folder:
        continue
    has_disallowed_extension = any(file.endswith(
        disallowed_extension) for disallowed_extension in disallowed_extensions)
    if has_disallowed_extension:
        continue
    file_is_png = path.suffix == ".png"
    png_is_in_allowed_folder = any(
        allowed_folder in path.parents for allowed_folder in folders_to_keep_pngs)
    if file_is_png and not png_is_in_allowed_folder:
        continue
    is_disallowed_file = any(file.endswith(disallowed_file)
                             for disallowed_file in disallowed_files)
    if is_disallowed_file:
        continue
    files_to_package.append(file)


release_folder = "/release"
copy_files_to_release_folder(files_to_package, release_folder)
compress_to_zip(release_folder, f"{release_folder}/release.zip")
