#!/usr/bin/env python2
import sys
import binascii
import base64
from Crypto.Cipher import AES

KEY = '7815696ecbf1c96e6894b779456d330e'
IV = '\x36\x8a\xea\x76\x12\xc9\xab\x91\x63\xda\xea\x76\x12\xc9\xac\x93'


class MaxCubeCrypto:
    MODE = AES.MODE_CBC
    BLOCK_SIZE = 16

    def encrypt(self, ptext):
        aes = AES.new(binascii.unhexlify(KEY), self.MODE, IV=IV)
        return aes.encrypt(self.pad(ptext))


    def decrypt(self, ctext):
        aes = AES.new(binascii.unhexlify(KEY), self.MODE, IV=IV)
        return self.unpad(aes.decrypt(ctext))


    def pad(self,s)
        return s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)


    def unpad(self,s):
        return s[0:-ord(s[-1])]


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('{} [enc|dec] input'.format(sys.argv[0]))
        sys.exit(1)

    maxcube = MaxCubeCrypto()

    if sys.argv[1] == 'enc':
        ret = maxcube.encrypt(sys.argv[2])
        sys.stdout.write(base64.b64encode(ret))
            
    elif sys.argv[1] == 'dec':
        data = base64.b64decode(sys.argv[2])
        ret = maxcube.decrypt(data)
        sys.stdout.write(ret)
            
    else:
        print('Invalid command: {}'.format(sys.argv[1]))
