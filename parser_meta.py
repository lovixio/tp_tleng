import ply.lex as lex
from ply.lex import LexError, StringTypes, LexToken
import ply.yacc as yacc
from funciones_auxiliares import *
import re

# Tokens
tokens = (
    'CARACTERES', 
    'LCORCHETE' , 'RCORCHETE',
    'COMILLA', 'ESPACIO' , 'newline',
    'MENOS', 'NUM', 'PUNTO', 'FILALETRA', 'PIEZA' , 'SLASH',
    'MAS', 'PREGUNTA', 'EXCLAMACION', 'EQUIS', 'O',
    'LPAREN', 'RPAREN', 'LLLAVE', 'RLLAVE'
)

t_LCORCHETE = r'\['         
t_RCORCHETE = r'\]'         

#CARACTERES se refiere a todos los caracteres que solo se usen para la metaData y comentarios
t_CARACTERES = r'[^\s\[\]\"\d+\.\-a-hPNBRQK\/\+\?!xO\(\)\{\}]+' 
t_COMILLA = r'\"'           
t_ESPACIO = r'\ '           
t_MENOS = r'-'              
t_NUM = r'\d+'              
t_PUNTO = r'\.'             
t_PIEZA = r'[P|N|B|R|Q|K]'  
t_FILALETRA = r'[a-h]'      
t_SLASH = r'\/'             
t_MAS = r'\+'               
t_PREGUNTA = r'\?'          
t_EXCLAMACION = r'!'        
t_EQUIS = r'x'              
t_O = r'O'                  
t_LPAREN = r'\('            
t_RPAREN = r'\)'            
t_LLLAVE = r'\{'            
t_RLLAVE = r'\}'            

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    raise LexError("Illegal character '%s'" % t.value)
    t.lexer.skip(1)
 
# Build the lexer
lexer = lex.lex()

# Clases para los atributos
class Comentario:
    def __init__(self, nivel, maxNivel, jugada=-1):
        self.nivel = nivel
        self.nivelMaxSinCaptura = maxNivel
        self.jugada = jugada

class Seguimiento:
    def __init__(self, captura):
        self.tieneCaptura = captura

class Jugada: 
    def __init__(self, numJugada, maxNivel):
        self.numeroJugada = int(numJugada)
        self.nivelMaxSinCaptura = int(maxNivel)

class MaxLvlContainer:
    def __init__(self, maxNivel):
        self.nivelMaxSinCaptura = int(maxNivel)

class Casillas:
    def __init__(self, numeroDeFila):   
        self.numeroDeFila = int(numeroDeFila)

class DescripcionDeError:
    def __init__(self, value, t):
        self.value = value
        self.type = t

# Parsing rules
precedence = ()

# Regla principal de la gramatica
def p_s(t):
    '''s : file'''
    t[0] = t[1]
    print('Maximo nivel sin captura: ', t[0].nivelMaxSinCaptura, '.', sep='')  

def p_file(t):
    '''file : metadataInicio file
            | metadataInicio Empty'''
    if t[2] == "":
        t[0] = MaxLvlContainer(t[1].nivelMaxSinCaptura)
    else:
        t[0] = MaxLvlContainer(maxNivel(t[1], t[2]))
    
def p_metadataInicio(t):
    '''metadataInicio : LCORCHETE metadata RCORCHETE metadataSegment partida'''
    t[0] = MaxLvlContainer(t[5].nivelMaxSinCaptura)

# El segmento de metadata hace recursión hasta terminar en una partida
def p_metadataSegment_MetaData(t):
    '''metadataSegment : LCORCHETE metadata RCORCHETE metadataSegment newline
                       | LCORCHETE metadata RCORCHETE metadataSegment
                       | Empty '''

def p_metadata_renglonMetaData(t):
    '''metadata : stringMeta1 ESPACIO COMILLA stringMeta2 COMILLA'''

# Para parsear las cosas escritas usamos una recursion sobre los distintos tokens que se pueden encontrar
def p_stringMeta_escritoEnPrimerElementoMetadata(t):
    '''stringMeta1 : contenidoMeta1 stringMeta1
                   | contenidoMeta1 Empty'''
    t[0] = t[1] + t[2]

def p_contenidoMeta1_delStringMeta1(t):
    '''contenidoMeta1 : caracteresnormales
                      | EQUIS
                      | NUM
                      | FILALETRA
                      | PIEZA
                      | LPAREN
                      | RPAREN
                      | LLLAVE
                      | RLLAVE'''
    t[0] = t[1]

def p_stringMeta2_escritoEnSegundoElementoMetadata(t):
    '''stringMeta2 : contenidoMeta2 stringMeta2
                   | contenidoMeta2 Empty'''
    t[0] = t[1] + t[2]

def p_contenidoMeta2_delStringMeta2(t):
    '''contenidoMeta2 : caracteresnormales
                      | EQUIS
                      | NUM
                      | FILALETRA
                      | PIEZA
                      | ESPACIO
                      | LPAREN
                      | RPAREN
                      | LLLAVE
                      | RLLAVE'''
    t[0] = t[1]

def p_caracteresnormales(t):
    '''caracteresnormales : MENOS
                          | PUNTO
                          | CARACTERES
                          | SLASH
                          | MAS
                          | PREGUNTA
                          | EXCLAMACION
                          | O '''
    t[0] = t[1]

# Una partida empieza con una jugada y una siguiente jugada (la cual puede ser el score, indicando el final de la partida)
def p_partida(t): 
    '''partida : jugada sigjugada'''
    if t[2].numeroJugada == -1 :
        if t[1].numeroJugada != -1:
            p_error(DescripcionDeError('Numero incorrecto', str(t[1].numeroJugada)))
        t[0] = MaxLvlContainer(t[1].nivelMaxSinCaptura)
    else:
        if not (t[1].numeroJugada == 1 and (t[2].numeroJugada == 2 or t[2].numeroJugada == 0)):
            p_error(DescripcionDeError('Numero incorrecto', str(t[1].numeroJugada)))
        t[0] = MaxLvlContainer(maxNivel(t[1], t[2])) # El maximo nivel sin captura de una partida es el maximo de sus jugadas    
    
def p_jugada(t):
    '''jugada : NUM PUNTO ESPACIO movimiento primerComentario posibleRendicion '''
    if t[6].nivel != -1 :
        t[0] = Jugada(t[1], maxNivel(t[5], t[6]))
    else:
        t[0] = Jugada(-int(t[1]), maxNivel(t[5], t[5]))

    if t[5].jugada != -1 and t[0].numeroJugada != t[5].jugada:
        p_error(DescripcionDeError('Comentario con numero equivocado', ''))

    if t[0].numeroJugada == 0:
        p_error(DescripcionDeError('Numero incorrecto', str(t[1].numeroJugada)))

def p_posibleRendicion(t):
    ''' posibleRendicion : movimiento segundoComentario
                         | Empty score'''
    if t[1] == '' : 
        t[0] = Comentario(-1, -1)
    else:
        t[0] = t[2]

def p_sigjugada(t):
    '''sigjugada : jugada sigjugada 
                 | score Empty
                 | Empty Empty'''
    if t[1] == '' :
        t[0] = Jugada(-1, -1)
    else:
        if t[1].numeroJugada != 0 and not (t[2].numeroJugada==-1 and t[1].numeroJugada < 0) and not (abs(t[2].numeroJugada) == t[1].numeroJugada + 1 or t[2].numeroJugada == 0):
            p_error(DescripcionDeError('Numero incorrecto', str(t[1].numeroJugada)))
        # Pasamos el número de la jugada definida ahora como número de la siguiente jugada anterior para comparar con la anterior
        if t[2] == '':
            t[0] = Jugada(t[1].numeroJugada, t[1].nivelMaxSinCaptura)
        else:
            t[0] = Jugada(t[1].numeroJugada, maxNivel(t[1], t[2]))
        
def p_movimiento(t):
    ''' movimiento : pieza casillas mate calidad ESPACIO '''
    numCasilla = t[2].numeroDeFila
    if numCasilla == 0 or numCasilla >= 9:
        p_error(DescripcionDeError('Numero de casilla invalido', str(numCasilla)))

def p_movimiento_erroqueLargo(t):
    '''movimiento : O MENOS O MENOS O ESPACIO'''
    t[0] = t[1] + t[2] + t[3] + t[4] + t[5]

def p_movimiento_erroqueCorto(t):
    '''movimiento : O MENOS O ESPACIO'''
    t[0] = t[1] + t[2] + t[3]

def p_pieza(t):
    ''' pieza : PIEZA
              | Empty'''
    t[0] = t[1]

def p_casillas_OrigenNumero(t):
    '''casillas : NUM captura FILALETRA NUM'''
    t[0] = Casillas(int(t[4]))

def p_casillas_Captura(t):
    '''casillas : EQUIS FILALETRA NUM'''
    t[0] = Casillas(int(t[3]))

def p_casillas_Columna(t):
    '''casillas : FILALETRA NUM destinoPosible Empty
                | FILALETRA captura FILALETRA NUM'''
    if t[4] == '' : 
        if t[3].numeroDeFila == 0 :
            t[0] = Casillas(t[2])
        else: 
            t[0] = Casillas(t[3].numeroDeFila)
    else:
        t[0] = Casillas(int(t[4]))
        
def p_destinoPosible(t):
    ''' destinoPosible : captura FILALETRA NUM
                       | Empty Empty Empty'''
    if t[3] == '' : 
        t[0] = Casillas(0)
    else:
        t[0] = Casillas(t[3])
        
def p_captura(t):
    '''captura : EQUIS
               | Empty'''
    t[0] = t[1]

def p_calidad_deUnMovimiento(t):
    '''calidad : EXCLAMACION
               | PREGUNTA
               | Empty'''
    t[0] = t[1]

def p_mate(t):
    '''mate : MAS Empty
            | MAS MAS
            | Empty Empty'''
    t[0] = t[1] + t[2]

def p_primerComentario(t):
    ''' primerComentario : comentario ESPACIO tresPuntos
                         | Empty Empty Empty '''
    if(t[1] == ''):
        t[0] = Comentario(0, 0, -1)
    else:
        t[0] = Comentario(t[1].nivel, t[1].nivelMaxSinCaptura, t[3])
    
def p_tresPuntos(t):
    ''' tresPuntos : NUM PUNTO PUNTO PUNTO ESPACIO
                   | Empty'''
    if t[1]=='' : 
        t[0] = -1
    else: 
        t[0] = int(t[1])

def p_segundoComentario(t):
    ''' segundoComentario : comentario ESPACIO
                          | Empty Empty '''
    if(t[1] == ''):
        t[0] = Comentario(0, 0)
    else:
        t[0] = Comentario(t[1].nivel, t[1].nivelMaxSinCaptura)
            
def p_comentario(t):
    ''' comentario : LPAREN contenidoComentario RPAREN 
                   | LLLAVE contenidoComentario RLLAVE '''
    t[0] = Comentario(t[2].nivel, t[2].nivelMaxSinCaptura)
           
def p_contenidoComentario(t):
    ''' contenidoComentario : palabraComentario ESPACIO contenidoComentario
                          | palabraComentario Empty Empty Empty'''
    if t[2] == '' :
        t[0] = t[1]      
    else:               
        maximo_nivel = max(t[1].nivel, t[3].nivel)
        maximo_nivelCaptura = max(t[1].nivelMaxSinCaptura, t[3].nivelMaxSinCaptura)
        minimo_nivelCaptura = min(t[1].nivelMaxSinCaptura, t[3].nivelMaxSinCaptura)
        if maximo_nivelCaptura == 1 and minimo_nivelCaptura == 0 :
            t[0] = Comentario(maximo_nivel, 0)
        else :
            t[0] = Comentario(maximo_nivel, maximo_nivelCaptura)

def p_palabraComentario_escritoEnComentarios(t):
    '''palabraComentario : caracteresnormales Empty stringComentario
                         | EQUIS Empty stringComentario 
                         | PIEZA seguimientoPieza Empty
                         | FILALETRA seguimientoOrigenCasilla Empty
                         | NUM seguimientoOrigenNum Empty
                         | comentario Empty Empty'''
    if t[3] != '':
        t[0] = Comentario( t[3].nivel, t[3].nivelMaxSinCaptura)
    elif t[2] == '' :
        nivelSinCaptura = 0
        if t[1].nivelMaxSinCaptura != 0 :
            nivelSinCaptura = t[1].nivelMaxSinCaptura + 1

        t[0] = Comentario( t[1].nivel, nivelSinCaptura)
    else:
        t[0] = Comentario(1, 1-int(t[2].tieneCaptura))

def p_stringComentario_delStringComent(t):
    '''stringComentario : contenidoStringComentario stringComentario
                        | Empty Empty'''
    if t[2] == '' :
        t[0] = Comentario(1, 1)
    else :
        t[0] = Comentario(1, 1)

def p_contenidoStringComentario(t):
    '''contenidoStringComentario : caracteresnormales
                                 | EQUIS
                                 | FILALETRA
                                 | PIEZA
                                 | NUM'''
    t[0] = t[1]

def p_seguimientoPieza(t):
    '''seguimientoPieza : FILALETRA seguimientoOrigenCasilla Empty
                        | NUM seguimientoOrigenNum Empty
                        | caracteresnormales Empty stringComentario
                        | EQUIS Empty stringComentario
                        | PIEZA Empty stringComentario
                        | Empty Empty Empty '''
    if t[2] == '':
        if t[1] == '' :
            t[0] = Seguimiento(False)
        else:
            t[0] = Seguimiento(False)
    else:
        t[0] = Seguimiento( t[2].tieneCaptura)

def p_seguimientoOrigenCasilla(t):
    '''seguimientoOrigenCasilla : EQUIS seguimientoCaptura Empty
                                | NUM seguimientoOrigenNum Empty
                                | caracteresnormales Empty stringComentario
                                | FILALETRA Empty stringComentario
                                | PIEZA Empty stringComentario
                                | Empty Empty Empty'''
    if t[2] == '':
        if t[1] == '' :
            t[0] = Seguimiento(False)
        else:
            t[0] = Seguimiento(False)
    else:
        t[0] = Seguimiento(t[2].tieneCaptura)

def p_seguimientoOrigenNum(t):
    ''' seguimientoOrigenNum : EQUIS seguimientoCaptura
                             | caracteresnormales stringComentario
                             | PIEZA stringComentario 
                             | NUM stringComentario
                             | FILALETRA stringComentario
                             | Empty Empty   '''
    if t[2] != 'x':
        if t[1] == '' :
            t[0] = Seguimiento(False)
        else:
            t[0] = Seguimiento( False)
    else:
        t[0] = Seguimiento( t[2].tieneCaptura)

def p_seguimientoCaptura(t):
    '''seguimientoCaptura : FILALETRA NUM mate seguimientoMovConCaptura
                          | caracteresnormales stringComentario Empty Empty
                          | EQUIS stringComentario Empty Empty
                          | PIEZA stringComentario Empty Empty
                          | NUM stringComentario Empty Empty
                          | Empty Empty Empty Empty '''
    if t[4] == '' :
        if t[1] == '' :
            t[0] = Seguimiento(False)
        else :
            t[0] = Seguimiento(False)
    else:
        t[0] = Seguimiento(t[4].tieneCaptura)

def p_seguimientoMovConCaptura(t):
    ''' seguimientoMovConCaptura : contenidoStringComentario stringComentario
                                 | Empty Empty '''
    if t[2] == '' :
        t[0] = Seguimiento(True)
    else : 
        t[0] = Seguimiento( False)

def p_score_simplificado(t):
    '''score : NUM MENOS NUM'''
    t[0] = Jugada(0, 0)
    if int(t[1]) > 1 or int(t[3]) > 1:
        p_error(DescripcionDeError('Score invalido', f'{t[1]}{t[2]}{t[3]}' ) )

def p_score_fraccion(t):
    '''score : NUM SLASH NUM MENOS NUM SLASH NUM'''
    t[0] = Jugada(0, 0)
    if not (int(t[1]) == 1 and int(t[3]) == 2 and int(t[5]) == 1 and int(t[7]) == 2):
        p_error(DescripcionDeError('Score invalido', f'{t[1]}{t[2]}{t[3]}{t[4]}{t[5]}{t[6]}{t[2]}'))
            
def p_Empty(t):
    ''' Empty :'''
    t[0] = '' # El atributo de empty siempre es vacio('') eso nos evita problemas despues
    pass

# Funcion que se ejecuta cuando el parser falla al reconocer una cadena
def p_error(t):
    if t.value == '"': # Puede faltar el ESPACIO entre los strings de metadata
        errorMessage = f'Error en {t.type}, falta el espacio en la metadata.'
    elif t.value == ' ': # Cierre de un comentario exterior }), NUM o FILALETRA de un movimiento, puede faltar un PUNTO
        errorMessage = f'Error en {t.type}, pueden ser muchar cosas.'
    elif t.value == '-': # Puede faltar una O de enroque, puede un NUM del Score o SLASH,
        errorMessage = f'Error en {t.type}, falta un O en el enrroque.'
    elif t.value == "[":
        errorMessage = f'Error en {t.type}, falta el ] de un segmento en la metadata'
    elif t.value ==   "]" : 
        errorMessage = f'Error en {t.type}, faltan las comillas de un segmento de la metadata'
    elif re.compile(r'[^\s\[\]\"\d+\.\-a-hPNBRQK\/\+\?!xO\(\)\{\}]+' ).match(t.value):
        errorMessage = "Error en los caracteres"
    elif re.compile(r'\d+').match(t.value) : 
        errorMessage = f'Error en {t.type}, Puede faltar la FILALETRA de un movimiento, el ESPACIO al final de una jugada, pueden faltar un ESPACIO, un SLASH o un MENOS en un SCORE, pueden haber un caracer equivocado para PIEZA'    
    elif t.value == "." : 
        errorMessage = f'Error en {t.type}, puede faltar un NUM para el numero de jugada'
    elif re.compile(r'[P|N|B|R|Q|K|a-h]').match(t.value) and len(t.value) == 1:
        errorMessage = f'Error en {t.type}, falta un espacio antes del movimiento.'
    elif t.value == "/":
        errorMessage = f'Error en {t.type}, falta un numero en el score de la partida.'
    elif t.value == "+" or t.value == "?" or t.value == "!":
        errorMessage = f'Error en {t.type}, falta el numero de casilla de movimiento.'
    elif t.value == "x":
        errorMessage = f'Error en {t.type}, falta un espacio en un movimiento.'
    elif t.value == "O":
        errorMessage = f'Error en {t.type}, falta un menos en el enrroque o se esperaba un espacio antes del enroque.'
    elif t.value == ")":
        errorMessage = f'Error en {t.type}, falta texto dentro del comentario o falta un cierre de parentesis.'
    elif t.value == "{" or t.value == "(":
        errorMessage = f'Error en {t.type}, falta un espacio en el comentario.'
    elif t.value == "}":
        errorMessage = f'Error en {t.type}, falta texto dentro del comentario o falta un cierre de llaves.'
    
    # Errores de atributos
    elif t.value == 'Numero incorrecto':
        errorMessage = f'Error en {t.type}, los numeros de jugada tienene que ser consecutivos.'
    elif t.value == 'Numero de casilla invalido':
        errorMessage = f'Error en {t.type}, Numero de casilla invalido.'
    elif t.value == 'Score invalido':
        errorMessage = f'Error en {t.type}, score invalido.'
    else: # Error no reconocido
        errorMessage = f'Error en {t.type}'

    raise RejectStringError(errorMessage)
    
parser = yacc.yacc()

try:
    s = input('Path del archivo con la entrada: ')
    with open(s, 'r') as file:
        partida = file.read()
        parser.parse(partida)
except EOFError:    
    print("Error en la entrada de datos.")