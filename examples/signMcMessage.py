#!/usr/bin/env python3
from __future__ import print_function

from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException
from decimal import Decimal
from mcBase import sha3
from eth_keys import KeyAPI
import argparse
import struct
import binascii

# Define here Chain_ID
CHAIN_ID = 99

# Magic define
SIGN_MAGIC = b'\x19Moac Signed Message:\n'

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
parser.add_argument('--path', help="BIP 32 path to sign with")
parser.add_argument('--message', help="Message to sign", required=True)
args = parser.parse_args()

args.message = args.message.encode()

if args.path == None:
    args.path = "44'/0'"

encodedTx = struct.pack(">I", len(args.message))
encodedTx += args.message

donglePath = parse_bip32_path(args.path)
apdu = bytearray.fromhex("e0080000")
apdu.append(len(donglePath) + 1 + len(encodedTx))
apdu.append(len(donglePath) // 4)
apdu += donglePath + encodedTx

dongle = getDongle(True)
result = dongle.exchange(bytes(apdu))

v = int(result[0])

# Compute parity
if (CHAIN_ID*2 + 35) + 1 > 255:
	ecc_parity = v - ((CHAIN_ID*2 + 35) % 256)
else:
	ecc_parity = (v + 1) % 2

v = "%02X" % ecc_parity
r = binascii.hexlify(result[1:1 + 32]).decode()
s = binascii.hexlify(result[1 + 32: 1 + 32 + 32]).decode()
msg_to_sign = SIGN_MAGIC + str(len(args.message)).encode() + args.message
hash = sha3(msg_to_sign.decode())

signature = KeyAPI.Signature(vrs=(int(v, 16), int(r, 16), int(s, 16)))
pubkey = KeyAPI.PublicKey.recover_from_msg_hash(hash, signature)

print("[INFO] Hash is: 0x", binascii.hexlify(hash).decode(), sep='');
print('{')
print('  "address": "', pubkey.to_address(), '",', sep='')
print('  "msg": "', args.message.decode(),'",', sep='')
print('  "sig": "', signature, '",', sep = '')
print('  "version": "3"')
print('  "signed": "ledger"')
print('}')
