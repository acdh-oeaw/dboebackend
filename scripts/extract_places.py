import glob
from acdh_tei_pyutils.tei import TeiReader
from acdh_xml_pyutils.xml import NSMAP
from csae_pyutils import save_json
from tqdm import tqdm


def main():
    region_types = [
        "Bundesland",
        "Großregion",
        "Kleinregion",
        "Gemeinde",
        "Ort",
    ]

    data = dict()

    files = sorted(glob.glob("./orig-files/*.xml"))
    for x in tqdm(files, total=len(files)):
        doc = TeiReader(x)
        for entry in doc.any_xpath(".//tei:entry[./tei:usg[@type='geo']/tei:listPlace]"):
            place_id = entry.xpath("./tei:usg[@type='geo']/tei:listPlace[@corresp]/@corresp", namespaces=NSMAP)[0]
            data[place_id] = {}
            for y in region_types:
                data[place_id][y] = {}
                try:
                    data[place_id][y]["label"] = entry.xpath(
                        f".//tei:place[@type='{y}']/tei:placeName", namespaces=NSMAP
                    )[0].text
                except IndexError:
                    data[place_id][y]["label"] = False
                try:
                    data[place_id][y]["idno"] = entry.xpath(
                        f".//tei:place[@type='{y}']/tei:idno", namespaces=NSMAP
                    )[0].text
                except IndexError:
                    data[place_id][y]["idno"] = False
    save_json(data, "places.json")


if __name__ == "__main__":
    main()
