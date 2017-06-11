#!/bin/env python2.7

# key to address ecc example



import pybitcointools

valid_private_key = False

while not valid_private_key:
    private_key = pybitcointools.random_key()
    decoded_private_key = pybitcointools.decode_privkey(private_key, 'hex')
    valid_private_key = 0 < decoded_private_key < pybitcointools.N

print "Private Key (hex) is:                    ", private_key
print "Private Key (decimal) is:                ", decoded_private_key

wif_encoded_private_key = pybitcointools.encode_privkey(decoded_private_key, 'wif')
print "Private Key (wif) is:                    ", wif_encoded_private_key
print ""

compressed_private_key = private_key + '01'
print "Private Key compressed (hex) is:         ", compressed_private_key

wif_compressed_compressed_private_key = pybitcointools.encode_privkey(
    pybitcointools.decode_privkey(compressed_private_key, 'hex'), 'hex'
)

print "Private Key (WIF-Compressed) is:         ", wif_compressed_compressed_private_key
print ""

# < fast_multiply() >   replace   < base10_multiply() >
public_key = pybitcointools.fast_multiply(pybitcointools.G, decoded_private_key)
print "Public Key (x,y) coordiates is:\n", public_key
print ""

hex_encoded_public_key = pybitcointools.encode_pubkey(public_key, 'hex')
print "Public Key (hex) is:                     ", hex_encoded_public_key
print ""

(public_key_x, public_key_y) = public_key
if (public_key_y % 2) == 0:
    compressed_prefix = '02'
else:
    compressed_prefix = '03'
hex_compressed_public_key = compressed_prefix + pybitcointools.encode(public_key_x, 16)
print "Compressed Public Key (hex) is:          ", hex_compressed_public_key
print ""

print "Compressed Bitcoin Adress (b58check) is: ", pybitcointools.pubkey_to_address(hex_compressed_public_key)
print ""