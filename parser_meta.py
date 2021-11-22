
import ply.lex as lex
from ply.lex import LexError, StringTypes
import ply.yacc as yacc
import os
os.system('color') # Sirve para que se vean los colorsitos del test en windows
from funciones_auxiliares import *

# Tokens

tokens = (
    'CARACTERES', 
    'LCORCHETE' , 'RCORCHETE',
    'COMILLA', 'ESPACIO' , 'newline',
    'MENOS', 'NUM', 'PUNTO', 'CASILLA', 'PIEZA' , 'SLASH',
    'MAS', 'PREGUNTA', 'EXCLAMACION', 'EQUIS'
)

t_LCORCHETE = r'\['
t_RCORCHETE = r'\]'

#CARACTERES se refiere a todos los caracteres que solo se usen para la metaData y comentarios
t_CARACTERES = r'[^\s\[\]\"\d+\.\-a-hPNBRQK\/\+\?!x]+' 
t_COMILLA = r'\"'
t_ESPACIO = r'\ '
t_MENOS = r'-'
t_NUM = r'\d+'
t_PUNTO = r'\.'
t_PIEZA = r'[P|N|B|R|Q|K]'
t_CASILLA = r'[a-h]'
t_SLASH = r'\/'
t_MAS = r'\+'
t_PREGUNTA = r'\?'
t_EXCLAMACION = r'!'
t_EQUIS = r'x'



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

def p_file_InicioArchivo(t):
    '''file : LCORCHETE metadata RCORCHETE metadataSegment'''

#El segmento de metadata hace recursión hasta terminar en una partida
def p_metadataSegment_MetaData(t):
    '''metadataSegment : LCORCHETE metadata RCORCHETE metadataSegment
                       | partida'''

def p_metadata_renglonMetaData(t):
    '''metadata : string ESPACIO COMILLA string COMILLA'''
    print(t[1] + ' ' + '"' + t[4] + '"')

#Para parsear las cosas escritas usamos una recursion sobre los distintos tokens que se pueden encontrar
def p_string_escritoEnLaMetaData(t):
    '''string : contenido string
              | contenido Empty'''
    t[0] = t[1] + t[2]

def p_contenido_delString(t):
    '''contenido : NUM
                 | MENOS
                 | CARACTERES
                 | CASILLA
                 | PIEZA
                 | SLASH
                 | MAS
                 | PREGUNTA
                 | EXCLAMACION
                 | EQUIS'''
    t[0] = t[1]

#una partida empieza con una jugada y una siguiente jugada (la cual puede ser el score, indicando el final de la partida)
def p_partida(t): 
    '''partida : jugada sigjugada'''
    if not (t[1] == 1 and (t[2] == 2 or t[2] == 0)):
        p_error(t)

def p_jugada(t):
    '''jugada : NUM PUNTO ESPACIO movimiento movimiento '''
    print("Jugada numero", t[1], "se jugo:", t[4], t[5])
    
    t[0] = int(t[1])
    if t[0] == 0:
        p_error(t)

def p_movimiento(t):
    ''' movimiento : pieza casillas NUM mate calidad ESPACIO '''
    t[0] = t[1] + t[2] + t[3]
    
    numCasilla = int(t[3])
    if numCasilla == 0 or numCasilla >= 9:
        p_error(t)

def p_pieza(t):
    ''' pieza : PIEZA
              | Empty'''
    t[0] = t[1]

def p_casillas_CapturaDestino(t):
    '''casillas : CASILLA'''
    t[0] = t[1]

#aca hay un bug que no sabe diferenciar estos dos casos y piensa que el segundo movimiento en el .txt está mal    
def p_casillas_OrigenCapturaDestino(t):
    '''casillas : origen captura CASILLA'''
    t[0] = t[1] + t[2] + t[3]

def p_origen(t):
    ''' origen : CASILLA
               | NUM
               | Empty'''
    t[0] = t[1]
        
def p_captura(t):
    ''' captura : EQUIS
                | Empty'''
    t[0] = t[1]

def p_calidad_deUnMovimiento(t):
        ''' calidad : EXCLAMACION
                    | PREGUNTA
                    | Empty'''

def p_mate(t):
    '''mate : MAS
            | MAS MAS
            | Empty '''

def p_sigjugada(t):
    '''sigjugada : jugada sigjugada 
                 | score'''
    if t[1]!=0 and not (t[2] == t[1]+1 or t[2] == 0):
        p_error(t)
    #pasamos el número de la jugada definida ahora como número de la siguiente jugada anterior para comparar con la anterior
    t[0] = t[1]
    
def p_score_simplificado(t):
    '''score : NUM MENOS NUM'''
    t[0] = 0
    if int(t[1]) > 1 or int(t[3]) > 1:
        p_error(t)

def p_score_fraccion(t):
    '''score : NUM SLASH NUM MENOS NUM SLASH NUM'''
    t[0] = 0
    if not (int(t[1]) == 1 and int(t[3]) == 2 and int(t[5]) == 1 and int(t[7]) == 2) :
        p_error(t)

def p_Empty(t):
    ''' Empty :'''
    t[0] = ''   # El atributo de empty siempre es vacio('') eso nos evita problemas despues
    pass

def p_error(t):
    raise RejectStringError(t)

parser = yacc.yacc()

"""while 1:
    try:
        s = raw_input('Partida > ')
    except EOFError:
        break
    if not s:
        continue
    parser.parse(s)"""



# Cada test es una tupla (string a correr, valor esperado (puede ser 1 o -1))
testsToRun = []

# Test 1: muchas lineas de metadata
testsToRun.append(('''[prueba "loca"]
[Nzscf5qWgtg~NVX "56B~n~nQIeAhy"]
[gvk7dXkliRpR "2LAkQJGhz81"]
[~NFS5lBHW4Mm~NmJsP "e4ZhVulzl"]

[GArzOdNa~nITcsbFO9ES "WUodxeqxI"]

1. a4 e3 1-0''', 1))

# Test 2: Metadata sin espacio ni comillas de apertura falla
testsToRun.append(('''[prueba "loca"]
[pruebaloca"]

1. a4 e3 1-0''', -1))

# Test 3: mataData con corchetes sin cerrar falla
testsToRun.append(('''[prueba "loca"
pruebaloca"]

1. a4 e3 1-0''', -1))

# Test 4: Empate
testsToRun.append(('''[prueba "loca"]
1. a4 e3 1/2-1/2''', 1))

# Test 5: multiples jugadas con jaque, mate y modificadores
testsToRun.append(('''[prueba "loca"]
1. a4! e3+? 2. a4 h3++ 3. a5 b2 0-1''', 1))

# Test 6: movimientos con capturas y con origenes
testsToRun.append(('''[prueba "loca"]
1. a4! Bxg5 2. Ka4 h3++ 3. Nbd7 N2d4 0-1''', 1))

# Se puede descomentar una linea en runTest para que los test sean los paths
# a los txt y no la cadena directa a parsear
runTests(testsToRun, parser.parse)



# Notas sobre las capturas:
#
#   Algunas jugadas tienen PIEZA NUM ... y otras PIEZA CASILLA ...
#   Un movimiento no puede empezar con 'x'
#
