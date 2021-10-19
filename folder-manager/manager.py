from argparse import ArgumentParser
import os
import glob
from stl_manager import unzip_and_move, default_map, individual_move


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--folder", type=str, help="Folder to monitor.")
    args = parser.parse_args()

    if args.folder:
        os.chdir(args.folder)

    original_files = set(glob.glob("*"))
    while True:
        latest_files = set(glob.glob("*"))
        file_diff = latest_files - original_files
        if len(file_diff) > 0:
            print(f"parsing_new_files: {file_diff}")
            for new_file in file_diff:
                if new_file.split(".")[-1] == "zip":
                    unzip_and_move(new_file)
                elif new_file.split(".")[-1] in default_map:
                    individual_move(new_file)
            original_files = set(glob.glob("*"))
