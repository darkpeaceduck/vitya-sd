import os
def command_cd(shell_status, args):
    chdir = args[0]
    os.chdir(chdir)
