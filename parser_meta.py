import ply.lex as lex
from ply.lex import LexError
import ply.yacc as yacc

# Tokens

tokens = (
    'CARACTERES', 
    'LCORCHETE' , 'RCORCHETE',
     "COMILLA", "ESPACIO" , "newline"
)

t_LCORCHETE = r'\['
t_RCORCHETE = r'\]'

t_CARACTERES = r'[^\s\[\]\"]+'
t_COMILLA = r'\"'
t_ESPACIO = r'\ '




def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    raise LexError("Illegal character '%s'" % t.value)
    t.lexer.skip(1)
 
# Build the lexer
lexer = lex.lex()

# Parsing rules
precedence = ()
  


def p_statement_MetaData(t):
    '''statement : expression'''

def p_expression_renglonMetaData(t):
    '''expression : LCORCHETE CARACTERES ESPACIO COMILLA CARACTERES COMILLA RCORCHETE
                  | LCORCHETE CARACTERES ESPACIO COMILLA CARACTERES COMILLA RCORCHETE newline expression'''
    print(t[1])

def p_error(t):
    print("Syntax error at ", t)

parser = yacc.yacc()

"""while True:
    try:
        s = ""
           # Use raw_input on Python 2
    except EOFError:
        break"""

s = '''[prueba "loca"]
[Nzscf5qWgtg~NVX "56B~n~nQIeAhy"]
[gvk7dXkliRpR "2LAkQJGhz81"]
[~NFS5lBHW4Mm~NmJsP "e4ZhVulzl"]
[yZ1PSI4r78KP "XwWzscEtUqkAu~nNt7Hq5"]

[GArzOdNa~nITcsbFO9ES "WUodxeqxI"]'''

def customParse(s):
    for cadena in s.split('\n'):
        if cadena != '':
            parser.parse(cadena)

customParse(s)
