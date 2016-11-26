#from cli.parser import parse
from cli.env_preprocessor import substitute
from cli.parser import parse


while True:
    try:
        s = input('> ')   # Use raw_input on Python 2
        print(parse(substitute(s)))
    except EOFError:
        break