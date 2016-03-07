
import binascii
from datetime import datetime
import hashlib
import zmq

import twitter
import ConfigParser, os.path
import boto3
import logging

def hex(bs):
    return binascii.hexlify(bs)

def double_sha256(bs):
    hash = hashlib.sha256(hashlib.sha256(bs).digest()).digest()
    return hex(hash[::-1])

def block_hash(bs):
    return double_sha256(bs[:80])

def tx_hash(bs):
    return double_sha256(bs)

def tweet(t, message):
    logging.info('posting %s', message)
    status = t.PostUpdate(message)
    logging.info(status)

def put(s3, bucket, key, bs):
    logging.info('putting object at s3://%s/%s', bucket, key)
    s3.Object('strongfellow.com', key).put(Body=bs)
    logging.info('sucess putting object at s3://%s/%s', bucket, key)

def copy(s3, source_bucket, source_key, dest_bucket, dest_key):
    logging.info('copying object from s3://%s/%s to s3://%s/%s',
                 source_bucket,
                 source_key,
                 dest_bucket,
                 dest_key)
    s3.copy_object(
        Bucket=dest_bucket,
        Key=dest_key,
        CopySource={'Bucket': source_bucket, 'Key': source_key},
    )
    logging.info('sucess copying object from s3://%s/%s to s3://%s/%s',
                 source_bucket,
                 source_key,
                 dest_bucket,
                 dest_key)


def main():
    logging.basicConfig(level=logging.INFO)

    config = ConfigParser.ConfigParser()
    config.read(os.path.expanduser('~/.twitrc'))
    print config.sections()

    t = twitter.Api(consumer_key=config.get('twitter', 'consumer_key'),
                    consumer_secret=config.get('twitter', 'consumer_secret'),
                    access_token_key=config.get('twitter', 'access_token_key'),
                    access_token_secret=config.get('twitter', 'access_token_secret'))
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')

    print(t.VerifyCredentials())

    port = 28332

    zmqContext = zmq.Context()
    zmqSubSocket = zmqContext.socket(zmq.SUB)
    zmqSubSocket.setsockopt(zmq.SUBSCRIBE, "hashblock")
    zmqSubSocket.setsockopt(zmq.SUBSCRIBE, "hashtx")
    zmqSubSocket.setsockopt(zmq.SUBSCRIBE, "rawblock")
    zmqSubSocket.setsockopt(zmq.SUBSCRIBE, "rawtx")
    zmqSubSocket.connect("tcp://127.0.0.1:%i" % port)

    bucket = 'strongfellow.com'
    template = 'Bitcoin Block Mined, %s: http://strongfellow.com/blocks/%s #btc #bitcoin'

    try:
        while True:
            msg = zmqSubSocket.recv_multipart()
            now = datetime.utcnow()
            d = now.strftime('%Y-%m-%dT%H:%M:%S')
            topic = str(msg[0])
            body = msg[1]
            logging.info('processing topic %s at %s', topic, d) 
            if topic == "hashblock":
                pass
            elif topic == "hashtx":
                pass
            elif topic == "rawblock":
                h = block_hash(body)
                key = 'blocks/%s' % h
                put(s3, bucket, key, body)
                message = template % (d, h)
                tweet(t, message)
                copy(s3_client, bucket, key,
                     'blocks.strongfellow.com',
                     'daily/%d-%02d-%02d/%s' % (now.year, now.month, now.day, h))
            elif topic == "rawtx":
                pass
#                h = tx_hash(body)
#                key = 'transactions/%s' % h
#                put(s3, bucket, key, body)
#                message = 'tx %s' % h
#                tweet(t, message)
    except:
        logging.exception('destroying zmq')
        zmqContext.destroy()

if __name__ == '__main__':
    main()
