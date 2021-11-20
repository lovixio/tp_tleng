import ply.lex as lex
from ply.lex import LexError
import ply.yacc as yacc

# Tokens

tokens = (
    'CARACTERES', 
    'LCORCHETE' , 'RCORCHETE',
    'COMILLA', 'ESPACIO' , 'newline',
    'MENOS', 'NUM', 'PUNTO'
)

t_LCORCHETE = r'\['
t_RCORCHETE = r'\]'

t_CARACTERES = r'[^\s\[\]\"\d+\.\-]+'
t_COMILLA = r'\"'
t_ESPACIO = r'\ '
t_MENOS = r'-'
t_NUM = r'\d+'
t_PUNTO = r'\.'




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
numeroDeJugada = 1
  

def p_file_InicioArchivo(t):
    'file : LCORCHETE metadata RCORCHETE metadataSegment'

def p_metadataSegment_MetaData(t):
    '''metadataSegment : LCORCHETE metadata RCORCHETE metadataSegment
                       | partida'''

def p_metadata_renglonMetaData(t):
    '''metadata : string ESPACIO COMILLA string COMILLA'''
    print(t[5])

def p_string_escritoEnLaMetaData(t):
    '''string : contenido string
              | contenido'''
    t[0] = t[1]

def p_contenido_delString(t):
    '''contenido : NUM
                 | MENOS
                 | CARACTERES'''

def p_partida(t): 
    'partida : jugada sigjugada'

def p_jugada(t):
    'jugada : NUM PUNTO ESPACIO'
    
def p_sigjugada(t):
    '''sigjugada : jugada sigjugada 
                 | scoresimplificado'''

def p_scoresimplificado(t):
    'scoresimplificado : NUM MENOS NUM'

def p_error(t):
    print("Syntax error at", t)

parser = yacc.yacc()

"""while True:
    try:
        s = ""
           # Use raw_input on Python 2
    except EOFError:
        break"""

s1 = '''[prueba "loca"]
[Nzscf5qWgtg~NVX "56B~n~nQIeAhy"]
[gvk7dXkliRpR "2LAkQJGhz81"]
[~NFS5lBHW4Mm~NmJsP "e4ZhVulzl"]
[yZ1PSI4r78KP "XwWzscEtUqkAu~nNt7Hq5"]

[GArzOdNa~nITcsbFO9ES "WUodxeqxI"]'''

s2 = '''[prueba "loca"]
[Nzscf5qWgtg~NVX "56B~n~nQIeAhy"]
[gvk7dXkliRpR "2LAkQJGhz81"]
[~NFS5lBHW4Mm~NmJsP "e4ZhVulzl"]
[yZ1PSI4r78KP "XwWzscEtUqkAu~nNt7Hq5"]

[GArzOdNa~nITcsbFO9ES "WUodxeqxI"]

1.2.2-3'''

def customParse(s):
    for cadena in s.split('\n'):
        if cadena != '':
            parser.parse(cadena)


with open('testing_text.txt', 'r') as file:
    partidas = file.read()
#customParse(s1)
parser.parse(partidas)

