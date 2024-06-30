from machine import Pin, PWM
from utime import ticks_ms

from ...urtps.node import Node
        
class TwoWheelPID(Node):
    """
    A class representing a two-wheel PID controller for motor control.

    Args:
        dt (float): The time interval between control updates in seconds. Default is 0.3 seconds.

    Attributes:
        motor1_pin2 (PWM): The PWM object representing the control pin for motor 1.
        motor1_pin1 (PWM): The PWM object representing the control pin for motor 1.
        motor2_pin2 (PWM): The PWM object representing the control pin for motor 2.
        motor2_pin1 (PWM): The PWM object representing the control pin for motor 2.
        motor1_hall_1 (Pin): The Pin object representing the hall sensor input for motor 1.
        motor1_hall_2 (Pin): The Pin object representing the hall sensor input for motor 1.
        motor2_hall_1 (Pin): The Pin object representing the hall sensor input for motor 2.
        motor2_hall_2 (Pin): The Pin object representing the hall sensor input for motor 2.
        pi1 (PI): The PI controller object for motor 1.
        pi2 (PI): The PI controller object for motor 2.
        last_time (int): The timestamp of the last control update.
        dt (float): The time interval between control updates in seconds.

    """

    def __init__(self, name = 'twoWheelPID', dt=0.3):
        super().__init__(name, 'subscribing')
        # Define motor control pins
        self.motor1_pin2 = PWM(Pin(6, Pin.OUT))
        self.motor1_pin1 = PWM(Pin(7, Pin.OUT))
        self.motor2_pin2 = PWM(Pin(19, Pin.OUT))
        self.motor2_pin1 = PWM(Pin(20, Pin.OUT))
        # Set the frequency of the PWM signal
        self.motor1_pin1.freq(100000)
        self.motor1_pin2.freq(100000)
        self.motor2_pin1.freq(100000)
        self.motor2_pin2.freq(100000)

        self.motor1_hall_1 = Pin(4, Pin.IN)
        self.motor1_hall_2 = Pin(5, Pin.IN)
        self.motor2_hall_1 = Pin(22, Pin.IN)
        self.motor2_hall_2 = Pin(21, Pin.IN)

        self.pi1 = PI(self.motor1_hall_1, self.motor1_hall_2)
        self.pi2 = PI(self.motor2_hall_1, self.motor2_hall_2)

        self.last_time = 0
        self.dt = dt

    def motor1_write(self, duty_cycle, direction):
        """
        Set the duty cycle and direction of motor 1.

        Args:
            duty_cycle (int): The duty cycle value between 0 and 65535.
            direction (bool): The direction of rotation. True for forward, False for backward.

        """
        if direction:
            self.motor1_pin1.duty_u16(duty_cycle)
            self.motor1_pin2.duty_u16(0)
        else:
            self.motor1_pin1.duty_u16(0)
            self.motor1_pin2.duty_u16(duty_cycle)

    def motor2_write(self, duty_cycle, direction):
        """
        Set the duty cycle and direction of motor 2.

        Args:
            duty_cycle (int): The duty cycle value between 0 and 65535.
            direction (bool): The direction of rotation. True for forward, False for backward.

        """
        if direction:
            self.motor2_pin1.duty_u16(duty_cycle)
            self.motor2_pin2.duty_u16(0)
        else:
            self.motor2_pin1.duty_u16(0)
            self.motor2_pin2.duty_u16(duty_cycle)

    async def tick(self):
        """
        Perform a control update.

        This method is called periodically to update the motor control based on the received message.

        """
        cur_time = ticks_ms()
        if self.get_message():

            x_linear, z_angular = self.get_message().split(",")
            x_linear = float(x_linear)
            z_angular = float(z_angular)

            self.pi1.set_ref_speed(x_linear + z_angular)
            self.pi2.set_ref_speed(x_linear - z_angular)

            print(self.pi1.ref_speed, self.pi2.ref_speed)

        if cur_time - self.last_time > self.dt:
            self.pi1.update()
            self.pi2.update()
            motor1_speed = self.pi1.pi()
            motor2_speed = self.pi2.pi()
            self.motor1_write(int(abs(motor1_speed)), motor1_speed > 0)
            self.motor2_write(int(abs(motor2_speed)), motor2_speed > 0)
        self.set_message(None)
        
    
class PI:
    """
    Proportional-Integral (PI) controller class for controlling the speed of a two-wheel robot.
    
    Args:
        hall1_pin (Pin): The pin connected to the first hall sensor.
        hall2_pin (Pin): The pin connected to the second hall sensor.
        prop (int, optional): The proportional gain of the controller. Defaults to 10000.
        integ (int, optional): The integral gain of the controller. Defaults to 1000.
    
    Attributes:
        position_old (int): The previous position of the robot.
        position (int): The current position of the robot.
        time_old (int): The previous time at which the position was updated.
        speed (float): The current speed of the robot.
        ref_speed (float): The reference speed set for the robot.
        prop (int): The proportional gain of the controller.
        integ (int): The integral gain of the controller.
        integ_sum (float): The sum of the integral errors.
        error (float): The current error between the reference speed and the actual speed.
        prev_error (float): The previous error between the reference speed and the actual speed.
    """
    
    def __init__(self, hall1_pin, hall2_pin, prop=10000, integ=1000) -> None:
        self.position_old = 0
        self.position = 0
        self.time_old = 0
        self.speed = 0
        self.ref_speed = 0
        self.prop = prop
        self.integ = integ
        self.integ_sum = 0
        self.error = 0
        self.prev_error = 0
        
        def interrupt_handler(hall1_val):
            """
            Interrupt handler function for updating the position of the robot based on the hall sensor readings.
            
            Args:
                hall1_val (int): The value of the first hall sensor.
            """
            if hall1_val == 1:
                if hall2_pin.value() == 0:
                    self.position += 1
                else:
                    self.position -= 1
            else:
                if hall2_pin.value() == 1:
                    self.position += 1
                else:
                    self.position -= 1
                    
        hall1_pin.irq(interrupt_handler, Pin.IRQ_RISING | Pin.IRQ_FALLING)
        hall2_pin.irq(interrupt_handler, Pin.IRQ_RISING | Pin.IRQ_FALLING)
        
        
    def update(self):
        """
        Update the speed of the robot based on the current position and time.
        
        Returns:
            float: The current speed of the robot.
        """
        time = ticks_ms()
        self.speed = (self.position - self.position_old) / 26 / (time - self.time_old)
        self.position_old = self.position
        self.time_old = time
        
        return self.speed
    
    def set_ref_speed(self, ref_speed):
        """
        Set the reference speed for the robot.
        
        Args:
            ref_speed (float): The reference speed to be set.
        """
        self.ref_speed = ref_speed
        self.integ_sum = 0
    
    def pi(self):
        """
        Calculate the control signal for the PI controller.
        
        Returns:
            float: The control signal calculated by the PI controller.
        """
        self.prev_error = self.error
        self.error = self.ref_speed - self.speed
        
        if self.error * self.prev_error < 0:
            self.integ_sum = 0
        
        return self.prop * self.error + self.integ * self.integ_sum