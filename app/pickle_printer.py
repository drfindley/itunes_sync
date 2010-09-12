#!/usr/bin/python
computers = "/Users/adam/Dropbox/Music Transfer/music_list.pickle"

import pickle
from pprint import pprint

import sys

if len(sys.argv) < 2:
    print "Please specify the pickle path"
    sys.exit()

fn = sys.argv[1]

with open(fn, 'r') as f:
    p = pickle.load(f)
    pprint(p)
