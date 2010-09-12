#!/usr/bin/python
computers = "/Users/adam/Dropbox/Music Transfer/computers.pickle"

import pickle
from pprint import pprint

with open(computers, 'rb') as f:
    p = pickle.load(f)

p['cuttooth'] = p['fasttrack'] = p['melatonin'] = {} 
pprint(p)

with open(computers, 'wb') as f:
    pickle.dump(p,f)
