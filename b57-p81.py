#!/bin/env python2.7

# pycoin_example.py

from pycoin.key import Key
from pycoin.key.validate import is_address_valid, is_wif_valid
from pycoin.services import spendables_for_address
from pycoin.tx.tx_utils import create_tx, sign_tx


def get_address(which):
    while 1:
        print "enter the %s address=> " % which,
        address = raw_input()           # input() >> raw_input()
        is_valid = is_address_valid(address)
        if is_valid:
            return address
        print "invalid address, please try again"

src_address = get_address("source")
spendables = spendables_for_address(src_address, "BTC", "text")
print spendables

while 1:
    print "enter the WIF for %s=> " % src_address,
    wif = raw_input()                   # input() >> raw_input()
    is_valid = is_wif_valid(wif)
    if is_valid:
        break
    print "invalid wif, please try again"

key = Key.from_text(wif)
if src_address not in (key.address(use_uncompressed=False), key.address(use_uncompressed=True)):
    print "** wif doesn't correspond to %s" % src_address

print "The secret exponent is %d" % key.secret_exponent()

dst_address = get_address("destination")

tx = create_tx(spendables, payables=[dst_address])
print tx
sign_tx(tx, wifs=[wif])
print tx

print "here is the singed output transaction"
print tx.as_hex()
