import os
from argparse import ArgumentParser
from shutil import rmtree, make_archive

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-t", "--text", action="store_true")
    parser.add_argument("-s", "--stl", action="store_true")
    parser.add_argument("-z", "--zip", action="store_true")
    parser.add_argument("-o", "--other", type=str)
    args = parser.parse_args()

    total_file_types = list()
    if args.text:
        total_file_types += ["txt"]
    if args.stl:
        total_file_types += ["stl"]
    if args.other:
        total_file_types += args.other.split(",")

    os.makedirs("./test_folder")
    for file_type in total_file_types:
        os.system(f'echo "test file" > ./test_folder/test_files.{file_type}')

    if args.zip:
        make_archive("test_folder", "zip", "./test_folder")
        rmtree("./test_folder")
