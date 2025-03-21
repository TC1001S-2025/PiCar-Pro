import RPi.GPIO as GPIO
import time
import Adafruit_PCA9685

class Picar:
    """
    Clase para controlar el robot Picar, que integra:
    - Chasis (motores para desplazamiento).
    - Brazo robótico (movimientos de pitch y yaw).
    - Garra (apertura y cierre).
    - Muñeca (ajuste de pitch).
    - LEDs (iluminación).
    
    Utiliza la librería Adafruit_PCA9685 para controlar servomotores a través del PWM,
    y RPi.GPIO para el manejo de los pines GPIO de la Raspberry Pi.
    """

    def __init__(self):
        """
        Constructor de la clase.
        Inicializa constantes, configura pines GPIO, inicia la comunicación con el PCA9685
        y posiciona los servomotores a sus posiciones iniciales.
        """
        # CONSTANTES DEL CHASIS
        self.MOTOR_A_EN    = 4        # Pin de habilitación del motor A
        self.MOTOR_B_EN    = 17       # Pin de habilitación del motor B

        self.MOTOR_A_PIN1  = 26       # Pin 1 para dirección del motor A
        self.MOTOR_A_PIN2  = 21       # Pin 2 para dirección del motor A
        self.MOTOR_B_PIN1  = 27       # Pin 1 para dirección del motor B
        self.MOTOR_B_PIN2  = 18       # Pin 2 para dirección del motor B

        self.PWM1_INITIAL_POSITION = 300  # Posición inicial del servomotor PWM1
        self.PWM1_MAX_YAW  = 480            # Límite máximo para giro (yaw)
        self.PWM1_MIN_YAW  = 160            # Límite mínimo para giro (yaw)

        # CONSTANTES DEL BRAZO ROBÓTICO
        self.ARM_PITCH_SERVO = 2          # Canal PWM para el movimiento de pitch del brazo
        self.ARM_YAW_SERVO = 0            # Canal PWM para el movimiento de yaw del brazo
        self.ARM_INITIAL_PITCH = 300      # Posición inicial de pitch
        self.ARM_INITIAL_YAW = 300        # Posición inicial de yaw

        # Límites del brazo
        self.ARM_MIN_PITCH = 100          # Límite mínimo para pitch
        self.ARM_MAX_PITCH = 500          # Límite máximo para pitch
        self.ARM_MIN_YAW = 150            # Límite mínimo para yaw
        self.ARM_MAX_YAW = 450            # Límite máximo para yaw

        # CONSTANTES DE LA GARRA
        self.CLAW_CHANNEL = 4             # Canal PWM para la garra

        # CONSTANTES DE LA MUÑECA
        self.WRIST_SERVO = 3              # Canal PWM para la muñeca
        self.WRIST_MIN_PITCH = 300        # Límite mínimo para el pitch de la muñeca
        self.WRIST_MAX_PITCH = 500        # Límite máximo para el pitch de la muñeca
        self.WRIST_INITIAL_PITCH = 400    # Posición inicial del pitch de la muñeca

        # CONSTANTES DE LOS LEDS
        self.LED_PINS = [5, 6, 13]        # Pines de los LEDs

        # CONSTRUCCIÓN E INICIALIZACIÓN DEL PCA9685
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)  # Frecuencia estándar para servos (50 Hz)

        # CONFIGURACIÓN DEL CHASIS
        self.pwm1_pos  = self.PWM1_INITIAL_POSITION
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # Configuración de los pines de los motores como salidas
        GPIO.setup(self.MOTOR_A_EN, GPIO.OUT)
        GPIO.setup(self.MOTOR_B_EN, GPIO.OUT)
        GPIO.setup(self.MOTOR_A_PIN1, GPIO.OUT)
        GPIO.setup(self.MOTOR_A_PIN2, GPIO.OUT)
        GPIO.setup(self.MOTOR_B_PIN1, GPIO.OUT)
        GPIO.setup(self.MOTOR_B_PIN2, GPIO.OUT)

        # Configuración del PWM para el control de velocidad de los motores
        self.pwm_A = GPIO.PWM(self.MOTOR_A_EN, 1000)  # Frecuencia de 1000 Hz
        self.pwm_B = GPIO.PWM(self.MOTOR_B_EN, 1000)

        self.pwm_A.start(0)
        self.pwm_B.start(0)

        # Detener motores al iniciar
        self.stop()

        # CONFIGURACIÓN DE LOS LEDS
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for pin in self.LED_PINS:
            GPIO.setup(pin, GPIO.OUT)

        # CONFIGURACIÓN DE LA MUÑECA
        self.wrist_actual_pitch = self.WRIST_INITIAL_PITCH

        # CONFIGURACIÓN DEL BRAZO
        self.arm_actual_pitch = self.ARM_INITIAL_PITCH
        self.arm_actual_yaw = self.ARM_INITIAL_YAW

        # Posicionar los servos a sus posiciones iniciales
        self.initializePosition()
        
    def initializePosition(self):
        """
        Posiciona los servomotores del brazo y la muñeca a sus posiciones iniciales.
        """
        self.pwm.set_pwm(self.ARM_PITCH_SERVO, 0, self.ARM_INITIAL_PITCH)
        self.pwm.set_pwm(self.ARM_YAW_SERVO, 0, self.ARM_INITIAL_YAW)
        self.pwm.set_pwm(self.WRIST_SERVO, 0, self.WRIST_INITIAL_PITCH)

    # MÉTODOS DEL CHASIS

    def stop(self):
        """
        Detiene el movimiento del chasis:
        - Apaga los pines de dirección de los motores.
        - Establece el ciclo de trabajo del PWM de los motores a 0.
        - Restablece la posición del servomotor PWM1 a la posición inicial.
        """
        GPIO.output(self.MOTOR_A_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_A_PIN2, GPIO.LOW)
        GPIO.output(self.MOTOR_B_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_B_PIN2, GPIO.LOW)
        self.pwm_A.ChangeDutyCycle(0)
        self.pwm_B.ChangeDutyCycle(0)

        # Restablecer el servomotor PWM1
        self.pwm.set_pwm(1, 0, self.PWM1_INITIAL_POSITION)

    def moveBackward(self, speed=60, duration=1):
        """
        Mueve el robot hacia atrás.
        
        Parámetros:
            speed (int): Velocidad de movimiento (valor del ciclo de trabajo).
            duration (float): Tiempo en segundos que se mantendrá el movimiento.
        """
        # Configuración de pines para mover los motores hacia atrás
        GPIO.output(self.MOTOR_A_PIN1, GPIO.HIGH)
        GPIO.output(self.MOTOR_A_PIN2, GPIO.LOW)
        GPIO.output(self.MOTOR_B_PIN1, GPIO.HIGH)
        GPIO.output(self.MOTOR_B_PIN2, GPIO.LOW)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(duration)
        self.stop()

    def moveForward(self, speed=60, duration=1):
        """
        Mueve el robot hacia adelante.
        
        Parámetros:
            speed (int): Velocidad de movimiento (valor del ciclo de trabajo).
            duration (float): Tiempo en segundos que se mantendrá el movimiento.
        """
        # Configuración de pines para mover los motores hacia adelante
        GPIO.output(self.MOTOR_A_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_A_PIN2, GPIO.HIGH)
        GPIO.output(self.MOTOR_B_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_B_PIN2, GPIO.HIGH)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)
        
        time.sleep(duration)
        self.stop()

    def rotateRight(self, speed=48, degrees=15):
        """
        Rota el robot a la derecha.
        
        Además, mueve el servomotor PWM1 a una posición definida para el giro a la derecha.
        
        Parámetros:
            speed (int): Velocidad de giro.
            degrees (int): Grados de giro (utilizados para calcular la duración).
        """
        # Mover el servomotor PWM1 a la posición mínima (giro a la derecha)
        self.pwm.set_pwm(1, 0, self.PWM1_MIN_YAW)

        GPIO.output(self.MOTOR_A_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_A_PIN2, GPIO.HIGH)
        GPIO.output(self.MOTOR_B_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_B_PIN2, GPIO.HIGH)

        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(degrees / 10)  # Duración del giro ajustada a los grados
        self.stop()

    def rotateLeft(self, speed=52, degrees=15):
        """
        Rota el robot a la izquierda.
        
        Además, mueve el servomotor PWM1 a una posición definida para el giro a la izquierda.
        
        Parámetros:
            speed (int): Velocidad de giro.
            degrees (int): Grados de giro (utilizados para calcular la duración).
        """
        # Mover el servomotor PWM1 a la posición máxima (giro a la izquierda)
        self.pwm.set_pwm(1, 0, self.PWM1_MAX_YAW)

        GPIO.output(self.MOTOR_A_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_A_PIN2, GPIO.HIGH)
        GPIO.output(self.MOTOR_B_PIN1, GPIO.LOW)
        GPIO.output(self.MOTOR_B_PIN2, GPIO.HIGH)
        
        self.pwm_A.ChangeDutyCycle(speed)
        self.pwm_B.ChangeDutyCycle(speed)

        time.sleep(degrees / 10)  # Duración del giro ajustada a los grados
        self.stop()

    def cleanup(self):
        """
        Limpia la configuración de los pines GPIO y detiene todos los movimientos.
        Se debe llamar antes de finalizar la ejecución del programa.
        """
        self.stop()
        GPIO.cleanup()

    # MÉTODOS PARA LOS LEDS

    def switch(self, port, status):
        """
        Controla el estado de un LED individual.
        
        Parámetros:
            port (int): Número del puerto (1, 2 o 3) que identifica el LED.
            status (int): Estado deseado (1 para encender, 0 para apagar).
            
        Si se ingresa un puerto no válido, se imprime un mensaje de error.
        """
        if port == 1:
            GPIO.output(5, GPIO.HIGH if status == 1 else GPIO.LOW)
        elif port == 2:
            GPIO.output(6, GPIO.HIGH if status == 1 else GPIO.LOW)
        elif port == 3:
            GPIO.output(13, GPIO.HIGH if status == 1 else GPIO.LOW)
        else:
            print('Wrong Command: Example--switch(3, 1)->to switch on port3')

    def ledOff(self):
        """
        Apaga todos los LEDs.
        """
        self.switch(1, 0)
        self.switch(2, 0)
        self.switch(3, 0)

    def ledOn(self):
        """
        Enciende todos los LEDs.
        """
        self.switch(1, 1)
        self.switch(2, 1)
        self.switch(3, 1)

    # MÉTODOS PARA LA GARRA

    def degreesToPulse(self, grados):
        """
        Convierte un ángulo en grados a un pulso PWM correspondiente para el servo.
        
        Parámetros:
            grados (float): Ángulo en grados (de 0 a 180).
            
        Retorna:
            int: Valor de pulso correspondiente.
            
        Los valores de pulso mínimo y máximo se definen para representar aproximadamente 0° y 180°.
        """
        pulso_min = 150   # Aproximadamente 0°
        pulso_max = 600   # Aproximadamente 180°
        return int(pulso_min + (grados / 180.0) * (pulso_max - pulso_min))

    def closeClaw(self):
        """
        Abre la garra (movimiento de apertura).
        
        Se espera 1 segundo antes de mover el servo y 0.5 segundos después para estabilizar el movimiento.
        """
        time.sleep(1)
        self.pwm.set_pwm(self.CLAW_CHANNEL, 0, self.degreesToPulse(0))
        time.sleep(0.5)

    def openClaw(self):
        """
        Cierra la garra (movimiento de cierre).
        
        El valor del pulso se ajusta para posicionar el servo en 90° (ajustable según el servo).
        """
        self.pwm.set_pwm(self.CLAW_CHANNEL, 0, self.degreesToPulse(90))

    # MÉTODOS PARA EL BRAZO ROBÓTICO

    def moveArmUp(self):
        """
        Mueve el brazo hacia arriba incrementando el ángulo de pitch.
        Verifica que no se supere el límite máximo.
        """
        if self.arm_actual_pitch + 15 <= self.ARM_MAX_PITCH:
            self.arm_actual_pitch += 15
            self.pwm.set_pwm(self.ARM_PITCH_SERVO, 0, self.arm_actual_pitch)

    def moveArmDown(self):
        """
        Mueve el brazo hacia abajo disminuyendo el ángulo de pitch.
        Verifica que no se supere el límite mínimo.
        """
        if self.arm_actual_pitch - 15 >= self.ARM_MIN_PITCH:
            self.arm_actual_pitch -= 15
            self.pwm.set_pwm(self.ARM_PITCH_SERVO, 0, self.arm_actual_pitch)

    def rotateArmRight(self):
        """
        Rota el brazo hacia la derecha incrementando el ángulo de yaw.
        Verifica que no se supere el límite máximo.
        """
        if self.arm_actual_yaw + 15 <= self.ARM_MAX_YAW:
            self.arm_actual_yaw += 15
            self.pwm.set_pwm(self.ARM_YAW_SERVO, 0, self.arm_actual_yaw)

    def rotateArmLeft(self):
        """
        Rota el brazo hacia la izquierda disminuyendo el ángulo de yaw.
        Verifica que no se supere el límite mínimo.
        """
        if self.arm_actual_yaw - 15 >= self.ARM_MIN_YAW:
            self.arm_actual_yaw -= 15
            self.pwm.set_pwm(self.ARM_YAW_SERVO, 0, self.arm_actual_yaw)

    # MÉTODOS PARA LA MUÑECA

    def moveWristUp(self):
        """
        Mueve la muñeca hacia arriba incrementando el ángulo de pitch.
        Verifica que no se supere el límite máximo.
        """
        if self.wrist_actual_pitch + 15 <= self.WRIST_MAX_PITCH:
            self.wrist_actual_pitch += 15
            self.pwm.set_pwm(self.WRIST_SERVO, 0, self.wrist_actual_pitch)

    def moveWristDown(self):
        """
        Mueve la muñeca hacia abajo disminuyendo el ángulo de pitch.
        Verifica que no se supere el límite mínimo.
        """
        if self.wrist_actual_pitch - 15 >= self.WRIST_MIN_PITCH:
            self.wrist_actual_pitch -= 15
            self.pwm.set_pwm(self.WRIST_SERVO, 0, self.wrist_actual_pitch)
