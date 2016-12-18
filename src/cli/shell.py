from cli.preprocessor import substitute
from cli.parser import parse
from cli.env import Env
import cli.runtime
import sys


if __name__ == '__main__':
    env = Env()
    while True:
        try:
            s = input('> ')  
            ss = substitute(s, env)
            ll = parse(ss)
            ll.exec(env, sys.stdin, sys.stdout)
        except Exception as e:
            print ("Failed to complete")
            print(e)