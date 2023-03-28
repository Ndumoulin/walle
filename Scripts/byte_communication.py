import serial
byte_to_send = 0x42 # Replace this with the byte you want to send

with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
    arduino.write(bytes([byte_to_send]))
    
    if arduino.isOpen():
                print("{} connected!". format(arduino.port))

    response = arduino.read()
    print(response)