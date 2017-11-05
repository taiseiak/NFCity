import RPi.GPIO as GPIO
import time
import os
import requests
import json
import sys
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto import Random




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
	##self.key = md5(key).hexdigest()
	##hacky solution
	self.key = "hackathongsu2017"


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









GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24

count = 0

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)

flag = 0

while count <3 :
  print "Distance Measurement In Progress"

  print "Waiting For Sensor To Settle"
  time.sleep(2)

  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)

  while GPIO.input(ECHO)==0:
    pulse_start = time.time()

  while GPIO.input(ECHO)==1:
    pulse_end = time.time()

  pulse_duration = pulse_end - pulse_start

  distance = pulse_duration * 17150

  distance = round(distance, 2)

  print "Distance:",distance,"cm"

  #GPIO.cleanup()

  time.sleep(10)
  
  ##do stuff here if car found

  if distance<100 :
    if flag == 1:
      continue
    flag = 1
    print ('\n parked car detected!!\n')
    print ('\n taking photo of car \n')
    
    os.system("raspistill -o parked.jpg")

    time.sleep(6)
    print ('\n photo captured, now calling server for recognition \n')


## local image recognition
    recogjson = os.system("alpr -n 1 -j lp.jpg >> rout.txt")
    out_dict = {}
    time.sleep(6)

    with open ('out.txt') as json_file:
      data = json.load(json_file)
      #print(data)
      for r in data['results']:
        print('platenumber: ' + r['plate'])
        out_dict['platenumber'] = r['plate']
        out_dict['spot'] = 1

    payload1 = json.dumps(out_dict)
    
##
##    with open('payloadout.txt', 'w') as payloadoutfile:  
##      json.dump(payload1, payloadoutfile)

    print(payload1)

    print('\n')

    ## now call the server

    ##first encrypt
    payloadciphertext = AESCipher('hackathongsu2017').encrypt(payload1)
    print('\npayloadciphertext: ' + payloadciphertext + '\n')


    ##hacky
    hashpayload = 'somehashvalue'
    
    payload_out = {}
    payload_out['ciphertext'] = payloadciphertext
    payload_out['hashvalue'] = hashpayload
    print(payload_out)
    print('\n')

    jsonsend = json.dumps(payload_out)

    jstring = str(jsonsend)
    print(jsonsend)

  

    #r = requests.post('http://NFCityServer.us-west-2.elasticbeanstalk.com/send_license', data=jstring)
    r = requests.post('http://NFCityServer.us-west-2.elasticbeanstalk.com/send_license', data={"ciphertext": payloadciphertext, "hashvalue": "somehashvalue"})


   
    
    print('\n the server says : ' +r.text)

##    url = 'http://18.216.77.110:8080/upload'
##    files = {'upload_image': open('parked.jpg','rb')}
##    r = requests.post(url, files=files)
##
##    print ('\n the server replied: ')
##    print(r.text)


    #now confirm with GE servers to ensure a car has entered the lot
    print ('\n  now calling GE api to confirm car entry into lot\n')

    url = "https://ic-event-service.run.aws-usw02-pr.ice.predix.io/v2/locations/LOC-ATL-0009-3/events"
    querystring = {"eventType":"PKIN","startTime":"1509875600000","endTime":"1509875728000"}
    headers = {
        'authorization': "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiI5NjliYmRiZDI2ZmM0NWQxYmFhNTBhMjdmNDg3MGM4ZCIsInN1YiI6ImhhY2thdGhvbiIsInNjb3BlIjpbInVhYS5yZXNvdXJjZSIsImllLWN1cnJlbnQuU0RTSU0tSUUtUFVCTElDLVNBRkVUWS5JRS1QVUJMSUMtU0FGRVRZLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtRU5WSVJPTk1FTlRBTC5JRS1FTlZJUk9OTUVOVEFMLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtVFJBRkZJQy5JRS1UUkFGRklDLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtUEFSS0lORy5JRS1QQVJLSU5HLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtUEVERVNUUklBTi5JRS1QRURFU1RSSUFOLkxJTUlURUQuREVWRUxPUCJdLCJjbGllbnRfaWQiOiJoYWNrYXRob24iLCJjaWQiOiJoYWNrYXRob24iLCJhenAiOiJoYWNrYXRob24iLCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwicmV2X3NpZyI6IjlmMWYyYzRkIiwiaWF0IjoxNTA5ODczMDI5LCJleHAiOjE1MTA0Nzc4MjksImlzcyI6Imh0dHBzOi8vODkwNDA3ZDctZTYxNy00ZDcwLTk4NWYtMDE3OTJkNjkzMzg3LnByZWRpeC11YWEucnVuLmF3cy11c3cwMi1wci5pY2UucHJlZGl4LmlvL29hdXRoL3Rva2VuIiwiemlkIjoiODkwNDA3ZDctZTYxNy00ZDcwLTk4NWYtMDE3OTJkNjkzMzg3IiwiYXVkIjpbImllLWN1cnJlbnQuU0RTSU0tSUUtVFJBRkZJQy5JRS1UUkFGRklDLkxJTUlURUQiLCJpZS1jdXJyZW50LlNEU0lNLUlFLVBBUktJTkcuSUUtUEFSS0lORy5MSU1JVEVEIiwiaWUtY3VycmVudC5TRFNJTS1JRS1QVUJMSUMtU0FGRVRZLklFLVBVQkxJQy1TQUZFVFkuTElNSVRFRCIsInVhYSIsImhhY2thdGhvbiIsImllLWN1cnJlbnQuU0RTSU0tSUUtRU5WSVJPTk1FTlRBTC5JRS1FTlZJUk9OTUVOVEFMLkxJTUlURUQiLCJpZS1jdXJyZW50LlNEU0lNLUlFLVBFREVTVFJJQU4uSUUtUEVERVNUUklBTi5MSU1JVEVEIl19.DQihU7hsYoBJyuGLnzdsrUgUhTJmNtGP4yr_MtOUrjOZ6uu2bFVysrKfTVrMIWR3d7cI0jPM4JR1rJcIAsjo2fN3TV0xliSwPGkWL4AzCIX-ZNbbolNZrpOtlVKzhQq80Xbkq2eH1pMC6UN2MNb8zZRtle3B-4M8lhEJ_dg9CG2d15JKp3rBnEB3O-3a1yFmqXeH9mmz1dxl6Or8hHltsvBU6u35yqxNeh3cuIkIGkRfQuJaMinVDrT41AVFKBsyBn83jZ_fjG0JTR87Oo4i2gZAxC4IGgsqTEK8roD0MSh7Dz9m2mJy85Aws_oNgAnAF6i98Vwrli25Yuj-WV515A",
        'predix-zone-id': "SDSIM-IE-PARKING",
        'cache-control': "no-cache",
        'postman-token': "ce79278e-404f-41af-abf2-60082503ae15"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print('\n the server says : ' +response.text)

    #print(response.text)
    jsonPKIN = json.loads(response.text)

    numin = jsonPKIN["metaData"]["totalRecords"]

    print('\n')
    print('number of cars that entered in this time period are ' + str(numin) +'\n')
    if numin==1 :
      print('numbers match\n')
    else :
      print('warning!! numbers dont match, sensors may need maintenance!!\n')


  else :
    if flag == 1:
      ## car has left the spot, so check GE servers to see if a car has left the lot as well

      ##end transaction
      
      r = requests.post('http://NFCityServer.us-west-2.elasticbeanstalk.com/end_transaction', data={"ciphertext": payloadciphertext, "hashvalue": "somehashvalue"})

      print ('\n  now calling GE api to confirm car exit from lot\n')

      url = "https://ic-event-service.run.aws-usw02-pr.ice.predix.io/v2/locations/LOC-ATL-0009-3/events"

      querystring = {"eventType":"PKOUT","startTime":"1509875600000","endTime":"1509875728000"}

      headers = {
          'authorization': "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiI5NjliYmRiZDI2ZmM0NWQxYmFhNTBhMjdmNDg3MGM4ZCIsInN1YiI6ImhhY2thdGhvbiIsInNjb3BlIjpbInVhYS5yZXNvdXJjZSIsImllLWN1cnJlbnQuU0RTSU0tSUUtUFVCTElDLVNBRkVUWS5JRS1QVUJMSUMtU0FGRVRZLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtRU5WSVJPTk1FTlRBTC5JRS1FTlZJUk9OTUVOVEFMLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtVFJBRkZJQy5JRS1UUkFGRklDLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtUEFSS0lORy5JRS1QQVJLSU5HLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtUEVERVNUUklBTi5JRS1QRURFU1RSSUFOLkxJTUlURUQuREVWRUxPUCJdLCJjbGllbnRfaWQiOiJoYWNrYXRob24iLCJjaWQiOiJoYWNrYXRob24iLCJhenAiOiJoYWNrYXRob24iLCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwicmV2X3NpZyI6IjlmMWYyYzRkIiwiaWF0IjoxNTA5ODczMDI5LCJleHAiOjE1MTA0Nzc4MjksImlzcyI6Imh0dHBzOi8vODkwNDA3ZDctZTYxNy00ZDcwLTk4NWYtMDE3OTJkNjkzMzg3LnByZWRpeC11YWEucnVuLmF3cy11c3cwMi1wci5pY2UucHJlZGl4LmlvL29hdXRoL3Rva2VuIiwiemlkIjoiODkwNDA3ZDctZTYxNy00ZDcwLTk4NWYtMDE3OTJkNjkzMzg3IiwiYXVkIjpbImllLWN1cnJlbnQuU0RTSU0tSUUtVFJBRkZJQy5JRS1UUkFGRklDLkxJTUlURUQiLCJpZS1jdXJyZW50LlNEU0lNLUlFLVBBUktJTkcuSUUtUEFSS0lORy5MSU1JVEVEIiwiaWUtY3VycmVudC5TRFNJTS1JRS1QVUJMSUMtU0FGRVRZLklFLVBVQkxJQy1TQUZFVFkuTElNSVRFRCIsInVhYSIsImhhY2thdGhvbiIsImllLWN1cnJlbnQuU0RTSU0tSUUtRU5WSVJPTk1FTlRBTC5JRS1FTlZJUk9OTUVOVEFMLkxJTUlURUQiLCJpZS1jdXJyZW50LlNEU0lNLUlFLVBFREVTVFJJQU4uSUUtUEVERVNUUklBTi5MSU1JVEVEIl19.DQihU7hsYoBJyuGLnzdsrUgUhTJmNtGP4yr_MtOUrjOZ6uu2bFVysrKfTVrMIWR3d7cI0jPM4JR1rJcIAsjo2fN3TV0xliSwPGkWL4AzCIX-ZNbbolNZrpOtlVKzhQq80Xbkq2eH1pMC6UN2MNb8zZRtle3B-4M8lhEJ_dg9CG2d15JKp3rBnEB3O-3a1yFmqXeH9mmz1dxl6Or8hHltsvBU6u35yqxNeh3cuIkIGkRfQuJaMinVDrT41AVFKBsyBn83jZ_fjG0JTR87Oo4i2gZAxC4IGgsqTEK8roD0MSh7Dz9m2mJy85Aws_oNgAnAF6i98Vwrli25Yuj-WV515A",
          'predix-zone-id': "SDSIM-IE-PARKING",
          'cache-control': "no-cache",
          'postman-token': "ce79278e-404f-41af-abf2-60082503ae15"
          }

      response = requests.request("GET", url, headers=headers, params=querystring)

      #print(response.text)

      jsonPKOUT = json.loads(response.text)

      numout = jsonPKOUT["metaData"]["totalRecords"]

      print('\n')
      print('number of cars that exited in this time period are ' + str(numout) +'\n')

      if numout==1 :
        print('numbers match\n')
      else :
        print('warning!! numbers dont match, sensors may need maintenance!!\n')
    
    flag = 0
  
  count +=1

GPIO.cleanup()
print ('\n end of program reached!!\n')
