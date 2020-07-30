""" The main thing"""

from lxml import etree
from tqdm import tqdm
from pprint import pprint
import time

fileName = "dblp.xml"
parseFileName = "dblp.dtd"
folder = "/media/data6TB/Deshmukh/"

fullpath = folder + fileName

count = 0
authors = []

print("importing")
start = time.time()
parser = etree.XMLParser(dtd_validation=True, load_dtd=True)
Tree = etree.parse(fullpath, parser=parser)
root = Tree.getroot()
end = time.time()
print(f"Done importing, that took a total of {end-start}")

print("looking for the types of tags present")
start = time.time()
typesOfTags = []
for element in root.iter():
    tag = element.tag
    if tag not in typesOfTags:
        typesOfTags.append(tag)
end = time.time()
print(f"There are {len(typesOfTags)} types of tags, they are:")
pprint(typesOfTags)
print(f"An itteration through the whole xml takes about {end-start}")


# for event, elem in tqdm(etree.iterparse(fullpath, load_dtd=True)):
#     # if elem.tag not in ["article", "inproceedings", "proceedings"]:
#     #     continue
#     elemAuthors = elem.findall("author")
#     for elemAuthor in elemAuthors:
#         if elemAuthor.text not in authors:
#             print(elemAuthor.text)
#             authors.append(elemAuthor.text)

#     elem.clear()
# pprint(authors)
# print(f"that is a total of {len(authors)} authors")


# for event, elem in lxml.etree.iterparser(fullpath, load_dtd="True"):
#     if elem.tag not in ['article', 'inproceedings', 'proceedings']:
#         continue

#     title = elem.find('title')
#     year = elem.find('year')
#     authors = elem.find('author')
#     venue = elem.find('venue')
