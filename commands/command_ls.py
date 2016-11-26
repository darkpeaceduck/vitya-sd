import os
def command_ls(shell_status, args):
    dir = args[0]
    for item in os.listdir(dir):
        shell_status.output_stream += item + "\n"
