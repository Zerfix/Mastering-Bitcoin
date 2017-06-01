from pycoin.key import Key
from pycoin.key.validate import is_address_valid, is_wif_valid
from pycoin.services import spendables_for_address
from pycoin.tx.tx_utils import create_signed_tx


def get_adress(whitch):
    while 1:
        print("enter the %s address=> " % whitch, end='')
        address = input()
        is_valid = is_address_valid(address)
        if is_valid:
            return address
        print("invalid address, please try again")

src_address = get_adress("source")
spendables = spendables_for_address(src_address)
print(spendables)

while 1:
    print("enter the WIF for %s=> " % src_address, end='')
    wif = input()
    is_valid = is_wif_valid(wif)
    if is_valid:
        break
    print("invalid wif, please try again")

key = Key.from_text(wif)
if src_address not in (key.address(use_uncompressed=False), key.address(use_uncompressed=True)):
    print("** wif doesn't correspond to %s" % src_address)

print("The secret exponent is %d" % key.secret_exponent())

dst_adress = get_adress("destination")

tx = create_signed_tx(spendables, payables=[dst_adress], wifs=[wif])

print("here is the singed output transaction")
print(tx.as_hex())
