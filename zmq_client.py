#!/usr/bin/env python2

import array
import binascii
import hashlib
import zmq

port = 28332

zmqContext = zmq.Context()
zmqSubSocket = zmqContext.socket(zmq.SUB)
zmqSubSocket.setsockopt(zmq.SUBSCRIBE, "hashblock")
zmqSubSocket.setsockopt(zmq.SUBSCRIBE, "hashtx")
zmqSubSocket.setsockopt(zmq.SUBSCRIBE, "rawblock")
zmqSubSocket.setsockopt(zmq.SUBSCRIBE, "rawtx")
zmqSubSocket.connect("tcp://127.0.0.1:%i" % port)

def hex(bs):
    return binascii.hexlify(bs)

def double_sha256(bs):
    hash = hashlib.sha256(hashlib.sha256(bs).digest()).digest()
    return hex(hash[::-1])

def block_hash(bs):
    return double_sha256(bs[:80])

def tx_hash(bs):
    return double_sha256(bs)

try:
    while True:
        msg = zmqSubSocket.recv_multipart()
        topic = str(msg[0])
        body = msg[1]

        if topic == "hashblock":
            print "HASH BLOCK: %s" % hex(body)
        elif topic == "hashtx":
            print "HASH TX:    %s" % hex(body)
#            print hex(body)
        elif topic == "rawblock":
            print "RAW BLOCK HEADER: %s" % hex(body[:80])
            print "Computed Block Hash: %s" % block_hash(body)
        elif topic == "rawtx":
            print 'RAW TX; hash is %s' % tx_hash(body)
#            print hex(body)

except KeyboardInterrupt:
    zmqContext.destroy()
except:
    zmqContext.destroy()
