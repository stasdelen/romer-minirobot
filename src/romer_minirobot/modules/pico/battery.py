from machine import Pin, ADC
from utime import ticks_ms

from ...urtps import Node

class Battery(Node):
    
    def __init__(self, battery_pin, delta_time,  name = 'battery', R1 = 100.0, R2 = 47.0) -> None:
        super().__init__(name, 'publishing')
        self.battery_adc = ADC(Pin(battery_pin))
        self.battery_percentage = 0
        self.ratio = (R1 + R2) / R2
        self.delta_time = delta_time
        self.last_time = ticks_ms()
        
    async def tick(self):
        self.set_message(None)
        time = ticks_ms()
        if time - self.last_time < self.delta_time:
            return
        self.last_time = time
        self.battery_percentage = self.battery_adc.read_u16() / 65535 * 3.3 * self.ratio
        self.set_message(self.battery_percentage)