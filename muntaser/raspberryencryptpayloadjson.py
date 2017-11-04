import time
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto import Random
import sys
import json



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







##START CODE



##recognize image and store result in json


#read results from json saved file
out_dict = {}
with open ('out.txt') as json_file:
	data = json.load(json_file)
	#print(data)
	for r in data['results']:
		print('platenumber: ' + r['plate'])
		out_dict['platenumber'] = r['plate']
		out_dict['spot'] = 1

payload1 = json.dumps(out_dict)

print(payload1)

print('\n')

##read the seed
with open ("seedfile") as seed_filein:
	seed = seed_filein.read()


##generate the key
hashk = SHA256.new()
hashk.update(seed)
hashkey = hashk.digest()
print('\n the key is : ' + hashkey + '\n')


payloadciphertext = AESCipher(hashkey).encrypt(payload1)
print('\npayloadciphertext: ' + payloadciphertext + '\n')

#hashp = SHA256.new()
#hashp.update(payloadciphertext + '||' + seed)
#hashpayload = hashp.digest()

hashpayload = md5(payloadciphertext + '||' + seed).hexdigest()
print('\n the hash of the payload + seed is : ' + hashpayload + '\n')
#hashpayloadencoded = hashpayload.encode('utf-8')
#print('\n the hash of the payload + seed encoded is : ' + hashpayloadencoded + '\n')

payload_out = {}
payload_out['ciphertext'] = payloadciphertext
payload_out['hashvalue'] = hashpayload
print(payload_out)
print('\n')


print(json.dumps(payload_out))

with open('jsonout.txt', 'w') as outfile:  
    json.dump(payload_out, outfile)

