from ..urtps.node import Node
        
class Bool(Node):
    def __init__(self, name):
        super().__init__(name, 'subscribing')
        self.value = False
    
    def get(self):
        return self.value
    
    async def tick(self):
        self.value = self.get_message() == 'True'
    