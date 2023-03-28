#include <Servo.h>

byte msg;

int servoAngle = 90;

Servo servo1;

void setup() {
  Serial.begin(9600);

  servo1.attach(6);
  servo1.write(servoAngle);
}

void loop() {
  readSerialPort();

  if(msg != null) {

    if (msg == "A,1" || msg == "RB"){
      servo1.writeMicroseconds(1600);
    }
    else if(msg == "A,-1" || msg == "LB")
    {
      servo1.writeMicroseconds(1400);
    }
    sendData();
    
  }
  delay(500);
}

void readSerialPort() {
  msg = "";

  if(Serial.available()) {
    delay(10);
    while (Serial.available() > 0) {
      msg += (char)Serial.read();
    }
    Serial.flush();
  }
}

void sendData() {
  // write data

  Serial.print(nom);
  Serial.print("received : ");
  Serial.print(msg);
}
