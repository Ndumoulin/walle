#include <Servo.h>

String nom = "Arduino";
String msg = "";

int servoAngle = 90;

Servo servo1;

void setup() {
  Serial.begin(115200);

  servo1.attach(6);
  servo1.write(servoAngle);
}

void loop() {
  readSerialPort();

  if(msg != "") {

    if (msg == "R" || msg == "A"){
      servo1.writeMicroseconds(1600);
    }
    else if(msg == "L" || msg == "B")
    {
      servo1.writeMicroseconds(1400);
    }
    
  }
  delay(50);
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

  Serial.print(msg);
}
