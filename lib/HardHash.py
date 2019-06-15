import hashlib
import sys

def HardHash(passphrase, salt, n, r, p):
   return hashlib.sha256(passphrase + salt + hashlib.scrypt(password = passphrase, salt = salt, n = pow(2, n), r = r, p = p, dklen = 32, maxmem = 2147483647)).digest()