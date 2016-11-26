import ply.yacc as yacc
import ply.lex as lex
from string import Template
from abc import abstractmethod
import functools

tokens = ('QUOTE_STR', 'STR')

t_QUOTE_STR    = r'\'[^\']*\''
t_STR          = r'[^\']+'
t_ignore = " \t"

class PrepReplace:
    def __init__(self, s):
        self.str = s
        
    @abstractmethod
    def substitute(self, env):
        pass

class QuoteStrReplace(PrepReplace):
    def __init__(self, s):
        super(QuoteStrReplace, self).__init__(s)
    def substitute(self, env):
        return self.str
    
class StrReplace(PrepReplace):
    def __init__(self, s):
        super(StrReplace, self).__init__(s)
    def substitute(self, env):
        templ = Template(self.str)
        return templ.substitute(env.get_vars())

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def p_cmd(t):
    '''
    cmd : cmd chunk 
    '''
    t[0] = t[1] + [t[2]]
    
def p_chunk_empty(t):
    '''
    cmd : 
    '''
    t[0] = []

def p_chunk_qoute(t):
    '''
    chunk : QUOTE_STR
    '''
    t[0] = QuoteStrReplace(t[1])
    
def p_fuck1(t):
    '''
    chunk : STR
    '''
    t[0] = StrReplace(t[1])


def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()
lexer = lex.lex()
    
def substitute(s, env):
    return functools.reduce(lambda x, y : x + y.substitute(env), parser.parse(s, lexer=lexer), "")
    
    
