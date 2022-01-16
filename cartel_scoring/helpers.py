def parse_manifest_file():
    with open(DATA_DIR + "mini-manifest.txt") as manifest_file:
        file_names = manifest_file.readlines()[:-2]
    file_names = list(map(lambda x: x[:-4], file_names))
    return file_names

DATA_DIR = "../data/"


def string_set(string_list):
    """a set function for string list"""
    print(f"mashing {string_list}")
    return list(dict.fromkeys(string_list))
