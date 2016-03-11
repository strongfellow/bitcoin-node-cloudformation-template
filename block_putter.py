
import boto3
import botocore
import binascii
import hashlib
import itertools
import sys
import logging

def read_exactly(input, n):
    result = input.read(n)
    if len(result) != n:
        raise EOFError
    return result

_hex = binascii.hexlify

def double_sha256(bs):
    hash = hashlib.sha256(hashlib.sha256(bs).digest()).digest()
    return _hex(hash[::-1])

def block_hash(bs):
    return double_sha256(bs[:80])

def tx_hash(bs):
    return double_sha256(bs)

def little_endian(input, n):
    bs = read_exactly(input, n)
    return sum(ord(b) << (i * 8) for i, b in enumerate(bs)) 

MAIN_NETWORK = 'f9beb4d9'

def main():
    logging.basicConfig(level=logging.INFO)
    s3 = boto3.client('s3')
    BUCKET = 'strongfellow.com'
    while True:
        network = _hex(read_exactly(sys.stdin, 4))
        length = little_endian(sys.stdin, 4)
        block = read_exactly(sys.stdin, length)
        h = block_hash(block)

        if network != MAIN_NETWORK:
            raise Exception('unexpected network: %s' % network)
        if not h.startswith('0000'):
            raise Exception('block hash %s doesnt have leading zeroes' % h)

        md5 = _hex(hashlib.md5(block).digest())
        print '%s\t%d\t%s\t%s' % (network, length, h, md5)
        key = 'blocks/%s' % h
        try:
            response = s3.head_object(Bucket=BUCKET, Key=key, IfMatch=md5)
            logging.info('cache hit for %s' % key)
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404 or error_code == 412:
                if error_code == 404:
                    logging.info('not found')
                if error_code == 412:
                    logging.info('found but md5 mismatch')
                logging.info('putting %s', key)
                s3.put_object(Bucket=BUCKET, Key=key, Body=block)
                logging.info('SUCCESS putting %s', key)
            else:
                logging.exception('unknown exception')
                raise

if __name__ == '__main__':
    main()
