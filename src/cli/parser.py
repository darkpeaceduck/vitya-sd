

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables -- all in one file.
# -----------------------------------------------------------------------------
'''
tokens = (
    'QUOTE','DOUBLE_QUOTE', 'EQUALS'
    'PIPE', 'VAR_START', 'NAME'
    )
'''
'''
'VAR_START', 'EQUALS'

'''
tokens = ('PIPE', 'NAME', 'EQUALS')

t_EQUALS       = r'='
t_PIPE         = r'\|'
t_NAME         = r'[a-zA-Z_][a-zA-Z0-9_]*'

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules
precedence = (('left', 'PIPE'),)
'''
precedence = (
    ('left', 'PIPE')
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )
'''

class Pipe:
    def __init__(self, cmd, nxt):
        self.cmd = cmd
        self.nxt = nxt
    def __str__(self):
        return "(" + str(self.cmd) + " -> " + str(self.nxt) + ")"

class EnvAssigment:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        return "(" + self.name + "=" + self.value + ")"
    
class Cmd:
    def __init__(self, name, env, args):
        self.name = name
        self.args = args
        self.env = env
    def __str__(self):
        ss = ""
        for huy in self.env:
            ss += str(huy) 
        return self.name + " args : " + str(self.args) + " env : " + ss
    
# dictionary of names

def p_pipe(t):
    '''
    cmd : cmd PIPE cmd 
    '''
    t[0] = Pipe(t[1], t[3])
    
def p_cmd(t):
    '''
    cmd : env NAME args
    '''
    t[0] = Cmd(t[2], t[1], t[3])

    
def p_args(t):
    '''
    args : NAME args
    '''
    t[0] = [t[1]] + (t[2])

def p_arg(t):
    '''
    args : 
    '''
    t[0] = []

def p_env0(t):
    '''
    env : 
    '''
    t[0] = []


def p_env(t):
    '''
    env : env envset
    '''
    t[0] = t[1] + [t[2]]
    
def p_env_set(t):
    '''
    envset : NAME EQUALS NAME
    '''
    t[0] = EnvAssigment(t[1], t[3])
'''
names = { }

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]
    


def p_statement_expr(t):
    'statement : expression'
    print(t[1])

def p_expression_binop(t):
    expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0
'''
def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('> ')   # Use raw_input on Python 2
    except EOFError:
        break
    print(parser.parse(s))