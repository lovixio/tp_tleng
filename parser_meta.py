import ply.lex as lex
from ply.lex import LexError
import ply.yacc as yacc

# Tokens

tokens = (
    'CARACTERES', 
    'LCORCHETE' , 'RCORCHETE',
    'COMILLA', 'ESPACIO' , 'newline',
    'MENOS', 'NUM', 'PUNTO', 'CASILLA', 'PIEZA' , 'SLASH'
)

t_LCORCHETE = r'\['
t_RCORCHETE = r'\]'

t_CARACTERES = r'[^\s\[\]\"\d+\.\-a-hPNBRQK\/]+'
t_COMILLA = r'\"'
t_ESPACIO = r'\ '
t_MENOS = r'-'
t_NUM = r'\d+'
t_PUNTO = r'\.'
t_PIEZA = r'[P|N|B|R|Q|K]'
t_CASILLA = r'[a-h]'
t_SLASH = r'\/'



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
                 | CARACTERES
                 | CASILLA
                 | PIEZA
                 | SLASH'''

def p_partida(t): 
    'partida : jugada sigjugada'

def p_jugada(t):
    '''jugada : NUM PUNTO ESPACIO movimiento movimiento'''
    print("Jugada numero", t[1], "se jugo:", t[4], t[5])
            
def p_movimiento(t):
    ''' movimiento : CASILLA NUM ESPACIO
                   | PIEZA CASILLA NUM ESPACIO'''
    
    t[0] = t[1] + t[2]
    numCasilla = t[2]
    if t[3]!=" " :
        t[0] += t[3]
        numCasilla = t[3]
    
    numCasilla = int(numCasilla)
    if numCasilla == 0 or numCasilla >= 9:
        p_error(t)

def p_sigjugada(t):
    '''sigjugada : jugada sigjugada 
                 | score'''

def p_score_simplificado(t):
    '''score : NUM MENOS NUM'''
    if int(t[1]) > 1 or int(t[3]) > 1:
        p_error(t)

def p_score_fraccion(t):
    '''score : NUM SLASH NUM MENOS NUM SLASH NUM'''
    if not (int(t[1]) == 1 and int(t[3]) == 2 and int(t[5]) == 1 and int(t[7]) == 2) :
        p_error(t)


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

