#!/usr/bin/env python
from __future__ import print_function

from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException
from decimal import Decimal
import argparse
import struct
import binascii
from mcBase import Transaction, UnsignedTransaction, unsigned_tx_from_tx
from rlp import encode

# Define here Chain_ID for EIP-155
#CHAIN_ID = 0
CHAIN_ID = 101

try:
    from rlp.utils import decode_hex, encode_hex, str_to_bytes
except:
    #Python3 hack import for pyethereum
    from chain3 import decode_hex, encode_hex, str_to_bytes

def parse_bip32_path(path):
    if len(path) == 0:
        return b""
    result = b""
    elements = path.split('/')
    for pathElement in elements:
        element = pathElement.split('\'')
        if len(element) == 1:
            result = result + struct.pack(">I", int(element[0]))
        else:
            result = result + struct.pack(">I", 0x80000000 | int(element[0]))
    return result


parser = argparse.ArgumentParser()
parser.add_argument('--nonce', help="Nonce associated to the account", type=int, required=True)
parser.add_argument('--gasprice', help="Network gas price", type=int, required=True)
parser.add_argument('--startgas', help="startgas", default='21000', type=int)
parser.add_argument('--amount', help="Amount to send in moac", required=True)
parser.add_argument('--to', help="Destination address", type=str, required=True)
parser.add_argument('--path', help="BIP 32 path to sign with")
parser.add_argument('--data', help="Data to add, hex encoded")
parser.add_argument('--systemflag', help="always 0", default='0', type=int)
parser.add_argument('--shardingflag', help="always 0", default='0', type=int)
parser.add_argument('--via', help="always 0", default='0x0000000000000000000000000000000000000000', type=str)
args = parser.parse_args()

if args.path == None:
    args.path = "44'/60'/0'/0/0"

if args.data == None:
    args.data = b""
else:
    args.data = decode_hex(args.data[2:])

amount = Decimal(args.amount) * 10**18

#print('check "to" ',decode_hex(args.to[2:]))
#via_test="0000000000000000000000000000000000000000"

tx = Transaction(
    nonce=int(args.nonce),
    systemflag=0,
    gasprice=int(args.gasprice),
    startgas=int(args.startgas),
    to=decode_hex(args.to[2:]),
    value=int(amount),
    data=args.data,
    shardingflag=0,
    via=decode_hex(args.via[2:]),
    v=CHAIN_ID,
    r=0,
    s=0
)

encodedTx = encode(tx, Transaction)
# encodedTx = encode(tx)
#encoded = hex('f84309808504a817c80082520894f8558382014485843b9aca008382520880a0a0a0880de0b6b3a76400008080940000000000000000000000000000000000000000638080')
#encodeStr = 'f84309808504a817c80082520894f8558382014485843b9aca008382520880a0a0a0880de0b6b3a76400008080940000000000000000000000000000000000000000638080'
#encoded = bytearray(encodeStr)
#print("test encode",encoded)
print("encodedTx: ",binascii.hexlify(encodedTx))

donglePath = parse_bip32_path(args.path)
apdu = bytearray.fromhex("e0040000")
apdu.append(len(donglePath) + 1 + len(encodedTx))
apdu.append(len(donglePath) // 4)
apdu += donglePath + encodedTx

dongle = getDongle(True)
result = dongle.exchange(bytes(apdu))

# Needs to recover (main.c:1121)
if (CHAIN_ID*2 + 35) + 1 > 255:
	ecc_parity = result[0] - ((CHAIN_ID*2 + 35) % 256)
	v = (CHAIN_ID*2 + 35) + ecc_parity
else:
	v = result[0]

print('v: ',v)

r = int(binascii.hexlify(result[1:1 + 32]), 16)
s = int(binascii.hexlify(result[1 + 32: 1 + 32 + 32]), 16)

#systemflag=0
#shardingflag=0
#via="00000000000000000000000000000000000000000"

print('r: ',r)
print('s: ',s)

tx = Transaction(tx.nonce, tx.systemflag, tx.gasprice, tx.startgas,
                 tx.to, tx.value, tx.data, tx.shardingflag, tx.via, v, r, s)

#tx = Transaction(tx.nonce, tx.gasprice, tx.startgas,
#                 tx.to, tx.value, tx.data, v, r, s)

print("Signed transaction", encode_hex(encode(tx)))

