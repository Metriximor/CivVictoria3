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
    Path("release"),
    Path("docs"),
]
disallowed_extensions = [".spec", ".lnk", ".psd", ".pdn", ".gitignore", ".dvc"]
disallowed_files = ["tasklist.txt", "docs.md"]
folders_to_keep_pngs: list[Path] = [Path("gfx/map/terrain"), Path("map_data")]

files_to_package = []


def compress_files_to_zip(file_list: list[str], zip_file_name: str) -> None:
    total_files = len(file_list)
    files_processed = 0

    with zipfile.ZipFile(
        zip_file_name, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as zipf:
        for file_path in file_list:
            zipf.write(file_path)
            files_processed += 1
            print(f"Progress: {files_processed}/{total_files} files compressed.")

        print("Compression completed.")


def copy_files_to_release_folder(file_paths: list[str], release_folder: str) -> None:
    for file_path in file_paths:
        shutil.copy2(file_path, release_folder)


for file in glob.iglob("./**/*", recursive=True):
    path = Path(file)
    is_disallowed_folder = any(
        disallowed_folder == path for disallowed_folder in folders_to_not_copy
    )
    is_inside_disallowed_folder = any(
        disallowed_folder in path.parents for disallowed_folder in folders_to_not_copy
    )
    if is_inside_disallowed_folder or is_disallowed_folder:
        continue
    has_disallowed_extension = any(
        file.endswith(disallowed_extension)
        for disallowed_extension in disallowed_extensions
    )
    if has_disallowed_extension:
        continue
    file_is_png = path.suffix == ".png"
    png_is_in_allowed_folder = any(
        allowed_folder in path.parents for allowed_folder in folders_to_keep_pngs
    )
    if file_is_png and not png_is_in_allowed_folder:
        continue
    is_disallowed_file = any(
        file.endswith(disallowed_file) for disallowed_file in disallowed_files
    )
    if is_disallowed_file:
        continue
    files_to_package.append(file)


compress_files_to_zip(files_to_package, "src/output/release.zip")
