from cli.preprocessor import substitute
from cli.parser import parse
from cli.env import Env


env = Env()
while True:
    try:
        s = input('> ')   # Use raw_input on Python 2
        print(parse(substitute(s, env)))
    except EOFError:
        break