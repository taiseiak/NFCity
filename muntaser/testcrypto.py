import time
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto import Random
import sys



# Padding for the input string --not
# related to encryption itself.
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        #self.key = md5(key.encode('utf8')).hexdigest()
	self.key = md5(key).hexdigest()

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode('utf8')












hash = SHA256.new()
hash.update('this is a test message')
hashvalue = hash.digest()
print(hashvalue)
print('\nnow saving\n')

with open('hashout.txt', 'w') as outfile: 
	outfile.write(hashvalue)

time.sleep(2)

with open('hashout.txt') as infile: 
	hashvalue2 = infile.read()

print(hashvalue2)

if(hashvalue==hashvalue2):
	print('\nhashes matched\n')
else:
	print('\nhashes didnt match!!\n')

print('\nnow encryption\n')

##this message contains the transaction/action tuple
message = 'my secret message'



##
# MAIN
# Just a test.
#msg = raw_input('Message...: ')
#msg = unicode(msg, errors='replace')
#pwd = raw_input('Password..: ')
#pwd = unicode(pwd, errors='replace')

#print('\nplain test: ' + msg)
#print('\nCiphertext test: ' + AESCipher(pwd).encrypt(msg))

ciphertext = AESCipher(hashvalue).encrypt(message)
print('Ciphertext real: ' + ciphertext)


print('\nnow decryption\n')
plaintext = AESCipher(hashvalue2).decrypt(ciphertext)
print('Decrypted Ciphertext real: ' + plaintext)

