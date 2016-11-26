from preprocessor import substitute
from parser import parse
from env import Env
import runtime
import sys


if __name__ == '__main__':
    env = Env()
    while True:
        try:
            s = input('> ')   
            ll = parse(substitute(s, env))
            ll.exec(env, sys.stdin, sys.stdout)
        except EOFError:
            break