from publication import Publication, PublicationManager
from helpers import parse_manifest_file, DATA_DIR
from tqdm import tqdm


def main():

    file_names = parse_manifest_file()
    publication_manager = PublicationManager()

    for file_name in tqdm(file_names, desc="reading files"):
        with open(DATA_DIR + file_name) as f:
            data_string = f.readlines()
        print(len(data_string))
        for line in tqdm(data_string, desc="parsing file"):
            publication = Publication()
            publication.populate_from_string(line)
            publication_manager.calculate_score_for(publication.id)
    print(set(publication_manager.publications))
    publication_manager.close()


if __name__ == "__main__":
    main()
