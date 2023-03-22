import serial, time

if __name__ == '__main__':

    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
        time.sleep(0.1)

        if arduino.isOpen():
            print("{} connected!". format(arduino.port))

            try:
                while True:
                    cmd=input("Enter command : ")
                    arduino.write(cmd.encode())

                    while arduino.inWaiting() == 0: pass
                    if arduino.inWaiting()>0:
                        answer =  arduino.readline()
                        print(answer)
                        arduino.flushInput()
            
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")
