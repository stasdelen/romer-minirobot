from ..urtps.node import Node
        
class Echo(Node):
    def __init__(self, name):
        super().__init__(name)
    
    async def tick(self):
        if self.get_message():
            print(f'Message received. {self.get_message()}')
        self.set_message(None)