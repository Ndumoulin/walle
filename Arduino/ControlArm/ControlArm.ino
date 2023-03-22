#include <Stepper.h>

String nom = "Arduino";
string msg;

const int stepsPerRevolution = 200;

Stepper myStepper = Stepper(stepsPerRevolution, 11, 10, 9, 8);

void setup() {
  // initialize the serial port:
  Serial.begin(9600);

  myStepper.setSpeed(60);
}

void loop() {
  readSerialPort();

  if(msg!= "") {
      // step one revolution  in one direction:
    Serial.println("clockwise");
    myStepper.step(stepsPerRevolution);
    delay(500);

    // step one revolution in the other direction:
    Serial.println("counterclockwise");
    myStepper.step(-stepsPerRevolution);
    delay(500);
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