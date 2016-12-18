#shell language primitives" 

#cmd | nxt"
class Pipe:
    def __init__(self, cmd, nxt):
        self.cmd = cmd
        self.nxt = nxt
    def __eq__(self, other):
        return self.cmd == other.cmd and self.nxt == other.nxt 
  
#env_assing name args"
class Cmd:
    def __init__(self, name, env_assign, args):
        self.name = name
        self.args = args
        self.env_assign = env_assign
    def __eq__(self, other):
        return self.name == other.name and self.args == other.args and self.env_assign == other.env_assign 
    
#name=value"
class EnvAssigment:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __eq__(self, other):
        return self.name == other.name and self.value == other.value

#set of EnvAssigment items"
class EnvSet:
    def __init__(self):
        self.items = []
        
    def __eq__(self, other):
        return self.items == other.items
        
    def add_assign(self, assign):
        self.items.append(assign)
        
    def get_items(self):
        return self.items
    
