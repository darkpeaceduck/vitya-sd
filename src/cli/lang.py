class Pipe:
    def __init__(self, cmd, nxt):
        self.cmd = cmd
        self.nxt = nxt
    def __str__(self):
        return "(" + str(self.cmd) + " -> " + str(self.nxt) + ")"

  
class Cmd:
    def __init__(self, name, env_assign, args):
        self.name = name
        self.args = args
        self.env_assign = env_assign
    def __str__(self):
        ss = ""
        for huy in self.env_assign:
            ss += str(huy) 
        return self.name + " args : " + str(self.args) + " env : " + ss
    
class EnvAssigment:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        return "(" + self.name + "=" + self.value + ")"