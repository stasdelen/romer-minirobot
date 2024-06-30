import random
import asyncio
from ..urtps.node import Node

class RandomNumberGenerator(Node):
    def __init__(self, delta_time = 1):
        super().__init__('RandomNumberGenerator')
        self.random_number = 0
        self.delta_time = delta_time
        
    async def tick(self):
        self.set_message(None)
        await asyncio.sleep(self.delta_time)
        self.random_number = random.randint(0, 100)
        self.set_message(self.random_number)