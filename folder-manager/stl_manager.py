import zipfile
from pathlib import Path
from shutil import copyfile, rmtree, move, copy
import os
from argparse import ArgumentParser
from collections import OrderedDict
from functools import wraps


default_map = OrderedDict(
    [
        ("pdf", "./BOOKs"),
        ("mobi", "./BOOKs"),
        ("epub", "./BOOKs"),
        ("mp3", "./TUNEs"),
        ("gba", "./ROMs"),
        ("stl", "./STLs"),
    ]
)


def handle_it(func):
    @wraps(func)
    def handled_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f">>> Unable to process {args[0]} with {func.__name__}")
            print(f">>> Exception: {e}")

    return handled_func


@handle_it
def unzip_and_move(
    zipped_file, alt_dir="../", file_types=default_map, exclude=True, delete=True
):
    category = "alt"
    output_name = zipped_file.split(".")[0]
    base_folder = Path(zipped_file).parent
    output = base_folder / output_name
    with zipfile.ZipFile(zipped_file, "r") as zip:
        zip.extractall(output)
    for file_type in file_types:
        proper_files = set(output.rglob(f"*.{file_type}"))
        if len(proper_files) > 0:
            category = file_type
            if exclude:
                for file_s in output.rglob("*"):
                    new_file = Path(file_types[file_type]) / output_name.replace(
                        "+", "-"
                    )
                    if not os.path.isdir(new_file):
                        os.mkdir(new_file)
                    if file_s in proper_files:
                        if file_s.parent != output:
                            print(f"    > > > Extracting {file_s}")
                            move(file_s, new_file / file_s.name)
                rmtree(output)
    if category == "alt":
        if output.parent != Path(alt_dir):
            print(f"    > > > Moving {output} to {alt_dir}")
            move(output, alt_dir)
    if delete:
        os.remove(zipped_file)


@handle_it
def individual_move(file_path, file_types=default_map):
    file_type = file_path.name.split(".")[-1]
    if file_type in file_types:
        if file_path.parent != Path(file_types[file_type]):
            print(
                f"    > > > Moving {file_path.name} to {Path(file_types[file_type]).absolute()}"
            )
            move(file_path, Path(file_types[file_type]))
            os.remove(file_path)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="File to unzip and remove.")
    args = parser.parse_args()

    if args.file.split(".")[0] == "zip":
        unzip_and_move(args.file)
    else:
        individual_move(args.file)
