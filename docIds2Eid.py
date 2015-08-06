#!/usr/local/bin/python3

from sys import argv

import requests
import json
from pprint import pprint

def getDoc(id):
    from_url='http://localhost:8080/solr/admin/luke?docId=%d&wt=json' % id
    print(from_url)
    res = requests.get(from_url)
    return json.loads(res.text)['doc']

if __name__ == '__main__':
    docIds = [int(i) for i in argv[1].split(',')]
    eid = argv[2]
    count = 0
    total = len(docIds)
    for did in docIds:
        if count % 10 == 0:
            print("\nAttempting %d of %d\n" % (count, total))
        count += 1
        doc = getDoc(did)
        docEid = doc['lucene']['eid']['value']
        print(docEid)
        if docEid == eid:
            pprint(doc)
            print("docId:%d" % did)
            exit()
    print("Not found")

