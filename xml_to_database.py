import xmltodict
import dataset
import tqdm
import os
import json


def get_part_info(filename):
    with open(filename, "r") as f:
        try:
            d = xmltodict.parse(f)
        except Exception as err:
            print filename
            raise(err)
    part = d["rsbpml"]["part_list"]["part"]
    part["sequences"] = part["sequences"]["seq_data"]
    for k, v in part.items():
        if isinstance(v, dict):
            part[k] = json.dumps(v)
    if "twins" in part:
        part.pop("twins")
    return part

filename = "./parts_xml/BBa_B0010.xml"

parts_xml_dir = "parts_xml/"
all_xml_files = sorted(os.listdir(parts_xml_dir))
infos = [
    get_part_info(os.path.join(parts_xml_dir, filename))
    for filename in tqdm.tqdm(all_xml_files)
]

IGEM_PARTS_DATABASE = "igem.sqlite"
if os.path.exists(IGEM_PARTS_DATABASE):
    os.remove(IGEM_PARTS_DATABASE)
database = dataset.connect(
    'sqlite:///' + IGEM_PARTS_DATABASE
)
table = database.create_table("parts")
table.insert_many(infos)
