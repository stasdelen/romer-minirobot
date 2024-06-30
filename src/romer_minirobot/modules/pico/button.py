from machine import Pin

from ...urtps import EventPubNode

class Button(EventPubNode):
    """
    Represents a button component that can be used to detect button presses.

    Args:
        pin_number (int): The pin number to which the button is connected.
        mode (str): The mode of the button. Can be 'pull_up' or 'pull_down'.
        invert (bool): Whether to invert the button's logic level.
        poll_sec (float): The time interval (in seconds) between button state checks.
        name (str, optional): The name of the button. Defaults to 'button'.

    Example:
        button = Button(5, 'pull_up', False, 0.1, 'my_button')
        # Creates a button object connected to pin 5, with pull-up mode,
        # non-inverted logic level, and a polling interval of 0.1 seconds.
        # The button is named 'my_button'.
    """

    def __init__(self, pin_number, mode, invert, poll_sec, name='button') -> None:
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
        """
        Checks the state of the button and publishes the button state if it has changed.
        """
        pin_val = self.pin.value()
        if pin_val != self.last_value:
            self.last_value = not self.last_value
            self.set_message(str(self.last_value == self.invert))
    