#include <Servo.h>

String nom = "Arduino";
String msg;

Servo servo1;

void setup() {
  Serial.begin(9600);

  servo1.attach(6);
}

void loop() {
  readSerialPort();

  if(msg.toInt() >= 0 && msg.toInt() <= 1023) {
    servo1.write(msg.toInt());
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
