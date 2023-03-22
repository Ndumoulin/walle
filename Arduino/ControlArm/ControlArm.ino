#include <Stepper.h>

String nom = "Arduino";
string msg;

const int stepsPerRevolution = 2038;

Stepper myStepper = Stepper(stepsPerRevolution, 11, 9, 10, 8);

void setup() {
  // initialize the serial port:
  Serial.begin(9600);
}

void loop() {
  readSerialPort();

  if(msg!= "") {
    myStepper.setSpeed(5);
	  myStepper.step(stepsPerRevolution);
	  delay(1000);
	
    // Rotate CCW quickly at 10 RPM
    myStepper.setSpeed(10);
    myStepper.step(-stepsPerRevolution);
    delay(1000);
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