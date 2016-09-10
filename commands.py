from os import getcwd


def command_exit(shell_status, _):
    shell_status.is_run = False


def command_pipe(shell_status):
    shell_status.input_stream = shell_status.output_stream
    shell_status.output_stream = ""


def command_echo(shell_status, args):
    shell_status.input_stream = ""
    shell_status.output_stream = ""
    for arg in args:
        shell_status.output_stream = shell_status.output_stream + str(arg) + " "


def command_assign(shell_status, args):
    shell_status.environment[args[0]] = args[1]


def command_cat(shell_status, args):
    shell_status.input_stream = ""
    shell_status.output_stream = ""

    for arg in args:
        with open(arg) as file:
            shell_status.output_stream += file.read()


def command_wc(shell_status, _):
    lines_num = len(shell_status.input_stream.split('\n'))
    words_num = len(shell_status.input_stream.split(' '))
    bytes_num = len(shell_status.input_stream) + 1
    shell_status.input_stream = ""
    shell_status.output_stream = "{} {} {}".format(lines_num, words_num, bytes_num)


def command_pwd(shell_status, _):
    shell_status.input_stream = ""
    shell_status.output_stream = getcwd()

command_by_name = {
    "exit":   command_exit,
    "|":      command_pipe,
    "echo":   command_echo,
    "assign": command_assign,
    "cat":    command_cat,
    "wc":     command_wc,
    "pwd":    command_pwd
}