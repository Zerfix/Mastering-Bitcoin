#!/bin/env python2.7

# hash_example.py

import hashlib

text = "I am Satoshi Nakamoto"

for nonce in xrange(20):
    input = text + str(nonce)
    hash = hashlib.sha256(input).hexdigest()
    
    print input, "=>", hash