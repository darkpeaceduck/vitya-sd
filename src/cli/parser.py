import ply.yacc as yacc
import ply.lex as lex
from cli.lang import Pipe, EnvAssigment, Cmd, EnvSet

tokens = ('PIPE', 'NAME', 'EQUALS', 'QUOTE_STR')

t_EQUALS       = r'='
t_PIPE         = r'\|'
t_NAME         = r'[a-zA-Z0-9_\-\.\\\/]+'
t_QUOTE_STR    = r'(\'[^\']*\')|(\"[^\"]*\")'
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

precedence = (('left', 'PIPE'),)


def p_full(t):
    '''
    full : cmd
    '''
    t[0] = t[1]
    
def p_full_env(t):
    '''
    full : env
    '''
    t[0] = t[1]
    
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

def p_arga_empty(t):
    '''
    args : 
    '''
    t[0] = []

def p_env_empty(t):
    '''
    env : 
    '''
    t[0] = EnvSet()


def p_env_enset(t):
    '''
    env : env envset
    '''
    t[0] = t[1]
    t[0].add_assign(t[2])
    
def p_envset(t):
    '''
    envset : NAME EQUALS arg_str
    '''
    t[0] = EnvAssigment(t[1], t[3])
    
def p_arg_str_quote(t):
    '''
    arg_str : QUOTE_STR 
    '''
    t[0] = t[1][1:-1]
    
def p_arg_str_value(t):
    '''
    arg_str : NAME
    '''
    t[0] = t[1]

    
def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()
lexer = lex.lex()

def parse(s):
    return parser.parse(s, lexer=lexer)