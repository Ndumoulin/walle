#include <Servo.h>

void setup() {
  Serial.begin(9600); // Make sure the baud rate matches the Raspberry Pi side

  servo1.attach(6);
  servo1.write(servoAngle);
}

void loop() {
  if (Serial.available() > 0) {
    servo1.writeMicroseconds(1600);
    int incomingByte = Serial.read();
    Serial.print("Received: ");
    Serial.println(incomingByte, DEC);
  }
}
