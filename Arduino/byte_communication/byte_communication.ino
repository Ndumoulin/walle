void setup() {
  Serial.begin(9600); // Make sure the baud rate matches the Raspberry Pi side
}

void loop() {
  if (Serial.available() > 0) {
    int incomingByte = Serial.read();
    Serial.print("Received: ");
    Serial.println(incomingByte, DEC);
  }
}
