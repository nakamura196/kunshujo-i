import glob
import json
import os
from hashlib import md5
#coding:utf-8
from googletrans import Translator
translator = Translator()

map = {}

files = glob.glob("/Users/nakamura/git/d_utda/kunshujo-i/src/gcv/od/*.json")
result = {}
for file in files:
    with open(file) as f:
        id = os.path.basename(file).split(".")[0]
        result[id] = []
        df = json.load(f)

        checks = []

        for obj in df:

            label = obj["label"]

            print(label)

            if label not in map:
                try:
                    map[label] = translator.translate(label, src='en' ,dest='ja').text
                except Exception as e:
                    print(e)
                    map[label] = label

            label = map[label]
            print(label)
            print("--------")

            if label not in checks:
                
                result[id].append({
                    "label" : "機械タグ",
                    "value" : label
                })

                checks.append(label)



files = glob.glob("/Users/nakamura/git/d_utda/kunshujo-i/docs/curation_m/**/*.json", recursive=True)

dir = "/Users/nakamura/git/d_utda/kunshujo-i/docs/data"

for file in files:
    print(file)

    filename = os.path.basename(file)

    print(filename)

    with open(file) as f:
        df = json.load(f)
        manifest = df["selections"][0]["within"]["@id"]
        if "u-tokyo" in manifest:
            uuid = manifest.split("/")[5]
            manifest = "https://archdataset.dl.itc.u-tokyo.ac.jp/manifest/"+uuid+".json"
            df["selections"][0]["within"]["@id"] = manifest

        curation_uri = "https://nakamura196.github.io/kunshujo-i/data/"+filename

        df["@id"] = curation_uri

        members = df["selections"][0]["members"]

        for member in members:
            member_id = member["@id"]
            hash = md5(member_id.encode('utf-8')).hexdigest()
            if hash in result:
                metadata = member["metadata"]
                for obj in result[hash]:
                    metadata.append(obj)


        f = open(dir+"/" + filename, "w")
        json.dump(df, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


print(result)