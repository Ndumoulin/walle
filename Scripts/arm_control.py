import serial, time
import os
import pygame
from pygame.constants import JOYBUTTONDOWN, JOYBUTTONUP, JOYAXISMOTION, JOYHATMOTION

t = time.localtime()

class XBOXController(object):
    """Class representing the XBOX controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None
    

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        

    def listen(self):
        with serial.Serial("/dev/ttyUSB0", 115200, timeout=1) as arduino:
            time.sleep(0.1)

            if arduino.isOpen():
                print("{} connected!". format(arduino.port))
                
                    
            """Listen for events to happen"""
            
            if not self.axis_data:
                self.axis_data = {}

            if not self.button_data:
                self.button_data = {}
                for i in range(self.controller.get_numbuttons()):
                    self.button_data[i] = False

            if not self.hat_data:
                self.hat_data = {}
                for i in range(self.controller.get_numhats()):
                    self.hat_data[i] = (0, 0)

            while True:
                
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        self.axis_data[event.axis] = round(event.value,2)
                        if self.controller.get_axis(2) > 0.3:
                            arduino.write(b"A")0
                            
                            
                            
                            
                            
                            
                            
                            
                            print(self.controller.get_axis(2))
                        if self.controller.get_axis(2) < -0.3:
                            arduino.write(b"B")
                            print(self.controller.get_axis(2))
                    elif event.type == pygame.JOYBUTTONDOWN:
                        self.button_data[event.button] = True
                        if event.button == 7:
                            arduino.write(b"R")
                        if event.button == 6:
                            arduino.write(b"L")
                    elif event.type == pygame.JOYBUTTONUP:
                        self.button_data[event.button] = False
                    elif event.type == pygame.JOYHATMOTION:
                        self.hat_data[event.hat] = event.value

                    # Insert your code on what you would like to happen for each event here!
                    # In the current setup, I have the state simply printing out to the screen.
                    
                    #os.system('cls' if os.name == 'nt' else 'clear')
                    


def controller_main():
    xbox = XBOXController()
    xbox.init()
    xbox.listen()
    

controller_main()

"""
pygame.init()
pygame.joystick.init()

try:
    controller = pygame.joystick.Joystick(0)
    controller.init()
    
except:
    print("WRONG")

#joysticks = []

#for i in range(0, pygame.joystick.get_count()):
#   joysticks.append(pygame.joystick.Joystick(i))
#    joysticks[-1].init()

if __name__ == '__main__':

    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
        time.sleep(0.1)

        if arduino.isOpen():
            print("{} connected!". format(arduino.port))

            try:
                while True:

                    #check for joystick events

                    for event in pygame.event.get():
                        if event.type == JOYBUTTONDOWN:
                            if event.button == 7:
                                arduino.write(b"RB")
                                print("Button RB down")
                            if event.button == 6:
                                arduino.write(b"LB")
                                print("Button LB down")
                                
                        if event.type == JOYAXISMOTION:
                            if controller.get_axis(2) > 0.5 :
                                #print(controller.get_axis(2))
                                arduino.write(b"A,1")
                                print("axis")
                            if controller.get_axis(2) < 0.5 :
                                #print(controller.get_axis(2))
                                arduino.write(b"A,-1")
                                print("axis")
                                
                    
                            
                            
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")
"""
