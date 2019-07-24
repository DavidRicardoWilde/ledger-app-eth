#!/usr/bin/env python
from rlp.sedes import big_endian_int, binary, Binary
from rlp import Serializable

try:
    from Crypto.Hash import keccak
    def sha3_256(x): return keccak.new(digest_bits=256, data=x.encode()).digest()
except:
    import sha3 as _sha3
    def sha3_256(x): return _sha3.sha3_256(x).digest()

address = Binary.fixed_length(20, allow_empty=True)

def sha3(seed):
    return sha3_256(str(seed))


class Transaction(Serializable):
    fields = [
        ('nonce', big_endian_int),
        ('systemflag',big_endian_int),
        ('gasprice', big_endian_int),
        ('startgas', big_endian_int),
        ('to', address),
        ('value', big_endian_int),
        ('data', binary),
	    ('shardingflag',big_endian_int),
	    ('via', address),
        ('v', big_endian_int),
        ('r', big_endian_int),
        ('s', big_endian_int),
    ]
def __init__(self, nonce, systemflag, gasprice, startgas, to, value, data, shardingflag=0, via='000000000000000000000000000000', v=0, r=0, s=0):super(Transaction, self).__init__(
            nonce, systemflag, gasprice, startgas, to, value, data, shardingflag, via, v, r, s)

#        def __init__(self, nonce, gasprice, startgas, to, value, data, v=0, r=0, s=0, systemflag=0, shardingflag=0):
 #       super(Transaction, self).__init_(
  #          nonce, gasprice, startgas, to, value, data, v, r, s, systemflag, shardingflag)

    #         class Transaction(Serializable):
    # fields = [
    #     ('nonce', big_endian_int),
    #     ('gasprice', big_endian_int),
    #     ('startgas', big_endian_int),
    #     ('to', address),
    #     ('value', big_endian_int),
    #     ('data', binary),
    #     ('v', big_endian_int),
    #     ('r', big_endian_int),
    #     ('s', big_endian_int),
    # ]

    # def __init__(self, nonce, gasprice, startgas, to, value, data, v=0, r=0, s=0):
    #     super(Transaction, self).__init__(
    #         nonce, gasprice, startgas, to, value, data, v, r, s)

class UnsignedTransaction(Serializable):
    fields = [
        ('nonce', big_endian_int),
        ('gasprice', big_endian_int),
        ('startgas', big_endian_int),
        ('to', address),
        ('value', big_endian_int),
        ('data', binary),
    ]

def unsigned_tx_from_tx(tx):
    return UnsignedTransaction(
        nonce=tx.nonce,
        gasprice=tx.gasprice,
        startgas=tx.startgas,
        to=tx.to,
        value=tx.value,
        data=tx.data,
    )

