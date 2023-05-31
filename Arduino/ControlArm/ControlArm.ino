#include <Servo.h>

// Définition de tous les PIN nécessaire pour les moteurs DC
#define enA 5
#define enB 3
#define in1 4
#define in2 7
#define in3 2
#define in4 8

String msg = "";

bool drivingMode = true;

int waistAngle = 90;
int shoulderAngle = 90;
int elbowAngle = 90;

int motorSpeedL= 0;
int motorSpeedR = 0;

int commands[7];

int Solenoid = 9;

Servo waistServo;
Servo shoulderServo;
Servo elbowServo;

void setup() {
  Serial.begin(115200);

  pinMode(Solenoid, OUTPUT);

  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  
  waistServo.attach(11);
  shoulderServo.attach(10);
  elbowServo.attach(6);
}

void loop() {
  readSerialPort();

  if(msg != "") {
    splitCommands(msg);

    // Contrôle du moteur DC gauche
    
    if(commands[0] > 0) {
      motorSpeedL = commands[0];
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      analogWrite(enA, motorSpeedL);
    }
    else if (commands[0] < 0) {
       motorSpeedL = commands[0] * -1;
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      analogWrite(enA, motorSpeedL);
    }
    else if (commands[0] == 0) {
      analogWrite(enA, 0);
    }

    // Contrôle du moteur DC droit
    
    if(commands[1] > 0) {
      motorSpeedR = commands[1];
      digitalWrite(in3, LOW);
      digitalWrite(in4, HIGH);
      analogWrite(enB, motorSpeedR);
    }
    else if (commands[1] < 0) {
       motorSpeedL = commands[1] * -1;
      digitalWrite(in3, HIGH);
      digitalWrite(in4, LOW);
      analogWrite(enB, motorSpeedR);
    }
    else if (commands[1] == 0) {
      analogWrite(enB, 0);
    }
  }
  
  // Waist servo control
  
  if(commands[2] == 1 && waistAngle < 180) {
    waistAngle = waistAngle + 1;
    waistServo.write(waistAngle);
  }
  else if(commands[2] && waistAngle > 0) {
    waistAngle = waistAngle - 1;
    waistServo.write(waistAngle);
  }

  // Shoulder servo control

  if(commands[3] == 1 && shoulderAngle < 180) {
    shoulderAngle = shoulderAngle + 1;
    shoulderServo.write(shoulderAngle);
  }
  else if(commands[3] == -1 && shoulderAngle > 0) {
    shoulderAngle = shoulderAngle - 1;
    shoulderServo.write(shoulderAngle);
  }
  
  // Elbow servo control

  if(commands[4] == 1 && elbowAngle < 180) {
    elbowAngle = elbowAngle + 1;
    elbowServo.write(elbowAngle);
  }
  else if(commands[4] == -1 && elbowAngle > 0) {
    elbowAngle = elbowAngle - 1;
    elbowServo.write(elbowAngle);
  }

  // Contrôle de l'électro-aimant
  if (commands[5] == 1) {
    digitalWrite(Solenoid, HIGH);
  } 
  else if(commands[5] == 0) {
    digitalWrite(Solenoid, LOW);
  }

  delay(20);
}

// Fonction permettant de séparer la string que l'on recoit et de reformer le tableau
void splitCommands(String line) {
  char *token;
  char buffer[50];
  int index = 0;
  
  line.toCharArray(buffer, sizeof(buffer));

  token = strtok(buffer, ";");

  while (token != NULL && index < 6) {
    int value = atoi(token);
    commands[index] = value;
    index++;
    token = strtok(NULL, ";");
  }
}

// Lecture sur le port série
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
