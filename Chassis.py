import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685

# Pines de los motores
Motor_A_EN    = 4
Motor_B_EN    = 17

Motor_A_Pin1  = 26
Motor_A_Pin2  = 21
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

# Pines del servomotor
pwm1_init = 300
pwm1_max  = 480
pwm1_min  = 160
pwm1_pos  = pwm1_init

class Chassis:
    def __init__(self):
        # Inicializa los pines y PWM para los motores
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

        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)

        self.stop()

    def stop(self):
        # Detiene los motores
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        self.pwm_A.ChangeDutyCycle(0)
        self.pwm_B.ChangeDutyCycle(0)

        # Detener servomotor
        self.pwm.set_pwm(1, 0, pwm1_init)

    def moveBackward(self, speed=60, duration=3):
        # Mueve las llantas traseras hacia atrás
        GPIO.output(Motor_A_Pin1, GPIO.HIGH)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.HIGH)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(duration)
        self.stop()

    def moveForward(self, speed=60, duration=3):
        # Mueve las llantas traseras hacia adelante
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.HIGH)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.HIGH)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(duration)
        self.stop()

    def rotateRight(self, speed=60, degrees=15):
        # Gira a la derecha y mueve el servomotor pwm1
        self.pwm.set_pwm(1, 0, pwm1_min)  # Mover el servomotor pwm1

        GPIO.output(Motor_A_Pin1, GPIO.HIGH)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.HIGH)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(degrees / 10)  # Ajustar la duración del giro
        self.stop()

    def rotateLeft(self, speed=60, degrees=15):
        # Gira a la izquierda y mueve el servomotor pwm1
        self.pwm.set_pwm(1, 0, pwm1_max)  # Mover el servomotor pwm1

        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.HIGH)
        GPIO.output(Motor_B_Pin1, GPIO.HIGH)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(degrees / 10)  # Ajustar la duración del giro
        self.stop()

    def cleanup(self):
        # Limpia los pines GPIO y apaga todo
        self.stop()
        GPIO.cleanup()