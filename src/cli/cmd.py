from os import getcwd
cmd_dict = {}

def cmd(arg):
    def wrapper(func):
        def new_func(*args):
            func(*args)
        cmd_dict[arg] = new_func
        return new_func
    return wrapper

@cmd("pwd")
def pwd(args, env, input, output):
    output.write(getcwd() + "\n")
    
def map_cmd(cmd, env, input, output):
    cmd_dict[cmd.name](cmd.args, env, input, output)