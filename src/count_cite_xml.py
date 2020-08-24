"""Counting the number of time cite key work shows up in the xml file
"""
import os
from variables import folder, fileName

full_path = folder + fileName

print(f'File Size is {os.stat(full_path).st_size / (1024 * 1024)} MB')

txt_file = open(full_path)

count = 0
cite_count = 0

for line in txt_file:
    if line.find("cite") != -1:
        cite_count += 1
    count += 1

txt_file.close()

print(f'Number of Lines in the file is {count}')
print(f'Number of line with thr word cite in it is {cite_count}')
