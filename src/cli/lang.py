class Pipe:
    def __init__(self, cmd, nxt):
        self.cmd = cmd
        self.nxt = nxt
  
class Cmd:
    def __init__(self, name, env_assign, args):
        self.name = name
        self.args = args
        self.env_assign = env_assign
    
class EnvAssigment:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class EnvSet:
    def __init__(self):
        self.items = []
        
    def add_assign(self, assign):
        self.items.append(assign)
        
    def get_items(self):
        return self.items
    
