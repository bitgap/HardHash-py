import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/lib')
import time
from enum import Enum
import unicodedata
import binascii
import argparse
import hashlib
from HardHash import HardHash 
import bip39


class Encoding(Enum):
        text = 'text'
        hex = 'hex'

def normalize(str, encoding):
        if encoding == Encoding.text:
                return unicodedata.normalize("NFKC", str).encode('UTF-8')
        elif encoding == Encoding.hex:
                return bytearray.fromhex(str)
        else:
                raise Exception("invalid type")

parser = argparse.ArgumentParser()

parser.add_argument('--passphrase', dest='passphrase', default="")

parser.add_argument('--salt', dest='salt', default="")

parser.add_argument('--passphraseEncoding', dest='passphraseEncoding', type=Encoding, default=Encoding.text)

parser.add_argument('--saltEncoding', dest='saltEncoding', type=Encoding, default=Encoding.text)

parser.add_argument('-n', dest='n', type=int, required=True)

parser.add_argument('-r', dest='r', type=int, required=True)

parser.add_argument('-p', dest='p', type=int, required=True)

args = parser.parse_args()

passphrase =  normalize(args.passphrase, args.passphraseEncoding)

salt =  normalize(args.salt, args.saltEncoding)

start = time.time()

hash = HardHash(passphrase, salt, args.n, args.r, args.p)

duration = time.time() - start

print(
"""
Passphrase
            Hex
                    {}
            BIP39*
                    {}

Salt
            Hex
                    {}
            BIP39*
                    {}

Hash
            Hex
                    {}
            BIP39
                    {}

{}s
"""
     .format(
             binascii.hexlify(passphrase).decode('ascii'), bip39.get_mnemonic(hashlib.sha256(passphrase).digest()), 
             binascii.hexlify(salt).decode('ascii'), bip39.get_mnemonic(hashlib.sha256(salt).digest()),
             binascii.hexlify(hash).decode('ascii'), bip39.get_mnemonic(hash),
             round(duration, 2)
           ))