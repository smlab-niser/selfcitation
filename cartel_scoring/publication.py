from collections import Counter
from functools import reduce
import json
from helpers import parse_manifest_file, DATA_DIR, string_set


class PublicationManager:
    def __init__(self):
        self.publications = []
        self.file = open("Datafile.csv", "a")

    def clean_publications(self):
        # emptying the list
        self.publications = []

    def add_publication(self, publication):
        # checking if we already have it else we move on
        for publication_ in self.publications:
            if publication_ == publication:
                return
        self.publications.append(publication)

    def find_publication_in_manager(self, publication):
        """Look for publications in the case"""
        for publication_ in self.publications:
            if publication_.id == publication.id:
                return True
        return False

    def get_publication(self, publication_id):
        """look for publication in cache, if not found then load up new ones"""
        for publication in self.publications:
            if publication.id == publication_id:
                return publication
        publication = Publication(publication_id)
        publication.populate()
        self.publications.append(publication)
        return publication

    def get_author_ids(self, publication_id):
        """Get the author ids of a publication"""
        publication = self.get_publication(publication_id)
        return publication.author_ids

    def is_interdisciplinary(self, first_id, second_id):
        """Checks if the publications from the two author ids have a common field of study"""
        first_publication_fos = self.get_publication(first_id).field_of_studies
        second_publication_fos = self.get_publication(second_id).field_of_studies
        return len([value for value in first_publication_fos if value in second_publication_fos]) == 0

    def calculate_score_for(self, publication_id):
        """The fucking algorithm, and adds rows to the data file"""
        publication = self.get_publication(publication_id)
        if publication.isolated_paper:
            return
        # get ids of citee authors
        citee_authors = []
        interdisciplinary_citee_authors = []
        for citee_publication_id in publication.citee_publication_ids:
            citee_authors.append(self.get_author_ids(citee_publication_id))
            if self.is_interdisciplinary(
                    publication.id, citee_publication_id
            ):
                interdisciplinary_citee_authors.append(
                    self.get_author_ids(citee_publication_id)
                )

        # get ids of citer authors
        citer_authors = []
        interdisciplinary_citer_authors = []
        for citer_publication_id in publication.citer_publication_ids:
            citer_authors.append(self.get_author_ids(citer_publication_id))
            if self.is_interdisciplinary(
                    publication.id, citer_publication_id
            ):
                interdisciplinary_citer_authors.append(
                    self.get_author_ids(citer_publication_id)
                )

        # histograming the citee/citer authors
        suspects_ids = string_set(citee_authors + citer_authors)

        citee_authors_counts = Counter(citee_authors)
        citer_authors_counts = Counter(citer_authors)

        interdisciplinary_citee_authors_counts = Counter(
            interdisciplinary_citee_authors
        )
        interdisciplinary_citer_authors_counts = Counter(
            interdisciplinary_citer_authors
        )

        # calculating cartel score and committing it to database
        for suspect_id in suspects_ids:

            # adding to the total score
            for author_id in publication.author_ids:
                self.add_row(
                    from_id=author_id,
                    to_id=suspect_id,
                    citee_count=citee_authors_counts[suspect_id],
                    citer_count=citer_authors_counts[suspect_id],
                    interdisciplinary=False,
                    year=publication.year
                )

            # adding to the interdisciplinary score
            for author_id in publication.author_ids:
                self.add_row(
                    from_id=author_id,
                    to_id=suspect_id,
                    citee_count=interdisciplinary_citee_authors_counts[suspect_id],
                    citer_count=interdisciplinary_citer_authors_counts[suspect_id],
                    interdisciplinary=True,
                    year=publication.year
                )

    def add_row(self, from_id, to_id, citee_count, citer_count, interdisciplinary, year):
        self.file.write(f"{from_id},{to_id},{citee_count},{citer_count},{int(interdisciplinary)},{year}")

    def close(self):
        self.file.close()


class Publication:
    def __init__(
        self,
        ID="",
        author_ids=[],
        citee_publication_ids=[],
        citer_publication_ids=[],
        field_of_studies=[],
        year=0
    ):
        # self.required_keys = ["id", "authors", "outCitations", "inCitations", "fieldsOfStudy", "year"]
        self.isolated_paper = None
        self.id = ID
        self.author_ids = author_ids
        self.citee_publication_ids = citee_publication_ids
        self.citer_publication_ids = citer_publication_ids
        self.field_of_studies = field_of_studies
        self.year = year

    def populate(self):
        """Populate the complete object from the database"""
        file_names = parse_manifest_file()
        for file_name in file_names:
            with open(DATA_DIR + file_name) as f:
                data_string = f.readlines()
            for line in data_string:
                if json.loads(line)["id"] == self.id:
                    self.populate_from_string(line)
                    return
        raise Exception(f"Publication {self.id} not found")

    def populate_from_string(self, line):
        publication = json.loads(line)
        # del line
        print(f"Loading up {publication['authors']}")

        # parsing author ids
        self.author_ids = []
        for authors_ids in list(map(lambda x: x["ids"], publication["authors"])):
            for authors_id in authors_ids:
                self.author_ids.append(authors_id)

        self.id = publication["id"]
        self.citee_publication_ids = publication["outCitations"]
        self.citer_publication_ids = publication["inCitations"]
        self.field_of_studies = publication["fieldsOfStudy"]
        self.year = publication["year"]
        self.isolated_paper = (len(self.citer_publication_ids)+len(self.citee_publication_ids)) == 0

    def __eq__(self, other):
        return self.id == other.id
