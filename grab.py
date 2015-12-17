from sys import argv

import requests
import json
from pprint import pprint

to_host='localhost'

known_hosts = {'CERT' : 'ec2-54-89-218-222.compute-1.amazonaws.com',
               'CSPC' : 'ec2-184-73-39-189.compute-1.amazonaws.com',
               'CERT-SP': 'ec2-54-167-178-134.compute-1.amazonaws.com',
               'CERT-FR': 'ec2-54-147-196-177.compute-1.amazonaws.com',
               'CERT-G': 'ec2-54-161-224-213.compute-1.amazonaws.com'}

handler = 'select'

def fetch(from_host, query):
    from_url='http://%s:8080/solr/ck/%s?%s&fl=*&wt=json' % (from_host, handler, query)
    print from_url
    res = requests.get(from_url)
    if res.status_code == 200:
        return json.loads(res.text)['response']['docs']
    else:
        print "Received status code %s for request %s" % (res.status_code, from_url)
        exit()

def post(stuff):
    to_url = 'http://%s:8080/solr/ck/update/json?commit=true' % to_host
    print 'About to post'
    res = requests.post(to_url, json.dumps(stuff))
    print res.status_code
    if res.status_code != 200:
        print res.text

if __name__ == '__main__':
    from_host, q, start, batch_size, end = argv[1:]
    start, batch_size, end = int(start), int(batch_size), int(end)
    for s in range(start, end, batch_size):
        query = q + "&start=%s" % s
        query += "&rows=%s" % batch_size
        stuff = fetch(from_host,query)
        print "Received %d results." % len(stuff)
        if len(stuff) == 0:
            exit()
        post(stuff)
        if len(stuff) < batch_size:
            print "Last results were less than requested, exiting"
            exit()
        if len(stuff) == 1:
            pprint(stuff)
