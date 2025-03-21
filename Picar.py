import RPi.GPIO as GPIO
import time
import Adafruit_PCA9685

class Picar:

    def __init__(self):

        # CONSTANTS
        # CHASSIS CONSTANTS
        self.MOTOR_A_EN    = 4
        self.MOTOR_B_EN    = 17

        self.MOTOR_A_PIN1  = 26
        self.MOTOR_A_PIN2  = 21
        self.MOTOR_B_PIN1  = 27
        self.MOTOR_B_PIN2  = 18

        self.PWM1_INITIAL_POSITION = 300
        self.PWM1_MAX_YAW  = 480
        self.PWM1_MIN_YAW  = 160

        # ARM CONSTANTS
        self.ARM_PITCH_SERVO = 2
        self.ARM_YAW_SERVO = 0
        self.ARM_INITIAL_PITCH = 300
        self.ARM_INITIAL_YAW = 300

        # Definir límites del brazo
        self.ARM_MIN_PITCH = 100
        self.ARM_MAX_PITCH = 500
        self.ARM_MIN_YAW = 150
        self.ARM_MAX_YAW = 450

        # CLAW CONSTANTS
        self.CLAW_CHANNEL = 4

        # WRIST CONSTANTS
        self.WRIST_SERVO = 3 

        self.WRIST_MIN_PITCH = 300 
        self.WRIST_MAX_PITCH = 500  

        self.WRIST_INITIAL_PITCH = 400  

        # lEDS CONSTANTS
        self.LED_PINS = [5, 6, 13]

        # CONSTRUCTORS
        # Inicialización del PCA9685
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)  # Frecuencia estándar para servos (50 Hz)

        #CHASSIS
        self.pwm1_pos  = self.PWM1_INITIAL_POSITION
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.MOTOR_A_EN, GPIO.OUT)
        GPIO.setup(self.MOTOR_B_EN, GPIO.OUT)
        GPIO.setup(self.MOTOR_A_PIN1, GPIO.OUT)
        GPIO.setup(self.MOTOR_A_PIN2, GPIO.OUT)
        GPIO.setup(self.MOTOR_B_PIN1, GPIO.OUT)
        GPIO.setup(self.MOTOR_B_PIN2, GPIO.OUT)

        self.pwm_A = GPIO.PWM(self.MOTOR_A_EN, 1000)
        self.pwm_B = GPIO.PWM(self.MOTOR_B_EN, 1000)

        self.pwm_A.start(0)
        self.pwm_B.start(0)

        self.stop()

        #LEDS CONSTRUCTOR
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for pin in self.LED_PINS:
            GPIO.setup(pin, GPIO.OUT)

        #WRIST CONSTRUCTOR
        self.wrist_actual_pitch = self.WRIST_INITIAL_PITCH

        #ARM CONSTRUCTOR
        self.arm_actual_pitch = self.ARM_INITIAL_PITCH
        self.arm_actual_yaw = self.ARM_INITIAL_YAW

        # Mover servos a la posición inicial al iniciar
        self.initializePosition()
        
    def initializePosition(self):
        self.pwm.set_pwm(self.ARM_PITCH_SERVO, 0, self.ARM_INITIAL_PITCH)
        self.pwm.set_pwm(self.ARM_YAW_SERVO, 0, self.ARM_INITIAL_YAW)
        self.pwm.set_pwm(self.WRIST_SERVO, 0, self.WRIST_INITIAL_PITCH)

#CHASSIS
    def stop(self):
        # Detiene los motores
        GPIO.output(self.MOTOR_A_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_A_PIN2, GPIO.LOW)
        GPIO.output(self.MOTOR_B_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_B_PIN2, GPIO.LOW)
        self.pwm_A.ChangeDutyCycle(0)
        self.pwm_B.ChangeDutyCycle(0)

        # Detener servomotor
        self.pwm.set_pwm(1, 0, self.PWM1_INITIAL_POSITION)

    def moveBackward(self, speed=60, duration=1):
        # Mueve las llantas traseras hacia atrás
        GPIO.output(self.MOTOR_A_PIN1, GPIO.HIGH)
        GPIO.output(self.MOTOR_A_PIN2, GPIO.LOW)
        GPIO.output(self.MOTOR_B_PIN1, GPIO.HIGH)
        GPIO.output(self.MOTOR_B_PIN2, GPIO.LOW)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(duration)
        self.stop()

    def moveForward(self, speed=60, duration=1):
        # Mueve las llantas traseras hacia adelante
        GPIO.output(self.MOTOR_A_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_A_PIN2, GPIO.HIGH)
        GPIO.output(self.MOTOR_B_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_B_PIN2, GPIO.HIGH)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)
        
        time.sleep(duration)
        self.stop()

    def rotateRight(self, speed=48, degrees=15):
        # Gira a la derecha y mueve el servomotor pwm1
        self.pwm.set_pwm(1, 0, self.PWM1_ARM_MIN_YAW)  # Mover el servomotor pwm1

        GPIO.output(self.MOTOR_A_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_A_PIN2, GPIO.HIGH)
        GPIO.output(self.MOTOR_B_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_B_PIN2, GPIO.HIGH)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(degrees / 10)  # Ajustar la duración del giro
        self.stop()

    def rotateLeft(self, speed=52, degrees=15):
        # Gira a la izquierda y mueve el servomotor pwm1
        self.pwm.set_pwm(1, 0, self.PWM1_MAX_YAW)  # Mover el servomotor pwm1

        GPIO.output(self.MOTOR_A_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_A_PIN2, GPIO.HIGH)
        GPIO.output(self.MOTOR_B_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_B_PIN2, GPIO.HIGH)
        
        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(degrees / 10)  # Ajustar la duración del giro
        self.stop()

    def cleanup(self):
        # Limpia los pines GPIO y apaga todo
        self.stop()
        GPIO.cleanup()

#LEDS
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

    def ledOff(self):
        #Apaga todos los LEDs.
        self.switch(1, 0)
        self.switch(2, 0)
        self.switch(3, 0)

    def ledOn(self):
        #Enciende todos los LEDs.
        self.switch(1, 1)
        self.switch(2, 1)
        self.switch(3, 1)

#CLAW
    # Función para convertir grados a pulsos del PCA9685
    def degreesToPulse(self, grados):
        pulso_min = 150   # Aproximadamente 0°
        pulso_max = 600   # Aproximadamente 180°
        return int(pulso_min + (grados / 180.0) * (pulso_max - pulso_min))

    # Método para abrir la garra
    def closeClaw(self):
        time.sleep(1)
        self.pwm.set_pwm(self.CLAW_CHANNEL, 0, self.degreesToPulse(0))
        time.sleep(0.5)

    # Método para cerrar la garra
    def openClaw(self):
        self.pwm.set_pwm(self.CLAW_CHANNEL, 0, self.degreesToPulse(90))  # Ajusta el valor según tu servo

# ARM
    def moveArmUp(self):
        if self.arm_actual_pitch + 15 <= self.ARM_MAX_PITCH:
            self.arm_actual_pitch += 15
            self.pwm.set_pwm(self.ARM_PITCH_SERVO, 0, self.arm_actual_pitch)
        print("Actual rotation: " + str(self.arm_actual_pitch))

    def moveArmDown(self):
        if self.arm_actual_pitch - 15 >= self.ARM_MIN_PITCH:
            self.arm_actual_pitch -= 15
            self.pwm.set_pwm(self.ARM_PITCH_SERVO, 0, self.arm_actual_pitch)
        print("Actual rotation: " + str(self.arm_actual_pitch))

    def rotateArmRight(self):
        if self.arm_actual_yaw + 15 <= self.ARM_MAX_YAW:
            self.arm_actual_yaw += 15
            self.pwm.set_pwm(self.ARM_YAW_SERVO, 0, self.arm_actual_yaw)
        print("Actual rotation: " + str(self.arm_actual_yaw))

    def rotateArmLeft(self):
        if self.arm_actual_yaw - 15 >= self.ARM_MIN_YAW:
            self.arm_actual_yaw -= 15
            self.pwm.set_pwm(self.ARM_YAW_SERVO, 0, self.arm_actual_yaw)
        print("Actual rotation: " + str(self.arm_actual_yaw))

#WRIST  

    def moveWristUp(self):
        if self.wrist_actual_pitch + 15 <= self.WRIST_MAX_PITCH:
            self.wrist_actual_pitch += 15
            self.pwm.set_pwm(self.WRIST_SERVO, 0, self.wrist_actual_pitch)

    def moveWristDown(self):
        if self.wrist_actual_pitch - 15 >= self.WRIST_MIN_PITCH:
            self.wrist_actual_pitch -= 15
            self.pwm.set_pwm(self.WRIST_SERVO, 0, self.wrist_actual_pitch)