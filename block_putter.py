
import boto3
import botocore
import binascii
import hashlib
import itertools
import sys
import logging

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

def main():
    logging.basicConfig(level=logging.INFO)
    bs = bytes_from_input(sys.stdin)
    s3 = boto3.client('s3')
    BUCKET = 'strongfellow.com'
    while True:
        network = hex(bytearray([bs.next(), bs.next(), bs.next(), bs.next()]))
        length = little_endian(itertools.islice(bs, 4))
        block = bytearray(itertools.islice(bs, length))
        h = block_hash(block)

        md5 = hex(hashlib.md5(block).digest())
        print '%s\t%d\t%s\t%s' % (network, length, h, md5)
        key = 'blocks/%s' % h
        try:
            response = s3.head_object(
                Bucket=BUCKET,
                Key=key,
                IfMatch=md5)
            logging.info('cache hit for %s' % key)

        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = int(e.response['Error']['Code'])
            if error_code == 404 or error_code == 412:
                logging.info('expected exception, object not found or md5 didn\'t match')
                logging.info('putting %s', key)
                s3.put_object(
                    Bucket=BUCKET,
                    Key=key,
                    Body=bytes(block))
            else:
                logging.exception('unknown exception')

if __name__ == '__main__':
    main()

