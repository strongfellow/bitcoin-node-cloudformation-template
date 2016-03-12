
import hashlib
import binascii

_hex = binascii.hexlify

def double_sha256(bs):
    hash = hashlib.sha256(hashlib.sha256(bs).digest()).digest()
    return _hex(hash[::-1])

