#!/usr/bin/python

import os
import re
import json
import requests

for fname in os.listdir('../wrappers'):
    if not re.match('.*\.json',fname):
        continue
    print fname
    with open("../wrappers/{}".format(fname)) as data:
        pattern = json.loads(data.read())
        oid = pattern["_id"]
        pattern_dump = json.dumps(pattern)
        requests.post("http://92.39.246.129:9200/crawl/wrapper/{}".format(oid), data=pattern_dump)


