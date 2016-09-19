"""Downloads all iGEM parts xml."""

import json
import os
import urllib2
import tqdm
import time
import xmltodict


parts_names_json = "./igemparts.json"
XML_DIR = "parts_xml"

with open(parts_names_json) as fp:
    parts_names = [
        part["name"]
        for part in json.load(fp)
    ]
parts_names = sorted(list(set(parts_names)))  # uniquify the list
n_parts = len(parts_names)
print "Found %d parts. first part: %s" % (n_parts, parts_names[0])

IGEM_API_BASE = "http://parts.igem.org/cgi/xml/part.cgi?part="
if not os.path.exists(XML_DIR):
    os.mkdir(XML_DIR)

def partname_to_filename(part_name):
    return os.path.join(XML_DIR, part_name + ".xml")


def download_infos(part_name, overwrite=False, sleep=0.2):
    """Download an iGEM part as an XML file."""
    filename = partname_to_filename(part_name)
    if os.path.exists(filename) and not overwrite:
        return
    time.sleep(0.2)
    url = IGEM_API_BASE + part_name
    # print url
    try:
        response = urllib2.urlopen(url)
        assert response.getcode() == 200
        xml = response.read()
        with open(filename, "w+") as f:
            f.write(xml)
    except:
        print ("could not download part " + part_name)


def test_xml(filename):
    """ Raise an exception if the xml file is ill-formed."""
    with open(filename, "r") as f:
        d = xmltodict.parse(f)
    return d["rsbpml"]["part_list"]["part"]

blacklist = []
for i, part_name in enumerate(parts_names):
    print (part_name, "%.01f" % (100.0*i/n_parts))
    try:
        download_infos(part_name, overwrite=False)
        test_xml(partname_to_filename(part_name))
    except:
        blacklist.append(part_name)


print ("%d parts could not be downloaded or were corrupted" % len(blacklist))
print ("Rerun this script to retry on these parts.")

for part_name in blacklist:
    filename = partname_to_filename(part_name)
    print part_name
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("not found")
