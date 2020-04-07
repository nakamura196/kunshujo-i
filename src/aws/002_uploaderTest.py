import sys
from classes import uploader
import csv
import glob
import json
import requests
import hashlib
import os
from hashlib import md5

INDEX = "kunshujo_items"
HOST = 'search-nakamura196-rgvfh3jsqpal3gntof6o7f3ch4.us-east-1.es.amazonaws.com'
REGION = 'us-east-1'
PROFILE_NAME = 'default'

files = glob.glob("/Users/nakamura/git/d_utda/kunshujo-i/docs/data/*.json")
files = sorted(files)

all_bodies = []

for file in files:
    with open(file) as f:
        df = json.load(f)
        members = df["selections"][0]["members"]

        curation_uri = df["@id"]

        for i in range(len(members)):
            member = members[i]
            member_id = member["@id"]
            hash = md5(member_id.encode('utf-8')).hexdigest()

            body = {
                "_type" : "_doc",
                "_index" : INDEX,
                "_id": hash,
                "_image": [member["thumbnail"]],
                "_title": [member["label"]],
                "_url": ["http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?curation="+curation_uri+"&pos="+str(i+1)],
            }

            metadata = member["metadata"]
            for obj in metadata:
                label = obj["label"]
                value = obj["value"]

                if label not in body:
                    body[label] = []
                if value not in body[label]:
                    body[label].append(value)

            all_bodies.append(body)

uploader.Uploader.main(
    index=INDEX, 
    host=HOST, 
    region=REGION, 
    profile_name=PROFILE_NAME, 
    all_body=all_bodies)
