import glob
import json

map = {
    "ndl": "automatic/ndl",
    "utokyo": "automatic/utokyo",
    "manual": "manual"
}

uni = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": "https://nakamura196.github.io/kunshujo-i/collection/collection_m.json",
    "@type": "cr:Collection",
    "label": "貼り込み資料画像検索プロトタイプ",
    "collections": []
}

################

manual_labels = []
files = glob.glob("../docs/curation_m/manual/*.json")
for file in files:
    with open(file) as f:
        df = json.load(f)

    if "@label" in df["selections"][0]["within"]:
        label = df["selections"][0]["within"]["@label"]
    else:
        label = df["selections"][0]["within"]["label"]
    manual_labels.append(label)

################

for key in map:
    files = glob.glob("../docs/curation_m/"+map[key]+"/*.json")

    collection = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": "https://nakamura196.github.io/kunshujo-i/collection/"+key+"_m.json",
        "@type": "cr:Collection",
        "label": key,
        "curations": []
    }

    uni["collections"].append({
        "@id": "https://nakamura196.github.io/kunshujo-i/collection/"+key+"_m.json",
        "@type": "cr:Collection",
        "label": key
    })

    for file in files:
        with open(file) as f:
            df = json.load(f)

        print(file)

        if "@label" in df["selections"][0]["within"]:
            label = df["selections"][0]["within"]["@label"]
        else:
            label = df["selections"][0]["within"]["label"]

        ### Manualラベルに含まれていない場合のみ
        if key == "manual" or label not in manual_labels:

            curation_obj = {
                "@context": "http://iiif.io/api/presentation/2/context.json",
                "@id": df["@id"],
                "@type": "cr:Curation",
                "label": label
            }
            collection["curations"].append(curation_obj)

    with open("../docs/collection/"+key+"_m.json", 'w') as f:
        json.dump(collection, f, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))

with open("../docs/collection/collection_m.json", 'w') as f:
    json.dump(uni, f, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
