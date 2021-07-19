from icecream import ic
def parse_manifest(path):
    """Takes in a manifest_file_path and returns the list of files from it"""
    # parsing the manifest file
    with open(path) as manifest_file:
        file_names = manifest_file.readlines()[:-2]

    # cleaning name
    file_names = list(map(lambda x: x[:-4], file_names))

    return file_names


class Author():
    def __init__(self, ids: list, name: str):
        self.ids = ids
        self.name = name

    def __str__(self):
        return f"{self.name}: {self.ids}"

    def add_id(self, new_id):
        self.ids = list(set(self.ids + [new_id]))

class Publication():
    def __init__(self, json):
        self.id = json["id"]
        self.title = json["title"]
        self.year = json["year"]
        self.fields_of_study = json["fieldsOfStudy"]

    def __str__(self):
        return f"{self.title} | {self.fields_of_study} - self.year"

