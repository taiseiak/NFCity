#include <Wire.h>

int led = 13;

void setup(){
  Wire.begin();
  Serial.begin(9600);
  pinMode(led, OUTPUT);
}

void loop(){
  Wire.requestFrom(4,6);
  
  while(Wire.available()){
    int i = Wire.read();
    
    //Serial.println(i);
    if(i==1){
      digitalWrite(led, HIGH);
      delay(1000);
      digitalWrite(led, LOW);
      Serial.println("Success!");
      //system("sendJson.sh");
    }
  }
  
  delay(500);
}
