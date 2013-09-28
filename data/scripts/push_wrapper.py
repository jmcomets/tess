#!/usr/bin/python

import os;
import re;
import json;
import requests;

for fname in os.listdir('wrappers'):
    if not re.match('.*\.json',fname):
        continue
    with open("wrappers/{}".format(fname)) as data:
        oid = json.loads(data.read())["_id"]
        requests.post("http://92.39.246.129:9200/crawl/wrapper/{}".format(oid))


