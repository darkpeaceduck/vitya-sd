from os import getcwd
import sys
import subprocess
import argparse
import re


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
        
@cmd("grep")
def grep(args, enbv, input, output):    
    parser = argparse.ArgumentParser()
    parser.add_argument('-A', type=int, action='store')
    parser.add_argument('-w', action='store_true')
    parser.add_argument('-i', action='store_true')
    parser.add_argument('re', action='store')
    parser.add_argument('file', action='store', nargs="?")
    args = parser.parse_args(args)
    
    reg = args.re
    if args.w:
        reg = "{0}{1}{0}".format("\\b", reg)
        
    compile_flags = []
    if args.i:
        compile_flags.append(re.IGNORECASE)
        
    rr = re.compile(reg, *compile_flags)
        
    stream = input
    need_close = False
    if args.file:
        stream = open(args.file)
        need_close = True 
    
    visible_line_inc = 1
    if args.A:
        visible_line_inc += args.A
        
    visible_line_counter = 0
    for line in stream:
        if rr.search(line):
            visible_line_counter += visible_line_inc
        if visible_line_counter > 0:
            output.write(line)
            visible_line_counter -= 1
            
    if need_close:
        stream.close()
    
    
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
