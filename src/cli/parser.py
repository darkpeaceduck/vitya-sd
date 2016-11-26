import ply.yacc as yacc
import ply.lex as lex

tokens = ('PIPE', 'NAME', 'EQUALS', 'QUOTE_STR', 'VALUE_STR')

t_EQUALS       = r'='
t_PIPE         = r'\|'
t_NAME         = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_VALUE_STR    = r'[^\' =\|]+'
t_QUOTE_STR    = r'\'[^\']*\''
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

precedence = (('left', 'PIPE'),)

class Pipe:
    def __init__(self, cmd, nxt):
        self.cmd = cmd
        self.nxt = nxt
    def __str__(self):
        return "(" + str(self.cmd) + " -> " + str(self.nxt) + ")"

  
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
    
class EnvAssigment:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __str__(self):
        return "(" + self.name + "=" + self.value + ")"
    
    
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
    args : arg_str args
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
    envset : NAME EQUALS arg_str
    '''
    t[0] = EnvAssigment(t[1], t[3])
    
def p_quote_str(t):
    '''
    arg_str : QUOTE_STR
    '''
    t[0] = t[1][1:-1]
    
def p_str(t):
    '''
    arg_str : VALUE_STR 
            | NAME 
    '''
    t[0] = t[1]

    
    
def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()
lexer = lex.lex()

def parse(s):
    return parser.parse(s, lexer=lexer)