import serial
byte_to_send = 54 # Replace this with the byte you want to send

with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
    arduino.flush()
    arduino.write(byte_to_send)
    
    if arduino.isOpen():
                print("{} connected!". format(arduino.port))

    if arduino.in_waiting > 0:
        print("in waiting")
        byte_received = arduino.read()
        print("Received:", byte_received)

    arduino.close()