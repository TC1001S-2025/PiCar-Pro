import RPi.GPIO as GPIO
import time

class Leds:
    def __init__(self):
        #Inicializa la clase y configura los pines GPIO para los LEDs.
        self.led_pins = [5, 6, 13]  # Pines GPIO para los LEDs
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for pin in self.led_pins:
            GPIO.setup(pin, GPIO.OUT)

    def switch(self, port, status):
        #Controla el estado de un LED individual.
        if port == 1:
            GPIO.output(5, GPIO.HIGH if status == 1 else GPIO.LOW)
        elif port == 2:
            GPIO.output(6, GPIO.HIGH if status == 1 else GPIO.LOW)
        elif port == 3:
            GPIO.output(13, GPIO.HIGH if status == 1 else GPIO.LOW)
        else:
            print('Wrong Command: Example--switch(3, 1)->to switch on port3')

    def LedOff(self):
        #Apaga todos los LEDs.
        self.switch(1, 0)
        self.switch(2, 0)
        self.switch(3, 0)

    def LedOn(self):
        #Enciende todos los LEDs.
        self.switch(1, 1)
        self.switch(2, 1)
        self.switch(3, 1)
