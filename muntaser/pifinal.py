import RPi.GPIO as GPIO
import time
import os
import requests

GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24

count = 0

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)


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
    print ('\n parked car detected!!\n')
    print ('\n taking photo of car \n')
    
    os.system("raspistill -o parked.jpg")

    time.sleep(6)
    print ('\n photo captured, now calling server for recognition \n')

    ## now call the server
##    url = 'http://18.216.77.110:8080/upload'
##    files = {'upload_image': open('parked.jpg','rb')}
##    r = requests.post(url, files=files)
##
##    print ('\n the server replied: ')
##    print(r.text)
    
  
  count +=1

GPIO.cleanup()
print ('\n end of program reached!!\n')
