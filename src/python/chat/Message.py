from queue import Queue
MESSAGE_MAX_LENGTH = 4096

class Message:
    def __init__(self, str_data=None, byte_data=None):
        if str_data:
            self.bdata = str_data.encode()
            self.sdata = str_data
        else:
            self.bdata = byte_data
            self.sdata = byte_data.decode()
        
    def __str__(self):
        return self.sdata
    
    def get_bytes(self):
        return self.bdata
    
class MessageQueueProcessor:
    def __init__(self):
        self.msg_q = Queue()
    def get_msg(self):
        return self.msg_q.get_nowait()
    def push_msg(self, msg):
        self.msg_q.put_nowait(msg)