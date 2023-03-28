String nom = "Arduino";

void setup() {
  Serial.begin(9600); // Make sure the baud rate matches the Raspberry Pi side
}

void loop() {
  if (Serial.available()) {
    byte byte_received = Serial.read();
    sendData(byte_received);
    // Do something with the received byte here
  }
}

void sendData(byte msg) {
  // write data

  Serial.print(nom);
  Serial.print("received : ");
  Serial.print(String(msg));
}
