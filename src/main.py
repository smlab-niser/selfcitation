""" The main thing"""

from lxml import etree
from tqdm import tqdm

from database import database
from variables import (
    folder,
    fileName,
    postgres_username,
    postgres_password,
    postgres_dbname,
)


fullPath = folder + fileName

# connection to postgres database
print(f"Starting connection with the postgres database {postgres_dbname}...")
db = database(postgres_dbname, postgres_username, postgres_password)

# importing xml file
print("Importing xml file...")
parser = etree.XMLParser(dtd_validation=True, load_dtd=True)
Tree = etree.parse(fullPath, parser=parser)
root = Tree.getroot()
print("XML file has been imported")

# setting up the tables and stuff
print("Setting up the database")
db.setup(verbose=True)
print("Done")

# scraping data
print("Starting scraping")
for element in tqdm(root):
    publicationKey = element.get("key")
    publicationTitle = ""
    publicationYear = -1

    for subElement in element:
        # removing \' coz they can mess things up
        try:
            value = subElement.text.replace("'", "")
        except Exception:
            value = subElement.text
        if subElement.tag == "cite":
            db.addCitation(value, publicationKey)
        elif subElement.tag == "author":
            db.addAuthorNAuthorship(value, publicationKey)
        elif subElement.tag == "title":
            publicationTitle = value
        elif subElement.tag == "year":
            publicationYear = int(subElement.text)
        else:
            continue
    # adding publication
    db.addPublication(
        publicationTitle, publicationKey, publicationYear, element.get("publtype")
    )


# clean up
print("Closing connections...")
db.close()

print("DONE, feel free to checkout the guts of your lovely database")
