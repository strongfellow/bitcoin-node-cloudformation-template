
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
            d = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
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
