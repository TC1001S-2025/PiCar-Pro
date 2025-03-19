import time
import RPi.GPIO as GPIO
import time
import Adafruit_PCA9685

class Picar:

    def __init__(self):
        #CHASSIS CONSTRUCTOR
        # Pines de los motores
        self.Motor_A_EN    = 4
        self.Motor_B_EN    = 17

        self.Motor_A_Pin1  = 26
        self.Motor_A_Pin2  = 21
        self.Motor_B_Pin1  = 27
        self.Motor_B_Pin2  = 18

        self.Dir_forward   = 0
        self.Dir_backward  = 1

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

        self.stop()

        #CLAW CONSTRUCTOR
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        self.pwm3_init = 300
        self.pwm3_max  = 500
        self.pwm3_min  = 300
        self.pwm3_pos  = pwm3_init

    def stop(self):
        #Detiene los motores
        GPIO.output(self.Motor_A_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_A_Pin2, GPIO.LOW)
        GPIO.output(self.Motor_B_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_B_Pin2, GPIO.LOW)
        self.pwm_A.ChangeDutyCycle(0)
        self.pwm_B.ChangeDutyCycle(0)

    def moveBackward(self, speed=60, duration=3):
        #Mueve el chasis hacia atras por la duración especificada
        GPIO.output(self.Motor_A_Pin1, GPIO.HIGH)
        GPIO.output(self.Motor_A_Pin2, GPIO.LOW)
        GPIO.output(self.Motor_B_Pin1, GPIO.HIGH)
        GPIO.output(self.Motor_B_Pin2, GPIO.LOW)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(duration)
        self.stop()

    def moveForward(self, speed=60, duration=3):
        #Mueve el chasis hacia adelante por la duración especificada
        GPIO.output(self.Motor_A_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_A_Pin2, GPIO.HIGH)
        GPIO.output(self.Motor_B_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_B_Pin2, GPIO.HIGH)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(duration)
        self.stop()

    def rotateRight(self, speed=60, degrees=15):
        #Gira a la derecha durante un ángulo determinado
        max_degrees = 35
        degrees = min(degrees, max_degrees)
        duration = degrees / 10  # Ajusta la duración del giro

        GPIO.output(self.Motor_A_Pin1, GPIO.HIGH)
        GPIO.output(self.Motor_A_Pin2, GPIO.LOW)
        GPIO.output(self.Motor_B_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_B_Pin2, GPIO.HIGH)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(duration)
        self.stop()

    def rotateLeft(self, speed=60, degrees=15):
        #Gira a la izquierda durante un ángulo determinado"""
        max_degrees = 35
        degrees = min(degrees, max_degrees)
        duration = degrees / 10  # Ajusta la duración del giro

        GPIO.output(self.Motor_A_Pin1, GPIO.LOW)
        GPIO.output(self.Motor_A_Pin2, GPIO.HIGH)
        GPIO.output(self.Motor_B_Pin1, GPIO.HIGH)
        GPIO.output(self.Motor_B_Pin2, GPIO.LOW)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(duration)
        self.stop()

    def cleanup(self):
        #Limpia los pines GPIO"""
        self.stop()
        GPIO.cleanup()

#CLAW
    def ctrl_range(self, raw, max_genout, min_genout):
        if raw > max_genout:
            raw_output = max_genout
        elif raw < min_genout:
            raw_output = min_genout
        else:
            raw_output = raw
        return int(raw_output)

    """
    def moveClawUp(self, speed=1):
        new_pos = self.arm_pos - speed
        self.arm_pos = self._clamp(new_pos, self.arm_min, self.arm_max)
        self.pwm.set_pwm(self.arm_channel, 0, self.arm_pos)
        time.sleep(0.02)

    def moveClawDown(self, speed=1):
        new_pos = self.arm_pos + speed
        self.arm_pos = self._clamp(new_pos, self.arm_min, self.arm_max)
        self.pwm.set_pwm(self.arm_channel, 0, self.arm_pos)
        time.sleep(0.02)"""

    def closeClaw(self,speed):
        global pwm3_pos
        if self.pwm3_direction:
            pwm3_pos -= speed
            pwm3_pos = ctrl_range(pwm3_pos, self.pwm3_max, self.pwm3_min)
            self.pwm.set_pwm(3, 0, pwm3_pos)
        else:
            pwm3_pos += speed
            pwm3_pos = ctrl_range(pwm3_pos, self.pwm3_max, self.pwm3_min)
            self.pwm.set_pwm(3, 0, pwm3_pos)
        print(pwm3_pos)


    def openClaw(self, speed):
        global pwm3_pos
        if self.pwm3_direction:
            pwm3_pos += speed
            pwm3_pos = ctrl_range(pwm3_pos, self.pwm3_max, self.pwm3_min)
            self.pwm.set_pwm(3, 0, pwm3_pos)
        else:
            pwm3_pos -= speed
            pwm3_pos = ctrl_range(pwm3_pos, self.pwm3_max, self.pwm3_min)
            self.pwm.set_pwm(3, 0, pwm3_pos)
        print(pwm3_pos)

# ARM
    def moveArmUp(self):
        pass

    def moveArmDown(self):
        pass

    def rotateArmRight(self):
        pass
    
    def rotateArmLeft(self):
        pass