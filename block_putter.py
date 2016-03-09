
import binascii
import hashlib
import itertools
import sys

def bytes_from_input(input, chunksize=8192):
    while True:
        chunk = input.read(chunksize)
        if chunk:
            for b in chunk:
                yield b
        else:
            break

def hex(bs):
    return binascii.hexlify(bs)

def double_sha256(bs):
    hash = hashlib.sha256(hashlib.sha256(bs).digest()).digest()
    return hex(hash[::-1])

def block_hash(bs):
    return double_sha256(bs[:80])

def tx_hash(bs):
    return double_sha256(bs)

def little_endian(bytes):
    i = 0
    n = 0
    for b in (ord(x) for x in bytes):
        n = n + (b << (i * 8))
        i += 1
    return n

bs = bytes_from_input(sys.stdin)
while True:
    network = hex(bytearray([bs.next(), bs.next(), bs.next(), bs.next()]))
    length = little_endian(itertools.islice(bs, 4))
    block = bytearray(itertools.islice(bs, length))
    h = block_hash(block)
    print '%s\t%d\t%s' % (network, length, h)
