#!/usr/bin/python
computers = "/Users/adam/Dropbox/Music Transfer/computers.pickle"

import pickle
from pprint import pprint

with open(computers, 'rb') as f:
    p = pickle.load(f)

p['melatonin'] = p['fasttrack'] 
pprint(p)

with open(computers, 'wb') as f:
    pickle.dump(p,f)
