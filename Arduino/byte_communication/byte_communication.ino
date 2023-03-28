void setup() {
  Serial.begin(9600); // Make sure the baud rate matches the Raspberry Pi side
}

void loop() {
  if (Serial.available() > 0) {
    byte byte_received = Serial.read();
    Serial.write(byte_received);
  }
}
