import serial

ser = serial.Serial('/dev/ttyUSB0', 9600) # Change the port and baud rate to match your setup
byte_to_send = 0x42 # Replace this with the byte you want to send
ser.write(bytes([byte_to_send]))
