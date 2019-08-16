import glob
import json

files = glob.glob("../docs/curation_bk/*.json")

for file in files:
    with open(file) as f:
        df = json.load(f)

    print(file)

    for selection in df["selections"]:
        label = selection["within"]["label"]

        attribution = "utokyo"

        if "張交帖" in label:
            attribution = "ndl"

        selection["@id"] = selection["@id"].replace("lire", "kunshujo-i").replace("curation", "curation/automatic/"+attribution)

    df["@id"] = df["@id"].replace(
        "lire", "kunshujo-i").replace("curation", "curation/automatic/"+attribution)

    with open(file.replace("curation_bk", "curation/automatic/"+attribution), 'w') as f:
        json.dump(df, f, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))






