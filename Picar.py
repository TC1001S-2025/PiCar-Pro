import RPi.GPIO as GPIO
import time
import Adafruit_PCA9685

class Picar:

    def __init__(self):
        # Inicialización del PCA9685
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)  # Frecuencia estándar para servos (50 Hz)


        #CHASSIS CONSTRUCTOR
        # Pines de los motores
        self.Motor_A_EN    = 4
        self.Motor_B_EN    = 17

        self.Motor_A_Pin1  = 26
        self.Motor_A_Pin2  = 21
        self.Motor_B_Pin1  = 27
        self.Motor_B_Pin2  = 18

        self.pwm1_init = 300
        self.pwm1_max  = 480
        self.pwm1_min  = 160
        self.pwm1_pos  = self.pwm1_init

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.Motor_A_EN, GPIO.OUT)
        GPIO.setup(self.Motor_B_EN, GPIO.OUT)
        GPIO.setup(self.Motor_A_Pin1, GPIO.OUT)
        GPIO.setup(self.Motor_A_Pin2, GPIO.OUT)
        GPIO.setup(self.Motor_B_Pin1, GPIO.OUT)
        GPIO.setup(self.Motor_B_Pin2, GPIO.OUT)

        self.pwm_A = GPIO.PWM(self.Motor_A_EN, 1000)
        self.pwm_B = GPIO.PWM(self.Motor_B_EN, 1000)

        self.pwm_A.start(0)
        self.pwm_B.start(0)

        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)

        self.stop()

        #CLAW CONSTRUCTOR
        # Canal del servo de la garra
        self.CANAL_GARRA = 4


        #LEDS CONSTRUCTOR
        #Inicializa la clase y configura los pines GPIO para los LEDs.
        self.led_pins = [5, 6, 13]  # Pines GPIO para los LEDs
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for pin in self.led_pins:
            GPIO.setup(pin, GPIO.OUT)

        #ARM CONSTRUCTOR 
        # Canal asignado en el PCA9685 para el servo que sube/baja el brazo
        self.arm_up_down_servo = 2
        # Canal asignado en el PCA9685 para el servo que gira el brazo
        self.arm_rotation_servo = 0

        # Definir límites del brazo
        self.min_up_down = 100
        self.max_up_down = 500
        self.min_rotation = 150
        self.max_rotation = 450

        # Posición inicial en 300
        self.position_up_down = 300
        self.actual_rotation = 300

        # Mover a la posición inicial al iniciar
        self.initializePosition()

        #WRIST CONSTRUCTOR
        self.wrist_up_down = 3 

        self.min_wrist_up_down = 300 
        self.max_wrist_up_down = 500  

        self.position_wrist_up_down = 400  

        self.initializeWristPosition()
        
    def initializePosition(self):
        self.pwm.set_pwm(self.arm_up_down_servo, 0, self.position_up_down)
        self.pwm.set_pwm(self.arm_rotation_servo, 0, self.actual_rotation)

#CHASSIS
    def stop(self):
        # Detiene los motores
        GPIO.output(self.Motor_A_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_A_Pin2, GPIO.LOW)
        GPIO.output(self.Motor_B_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_B_Pin2, GPIO.LOW)
        self.pwm_A.ChangeDutyCycle(0)
        self.pwm_B.ChangeDutyCycle(0)

        # Detener servomotor
        self.pwm.set_pwm(1, 0, self.pwm1_init)

    def moveBackward(self, speed=60, duration=3):
        # Mueve las llantas traseras hacia atrás
        GPIO.output(self.Motor_A_Pin1, GPIO.HIGH)
        GPIO.output(self.Motor_A_Pin2, GPIO.LOW)
        GPIO.output(self.Motor_B_Pin1, GPIO.HIGH)
        GPIO.output(self.Motor_B_Pin2, GPIO.LOW)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(duration)
        self.stop()

    def moveForward(self, speed=60, duration=3):
        # Mueve las llantas traseras hacia adelante
        GPIO.output(self.Motor_A_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_A_Pin2, GPIO.HIGH)
        GPIO.output(self.Motor_B_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_B_Pin2, GPIO.HIGH)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)
        
        time.sleep(duration)
        self.stop()

    def rotateRight(self, speed=48, degrees=15):
        # Gira a la derecha y mueve el servomotor pwm1
        self.pwm.set_pwm(1, 0, self.pwm1_min)  # Mover el servomotor pwm1

        GPIO.output(self.Motor_A_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_A_Pin2, GPIO.HIGH)
        GPIO.output(self.Motor_B_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_B_Pin2, GPIO.HIGH)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(degrees / 10)  # Ajustar la duración del giro
        self.stop()

    def rotateLeft(self, speed=52, degrees=15):
        # Gira a la izquierda y mueve el servomotor pwm1
        self.pwm.set_pwm(1, 0, self.pwm1_max)  # Mover el servomotor pwm1

        GPIO.output(self.Motor_A_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_A_Pin2, GPIO.HIGH)
        GPIO.output(self.Motor_B_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_B_Pin2, GPIO.HIGH)
        
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

#CLAW

    # Función para convertir grados a pulsos del PCA9685
    def grados_a_pulsos(self, grados):
        pulso_min = 150   # Aproximadamente 0°
        pulso_max = 600   # Aproximadamente 180°
        return int(pulso_min + (grados / 180.0) * (pulso_max - pulso_min))

    # Método para abrir la garra
    def cerrar_garra(self):
        self.pwm.set_pwm(self.CANAL_GARRA, 0, self.grados_a_pulsos(0))

    # Método para cerrar la garra
    def abrir_garra(self):
        self.pwm.set_pwm(self.CANAL_GARRA, 0, self.grados_a_pulsos(90))  # Ajusta el valor según tu servo

# ARM
    def moveArmUp(self):
        if self.position_up_down + 15 <= self.max_up_down:
            self.position_up_down += 15
            self.pwm.set_pwm(self.arm_up_down_servo, 0, self.position_up_down)
        print("Actual rotation: " + str(self.position_up_down))

    def moveArmDown(self):
        if self.position_up_down - 15 >= self.min_up_down:
            self.position_up_down -= 15
            self.pwm.set_pwm(self.arm_up_down_servo, 0, self.position_up_down)
        print("Actual rotation: " + str(self.position_up_down))

    def rotateArmRight(self):
        if self.actual_rotation + 15 <= self.max_rotation:
            self.actual_rotation += 15
            self.pwm.set_pwm(self.arm_rotation_servo, 0, self.actual_rotation)
        print("Actual rotation: " + str(self.actual_rotation))

    def rotateArmLeft(self):
        if self.actual_rotation - 15 >= self.min_rotation:
            self.actual_rotation -= 15
            self.pwm.set_pwm(self.arm_rotation_servo, 0, self.actual_rotation)
        print("Actual rotation: " + str(self.actual_rotation))

#WRIST
    def initializeWristPosition(self):
        self.pwm.set_pwm(self.wrist_up_down, 0, self.position_wrist_up_down)

    def moveWristUp(self):
        if self.position_wrist_up_down + 15 <= self.max_wrist_up_down:
            self.position_wrist_up_down += 15
            self.pwm.set_pwm(self.wrist_up_down, 0, self.position_wrist_up_down)

    def moveWristDown(self):
        if self.position_wrist_up_down - 15 >= self.min_wrist_up_down:
            self.position_wrist_up_down -= 15
            self.pwm.set_pwm(self.wrist_up_down, 0, self.position_wrist_up_down)