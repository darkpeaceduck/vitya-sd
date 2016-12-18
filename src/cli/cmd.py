from os import getcwd
import sys
import subprocess


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
    if len(args) > 0:
        fname = args[0]
        with open(fname, 'r') as f:
            output.write(f.read())
    else:
        output.write(input.read())
        
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
    
def map_cmd(cmd, env, input, output, pseudo):
    try:
        cmd_dict[cmd.name](cmd.args, env, input, output)
    except KeyError:
        subproc = None
        hid_output = None
        if pseudo:
            subproc = subprocess.Popen([cmd.name] + cmd.args, env=env.get_vars(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            hid_output = subproc.communicate(str.encode(input.read()))[0]
        else:
            subproc = subprocess.Popen([cmd.name] + cmd.args, env=env.get_vars(), stdin=input, stdout=subprocess.PIPE)
            hid_output = subproc.communicate()[0]
        output.write(hid_output.decode("utf-8"))
