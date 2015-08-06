#!/usr/local/bin/python3

import sys

import requests
import json

localhost = 'localhost'

def delete(from_host, query):
    del_query = '<delete><query>%s</query></delete>' % query
    from_url='http://%s:8080/solr/update' % from_host
    print("%s -- %s" % (from_url, del_query))
    res = requests.post(from_url, del_query)
    requests.post(from_url, '<commit>')
    print("Tried to delete")
    return res.text

if __name__ == '__main__':
    q = sys.argv[1]
    host = sys.argv[2] if len(sys.argv) > 2 else localhost
    if "=" in q:
        print("%s is invalid as a delete query" % q)
        exit()
    stuff = delete(host, q)
    print(stuff)

