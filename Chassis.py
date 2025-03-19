import time
import RPi.GPIO as GPIO

# Pines de los motores
Motor_A_EN    = 4
Motor_B_EN    = 17

Motor_A_Pin1  = 26
Motor_A_Pin2  = 21
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

Dir_forward   = 0
Dir_backward  = 1

class Chassis:
    def __init__(self):
        #Inicializa los pines y PWM para los motores
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(Motor_A_EN, GPIO.OUT)
        GPIO.setup(Motor_B_EN, GPIO.OUT)
        GPIO.setup(Motor_A_Pin1, GPIO.OUT)
        GPIO.setup(Motor_A_Pin2, GPIO.OUT)
        GPIO.setup(Motor_B_Pin1, GPIO.OUT)
        GPIO.setup(Motor_B_Pin2, GPIO.OUT)

        self.pwm_A = GPIO.PWM(Motor_A_EN, 1000)
        self.pwm_B = GPIO.PWM(Motor_B_EN, 1000)

        self.pwm_A.start(0)
        self.pwm_B.start(0)

        self.stop()

    def stop(self):
        #Detiene los motores
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        self.pwm_A.ChangeDutyCycle(0)
        self.pwm_B.ChangeDutyCycle(0)

    def moveBackward(self, speed=60, duration=3):
        #Mueve el chasis hacia atras por la duración especificada
        GPIO.output(Motor_A_Pin1, GPIO.HIGH)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.HIGH)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(duration)
        self.stop()

    def moveForward(self, speed=60, duration=3):
        #Mueve el chasis hacia adelante por la duración especificada
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.HIGH)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.HIGH)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(duration)
        self.stop()

    def rotateRight(self, speed=60, degrees=15):
        #Gira a la derecha durante un ángulo determinado
        max_degrees = 35
        degrees = min(degrees, max_degrees)
        duration = degrees / 10  # Ajusta la duración del giro

        GPIO.output(Motor_A_Pin1, GPIO.HIGH)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.HIGH)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(duration)
        self.stop()

    def rotateLeft(self, speed=60, degrees=15):
        #Gira a la izquierda durante un ángulo determinado"""
        max_degrees = 35
        degrees = min(degrees, max_degrees)
        duration = degrees / 10  # Ajusta la duración del giro

        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.HIGH)
        GPIO.output(Motor_B_Pin1, GPIO.HIGH)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(duration)
        self.stop()

    def cleanup(self):
        #Limpia los pines GPIO"""
        self.stop()
        GPIO.cleanup()