#!/usr/bin/python

import csv
import json
import os

data_dir = '_data/'

region_dirs = os.listdir(data_dir)
json_files = []
for region_dir in region_dirs:
  json_files.extend(map(lambda x: data_dir + os.path.join(region_dir, x), os.listdir(data_dir + region_dir)))
print json_files
write_file = open('people.csv','w')
writer = csv.writer(write_file)
for json_file in filter(lambda x: 'person' in x, json_files):
  with open(json_file) as f:
    content = "".join(f.read())
    person = json.loads(content)
    name = person['name']
    birth_date = person['birth_date']
    image = person['image']
    source1 = person['sources'][1]['url']
    writer.writerow([s.encode('utf-8') for s in [name, birth_date, image, source1]])
write_file.close()
