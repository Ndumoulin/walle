#include <Servo.h>

String nom = "Arduino";
String msg = "";

int servoAngle = 90;
int commands[6];

Servo servo1;

void setup() {
  Serial.begin(115200);

  servo1.attach(6);
  servo1.write(servoAngle);
}

void loop() {
  readSerialPort();

  if(msg != "") {
    sendData();
    splitCommands(msg);
    if(commands[3] == 1) {
      servo1.write(180);
    }
    else if(commands[3] == 0) {
      servo1.write(90);
    }
    else if(commands[3] == -1) {
      servo1.write(0);
    }
  }
  delay(50);
}

void splitCommands(String line) {
  char *token;
  char buffer[50];
  int index = 0;
  
  line.toCharArray(buffer, sizeof(buffer));

  token = strtok(buffer, ";");

  while (token != NULL && index < 5) {
    int value = atoi(token);
    commands[index] = value;
    index++;
    token = strtok(NULL, ";");
  }
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
