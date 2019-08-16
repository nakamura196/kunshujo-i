import glob
import numpy
import json
import urllib.request
import csv
from hashlib import md5
import os
import requests
import shutil

collection_url = "https://kunshujo.dl.itc.u-tokyo.ac.jp/data/data.json"

response = urllib.request.urlopen(collection_url)
response_body = response.read().decode("utf-8")
curations = json.loads(response_body)

map = {}

for i in range(len(curations)):

    if i % 10 == 0:
        print(str(i+1)+"/"+str(len(curations)))

    obj = curations[i]

    curation_url = obj["http://purl.org/dc/terms/relation"][0]["@id"]
    volume = obj["http://purl.org/ontology/bibo/volume"][0]["@value"]

    if volume not in map:
        map[volume] = {
            "members": {}
        }

    new_members = map[volume]["members"]

    response = urllib.request.urlopen(curation_url)
    response_body = response.read().decode("utf-8")
    curation = json.loads(response_body)

    selections = curation["selections"]

    for selection in selections:
        members = selection["members"]

        for member in members:

            id = member["@id"]

            page = int(id.split("/canvas/p")[1].split("#")[0])
            index = int(member["label"].split("-")[-1])

            if page not in new_members:
                new_members[page] = {}

            obj = new_members[page]

            if index not in obj:
                obj[index] = []

            obj[index].append(member)

        if "within" not in map[volume]:
            map[volume]["within"] = selection["within"]

for volume in map:
    members = map[volume]["members"]

    id = str(volume).zfill(3)

    curation = {
        "@context": [
            "http://iiif.io/api/presentation/2/context.json",
            "http://codh.rois.ac.jp/iiif/curation/1/context.json"
        ],
        "@id": "https://nakamura196.github.io/kunshujo-i/curation/manual/"+id+".json",
        "@type": "cr:Curation",
        "label": "Curating list",
        "selections": [
            {
                "@id": "https://nakamura196.github.io/kunshujo-i/curation/manual/"+id+".json/range1",
                "@type": "sc:Range",
                "label": "Manual curation by IIIF Curation Viewer",
                "members": [],
                "within": map[volume]["within"]
            }
        ]
    }

    for page in sorted(members):
        for index in sorted(members[page]):
            for uri in members[page][index]:
                curation["selections"][0]["members"].append(uri)

    with open('../docs/curation/manual/'+id+'.json', 'w') as outfile:
        json.dump(curation, outfile, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))
