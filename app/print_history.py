#!/usr/bin/python
computers = "/Users/adam/Dropbox/Music Transfer/history.pickle"

import pickle
from pprint import pprint

with open(computers, 'r') as f:
    p = pickle.load(f)
    pprint(p)
