""" The main thing"""

import multiprocessing as mp

from lxml import etree
import time

from database import database
import list_splitter
from variables import (
    folder,
    fileName,
    postgres_username,
    postgres_password,
    postgres_dbname,
    number_of_threads,
)


super_start = time.time()
# connection to postgres database
print(f"Starting connection with the database {postgres_dbname}...")
start = time.time()
db = database(postgres_dbname, postgres_username, postgres_password)
end = time.time()
print(f"Connecting to database took: {end - start}")

# importing xml file
print("Importing xml file...")
start = time.time()
parser = etree.XMLParser(dtd_validation=True, load_dtd=True)
Tree = etree.parse(folder + fileName, parser=parser)
root = Tree.getroot()
end = time.time()
print(f"Importing xml took: {end - start}")

# setting up the tables and stuff
print("Setting up the database")
start = time.time()
db.setup(verbose=True)
db.close()
end = time.time()
print(f"Setting database tables took: {end - start}")

# splitting the list
print("Splitting lists")
start = time.time()
root_parts = list_splitter.split(root, number_of_threads)
end = time.time()
print(f"Splitting xml doc into {number_of_threads} parts took: {end-start}")

# engulfing splits into <root></root>
# def shell(root_part):
#     root_shell = etree.Element("root")
#     for element in root_part:
#         root_shell.append(element)
#     return root_shell

# shelled_roots = []
# for root_part in root_parts:
#     shelled_roots.append(shell(root_part))

# scraping data
print("Starting scraping")
start = time.time()


def scrape(n):
    scrape_root = root_parts[n]
    db = database(postgres_dbname, postgres_username, postgres_password)
    for element in scrape_root:
        publicationKey = element.get("key")
        publicationTitle = ""
        publicationYear = -1

        for subElement in element:
            # removing \' coz they can mess things up
            try:
                value = subElement.text.replace("'", "")
            except Exception:
                value = subElement.text
            tag = subElement.tag
            if tag == "cite":
                db.addCitation(value, publicationKey)
            elif tag == "author":
                db.addAuthorNAuthorship(value, publicationKey)
            elif tag == "title":
                publicationTitle = value
            elif tag == "year":
                publicationYear = int(subElement.text)
            else:
                continue
        # adding publication
        db.addPublication(
            publicationTitle, publicationKey, publicationYear, element.get("publtype"),
        )
    db.close()


pool = mp.Pool(processes=number_of_threads)
pool.map(scrape, range(number_of_threads))

end = time.time()
print(f"Scraping and feeding data took: {end - start}")

# clean up
print("Closing connections...")
super_end = time.time()

print(
    f"""DONE, feel free to checkout the guts of your lovely database
    XML file: {folder + fileName}
    Spread across: {number_of_threads} threads
    Total time: {super_end - super_start}
"""
)
