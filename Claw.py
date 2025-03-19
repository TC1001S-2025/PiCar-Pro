import time
import Adafruit_PCA9685

class Claw:
    def __init__(self, pwm, arm_channel=1, grip_channel=3):
        self.pwm = pwm

        self.arm_channel = arm_channel
        self.arm_init = 300
        self.arm_min = 160
        self.arm_max = 480      
        self.arm_pos = self.arm_init

        self.grip_channel = grip_channel
        self.grip_closed = 300
        self.grip_open = 500
        self.grip_pos = self.grip_open

    def _clamp(self, value, min_value, max_value):
        return max(min_value, min(max_value, value))

    def moveClawUp(self, speed=1):
        new_pos = self.arm_pos - speed
        self.arm_pos = self._clamp(new_pos, self.arm_min, self.arm_max)
        self.pwm.set_pwm(self.arm_channel, 0, self.arm_pos)
        time.sleep(0.02)

    def moveClawDown(self, speed=1):
        new_pos = self.arm_pos + speed
        self.arm_pos = self._clamp(new_pos, self.arm_min, self.arm_max)
        self.pwm.set_pwm(self.arm_channel, 0, self.arm_pos)
        time.sleep(0.02)

    def openClaw(self, speed=1):
        new_pos = self.grip_pos + speed
        self.grip_pos = self._clamp(new_pos, self.grip_closed, self.grip_open)
        self.pwm.set_pwm(self.grip_channel, 0, self.grip_pos)
        time.sleep(0.02)

    def closeClaw(self, speed=1):
        new_pos = self.grip_pos - speed
        self.grip_pos = self._clamp(new_pos, self.grip_closed, self.grip_open)
        self.pwm.set_pwm(self.grip_channel, 0, self.grip_pos)
        time.sleep(0.02)