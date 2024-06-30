import asyncio
from ..urtps.node import BlockingNode

# class Teller(BlockingNode):
    
#     # Static variable to keep track of the number of tellers
#     static_id = 0
    
#     def __init__(self, msg, name, delta_time = 1):
#         # If name is not provided, set it to a unique name
#         if not name:
#             name = f"Teller-{Teller.static_id}"
#         super().__init__(name)
#         Teller.static_id += 1
#         # Message to be sent
#         self.msg = msg
#         # Time interval between messages
#         self.delta_time = delta_time
        
#     async def tick(self):
#         self.set_message(None)  
#         await asyncio.sleep(self.delta_time)
#         self.set_message(self.msg)
        
class Teller(BlockingNode):
    static_id = 0
    
    def __init__(self, msg, delta_time, name = None) -> None:
        if not name:
            name = f"Teller-{Teller.static_id}"
        super().__init__(name, delta_time)
        Teller.static_id += 1
        self.set_message(msg)
        
    async def tick(self):
        return self.get_message()