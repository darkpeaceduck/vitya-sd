from chat.Message import MessageQueueProcessor
from threading import Event
from abc import abstractmethod
from chat.ConnectionManagers import AbstractConnectionManager

class AbstractBus(MessageQueueProcessor, AbstractConnectionManager):
    def __init__(self):
        MessageQueueProcessor.__init__(self)
        AbstractConnectionManager.__init__(self)

    @abstractmethod
    def on_sent(self, msg):
        pass
    
    @abstractmethod
    def on_receive_msg(self, msg):
        pass
        
    @abstractmethod
    def on_closed(self):
        pass
    
    @abstractmethod
    def on_connected(self):
        pass
    
class StateBus(AbstractBus):
    def __init__(self, connection_manager):
        AbstractBus.__init__(self)
        self.connection_manager = connection_manager
        self.connection_manager.addListener(self)
        self.state = {
            "connected" : None,
            "closed" : None,
        }
    
    def set_state(self, state, value):
        self.state[state] = value
        
    def clear_state(self, state):
        self.state[state] = None
        
    def get_state(self, state):
        return self.state[state]
    
    def on_sent(self, msg):
        self.push_msg(msg)

    def on_receive_msg(self, msg):
        self.push_msg(msg)
        
    def on_closed(self):
        self.set_state("closed", True)
        
    def on_connected(self, client):
        self.set_state("connected", client)
        
    def send(self, msg):
        self.connection_manager.send(msg)
    
    def connect(self, bind_address, address):
        self.connection_manager.connect(bind_address, address)
    
    def listen(self, bind_adress):
        self.connection_manager.listen(bind_adress)
    
    def close(self):
        self.connection_manager.close()