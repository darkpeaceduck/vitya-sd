from os import getcwd
import sys
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
    
@cmd("cat")
def cat(args, env, input, output):
    fname = args[0]
    with open(fname, 'r') as f:
        output.write(f.read())
        
@cmd("echo")
def echo(args, env, input, output):
    for arg in args:
        output.write(arg)
    output.write("\n")
    
@cmd("wc")
def wc(args, env, input, output):
    total_len = 0
    total_line = 0
    total_words = 0
    for line in input:
        total_len += len(line)
        total_line += 1
        total_words += len(line.split())
    output.write("{0} {1} {2}\n".format(total_line, total_words, total_len))
    
@cmd("exit")
def exit(args, env, input, output):
    sys.exit(0)
    
def map_cmd(cmd, env, input, output):
    cmd_dict[cmd.name](cmd.args, env, input, output)