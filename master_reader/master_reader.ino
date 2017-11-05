#include <rgb_lcd.h>
#include <Wire.h>

rgb_lcd lcd;

void setup(){
  Wire.begin();
  lcd.begin(16, 2);
  Serial.begin(9600);
  lcd.print("Hello");
}

void loop(){
  Wire.requestFrom(4,6);
  lcd.setCursor(0,1);
  
  while(Wire.available()){
    int i = Wire.read();
    
    //Serial.println(i);
    if(i==1){
      lcd.print("Success");
      Serial.println("Success!");
      //system("sendJson.sh");
    }
  }
  
  delay(500);
  lcd.clear();
}
