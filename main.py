from lexer import get_tokens
from splitter import get_commands
from performer import execute_commands


class ShellStatus:
    is_run = True
    environment = {}
    input_stream = ""
    output_stream = ""


while ShellStatus.is_run:
    command = input("Type your command: ")
    token_queue = get_tokens(command, ShellStatus.environment)
    command_queue = get_commands(token_queue)
    execute_commands(command_queue, ShellStatus)

    if ShellStatus.input_stream != '':
        print(ShellStatus.input_stream)
