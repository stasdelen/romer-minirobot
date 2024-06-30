from machine import Pin

from ...urtps import EventPubNode

class Button(EventPubNode):

    def __init__(self, pin_number, mode, invert, poll_sec, name = 'button') -> None:
        super().__init__(name, 'publishing')
        self.pin = Pin(pin_number, Pin.IN)
        if mode:
            if mode == 'pull_up':
                self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
            elif mode == 'pull_down':
                self.pin = Pin(pin_number, Pin.IN, Pin.PULL_DOWN)
        self.invert = not invert
        self.poll_sec = poll_sec
        self.last_value = self.pin.value()
        
    async def tick(self):
        # await asyncio.sleep(self.poll_sec)
        pin_val = self.pin.value()
        if pin_val != self.last_value:
            self.last_value = not self.last_value
            # print(str(self.last_value == self.invert))
            self.set_message(str(self.last_value == self.invert))
    