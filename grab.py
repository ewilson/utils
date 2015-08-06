#!/usr/local/bin/python3

from sys import argv

import requests
import json
from pprint import pprint

to_host='localhost'

def fetch(from_host, query):
    from_url='http://%s:8080/solr/select?%s&fl=*&wt=json' % (from_host, query)
    print(from_url)
    res = requests.get(from_url)
    if res.status_code == 200:
        return json.loads(res.text)['response']['docs']
    else:
        print("Received status code %s for request %s" % (res.status_code, from_url))
        exit()

def post(stuff):
    to_url = 'http://%s:8080/solr/update/json?commit=true' % to_host
    print('About to post')
    res = requests.post(to_url, json.dumps(stuff))
    print(res.status_code)
    if res.status_code != 200:
        print(res.text)

if __name__ == '__main__':
    from_host, q, *opts = argv[1:]
    start, batch_size, end = [int(o) for o in opts] if opts else (0, 100, 100)
    if batch_size:
        for s in range(start, end, batch_size):
            query = q + "&start=%s" % s
            query += "&rows=%s" % batch_size
            stuff = fetch(from_host,query)
            print("Received %d results." % len(stuff))
            post(stuff)
            if len(stuff) < batch_size:
                print("Last results were less than requested, exiting")
                exit()
            if len(stuff) == 1:
                pprint(stuff)
