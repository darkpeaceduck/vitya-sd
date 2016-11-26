from lang import Cmd, Pipe, EnvAssigment
import copy
from cmd import map_cmd
from io import StringIO

def exec_method(cls):
    def exec_method_gen(func):
        def wrapped(*args):
            func(*args)
        cls.exec = wrapped
        return wrapped
    return exec_method_gen


@exec_method(Pipe)
def pipe_exec(self, env, input, output):
    pseudo_io = StringIO()
    self.cmd.exec(env, input, pseudo_io)
    pseudo_io.seek(0)
    self.nxt.exec(env, pseudo_io, output)

@exec_method(Cmd)
def cmd_exec(self, env, input, output):
    local_env = copy.copy(env)
    for assign in self.env_assign:
        assign.exec(local_env)
    map_cmd(self, local_env, input, output)

@exec_method(EnvAssigment)
def assigment_exec(self, env):
    env.add_vars({self.name : self.value})