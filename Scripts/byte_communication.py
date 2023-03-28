import serial, time
byte_to_send = b'\x41' # Replace this with the byte you want to send

with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
    
    time.sleep(0.1)
    arduino.flush()
    arduino.write(bytes([22]))
    
    if arduino.isOpen():
                print("{} connected!". format(arduino.port))

    if arduino.in_waiting > 0:
        print("in waiting")
        byte_received = arduino.read()
        print("Received:", byte_received)

    arduino.close()