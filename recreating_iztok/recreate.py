import networkx as nx
import matplotlib.pyplot as plt
from helpers import parse_manifest, Author, Publication
from tqdm import tqdm
import json
from icecream import ic
from datetime import datetime

DATA_PATH = "./data/"

def main(manifest_path):
    start = datetime.now()
    file_names = parse_manifest(manifest_path)
    publication_graph = nx.DiGraph()
    # authors = []
    publications = []
    starting_loop = datetime.now()
    for path in tqdm(file_names):
        with open(DATA_PATH + path) as data_file:
            publication_jsons = list(map(lambda x: json.loads(x), data_file.readlines()))

        # parsing it
        # - into publication objects
        # - into graph
        for publication in publication_jsons:
            publication_graph.add_node(publication["id"])
            publications.append(Publication(publication))

            for out_citation in publication["outCitations"]:
                publication_graph.add_edge(publication["id"], out_citation)

            for in_citation in publication["inCitations"]:
                publication_graph.add_edge(in_citation, publication["id"])
    end = datetime.now()
    print("Everything is loaded into memory")
    print(f"started at {start}")
    print(f"initiate loop at {starting_loop} - {starting_loop - start}")
    print(f"Loop ends at {end} - {end - starting_loop}")



if __name__ == "__main__":
    main("./data/mini-manifest.txt")
