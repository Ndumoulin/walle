#include <Stepper.h>

String nom = "Arduino";
string msg;

const int stepsPerRevolution = 2038;

Stepper myStepper = Stepper(stepsPerRevolution, 11, 9, 10, 8);

void setup() {
  Serial.begin(9600);

  // set the speed at 60 rpm:
  myStepper.setSpeed(60);
  // initialize the serial port:
  Serial.begin(9600);
}

void loop() {
  readSerialPort();

  if(msg!= "") {
    myStepper.step(stepsPerRevolution);
    delay(500);
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