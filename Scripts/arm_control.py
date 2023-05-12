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
    
    commands = [0,0,0,0,0,0,1]
    drivingMode = True
    

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        
    def generate_command(self):
        line = ";".join(str(x) for x in self.commands)
        ##print(line)
        return line
        

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
                previous_commands = self.commands.copy()
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        self.axis_data[event.axis] = round(event.value,2)
                        
                        if self.drivingMode == True:
                            """LEFT DC motors control"""
                            if event.axis == 1 and self.axis_data[event.axis] == 0 and self.commands[0] != 0:
                                self.commands[0] = 0
                            if event.axis == 1 and self.axis_data[event.axis] >= 0.5 and self.commands[0] != -100:
                                self.commands[0] = -100
                            if event.axis == 1 and self.axis_data[event.axis] <= -0.5 and self.commands[0] != 100:
                                self.commands[0] = 100
                                
                            """RIGHT DC motors control"""
                            if event.axis == 3 and self.axis_data[event.axis] == 0 and self.commands[1] != 0:
                                self.commands[1] = 0
                            if event.axis == 3 and self.axis_data[event.axis] >= 0.5 and self.commands[1] != -100:
                                self.commands[1] = -100
                            if event.axis == 3 and self.axis_data[event.axis] <= -0.5 and self.commands[1] != 100:
                                self.commands[1] = 100
                            
                        if self.drivingMode == False:
                            """Shoulder servo control"""
                            
                            if event.axis == 3 and self.axis_data[event.axis] == 0 and self.commands[3] != 0:
                                self.commands[3] = 0
                            if event.axis == 3 and self.axis_data[event.axis] >= 0.3 and self.commands[3] != -1:
                                self.commands[3] = -1
                            if event.axis == 3 and self.axis_data[event.axis] <= -0.3 and self.commands[3] != 1:
                                self.commands[3] = 1
                                
                            """Elbow servo control"""
                            
                            if event.axis == 1 and self.axis_data[event.axis] == 0 and self.commands[4] != 0:
                                self.commands[4] = 0
                            if event.axis == 1 and self.axis_data[event.axis] >= 0.3 and self.commands[4] != -1:
                                self.commands[4] = 1
                            if event.axis == 1 and self.axis_data[event.axis] <= -0.3 and self.commands[4] != 1:
                                self.commands[4] = -1
                        
                    elif event.type == pygame.JOYBUTTONDOWN:
                        self.button_data[event.button] = True
                        
                        """Changement de mode"""
                        if event.button == 4 and self.commands[6] == 0:
                            self.commands[6] = 1
                            self.drivingMode = True
                        elif event.button == 4 and self.commands[6] == 1:
                            self.commands[6] = 0
                            self.drivingMode = False
                        
                        if self.drivingMode == False:
                            """Waist servo control"""
                            
                            if event.button == 7:
                                self.commands[2] = -1
                            if event.button == 6:
                                self.commands[2] = 1
                                
                        """Magnet control"""
                        if event.button == 3:
                            if self.commands[5] == 0:
                                self.commands[5] = 1
                            elif self.commands[5] == 1:
                                self.commands[5] = 0
                                
                    elif event.type == pygame.JOYBUTTONUP:
                        self.button_data[event.button] = False
                        if event.button == 7:
                            self.commands[2] = 0
                        if event.button == 6:
                            self.commands[2] = 0
                            
                    elif event.type == pygame.JOYHATMOTION:
                        self.hat_data[event.hat] = event.value
                        
                    if previous_commands != self.commands:
                        arduino.write(str.encode(self.generate_command()))
                        print(str.encode(self.generate_command()))
                        
      
def convert_data(x):
    return int(x * 255)
    

def controller_main():
    xbox = XBOXController()
    xbox.init()
    xbox.listen()


controller_main()
