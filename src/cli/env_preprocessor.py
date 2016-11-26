
import ply.yacc as yacc
import ply.lex as lex
from string import Template
import os

tokens = ('QUOTE_STR', 'STR')

t_QUOTE_STR    = r'\'[^\']*\''
t_STR          = r'[^\']+'
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def p_cmd(t):
    '''
    cmd : cmd fuck 
    '''
    t[0] = t[1] + t[2]
    
def p_empty(t):
    '''
    cmd : 
    '''
    t[0] = ''

def p_fuck(t):
    '''
    fuck : QUOTE_STR
    '''
    t[0] = t[1]
    
def replace_env(s):
    o = Template(s)
    return o.substitute(os.environ)
    
def p_fuck1(t):
    '''
    fuck : STR
    '''
    t[0] = replace_env(t[1])


def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()
lexer = lex.lex()
    
def substitute(s):
    return parser.parse(s, lexer=lexer)
    
