
import ply.lex as lex
from ply.lex import LexError, StringTypes
import ply.yacc as yacc
from funciones_auxiliares import *

# Tokens

tokens = (
    'CARACTERES', 
    'LCORCHETE' , 'RCORCHETE',
    'COMILLA', 'ESPACIO' , 'newline',
    'MENOS', 'NUM', 'PUNTO', 'COLUMNA', 'PIEZA' , 'SLASH',
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
t_COLUMNA = r'[a-h]'
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

class Comentario:
    def __init__(self, mensaje, nivel, maxNivel):
        self.nivel = nivel
        self.mensaje = mensaje
        self.nivelMaxSinCaptura = maxNivel

class Seguimiento:
    def __init__(self, mensaje, captura):
        self.tieneCaptura = captura
        self.mensaje = mensaje

class Jugada: 
    def __init__(self, numJugada, maxNivel):
        self.numeroJugada = int(numJugada)
        self.nivelMaxSinCaptura = int(maxNivel)

class MaxLvlContainer:
    def __init__(self, maxNivel):
        self.nivelMaxSinCaptura = int(maxNivel)

class Casillas:
    def __init__(self, mensaje, numeroDeFila):
        self.mensaje = mensaje       
        self.numeroDeFila = int(numeroDeFila)

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

def p_s(t):
    '''s : file'''
    t[0] = t[1]
    print('', t[0].nivelMaxSinCaptura)  

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

#El segmento de metadata hace recursión hasta terminar en una partida
def p_metadataSegment_MetaData(t):
    '''metadataSegment : LCORCHETE metadata RCORCHETE metadataSegment
                       | Empty '''

def p_metadata_renglonMetaData(t):
    '''metadata : stringMeta1 ESPACIO COMILLA stringMeta2 COMILLA'''
    print(t[1] + ' ' + '"' + t[4] + '"')

#Para parsear las cosas escritas usamos una recursion sobre los distintos tokens que se pueden encontrar
def p_stringMeta_escritoEnPrimerElementoMetadata(t):
    '''stringMeta1 : contenidoMeta1 stringMeta1
                   | contenidoMeta1 Empty'''
    t[0] = t[1] + t[2]

def p_contenidoMeta1_delStringMeta1(t):
    '''contenidoMeta1 : caracteresnormales
                      | EQUIS
                      | NUM
                      | COLUMNA
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
                      | COLUMNA
                      | PIEZA
                      | ESPACIO
                      | LPAREN
                      | RPAREN
                      | LLLAVE
                      | RLLAVE'''
    t[0] = t[1]

def p_caracteresnormales(t):
    '''caracteresnormales : MENOS
                        | CARACTERES
                        | SLASH
                        | MAS
                        | PREGUNTA
                        | EXCLAMACION
                        | O '''
    t[0] = t[1]

#una partida empieza con una jugada y una siguiente jugada (la cual puede ser el score, indicando el final de la partida)
def p_partida(t): 
    '''partida : jugada sigjugada'''
    if not (t[1].numeroJugada == 1 and (t[2].numeroJugada == 2 or t[2].numeroJugada == 0)):
        p_error(t)
    t[0] = MaxLvlContainer(maxNivel(t[1], t[2])) #El maximo nivel sin captura de una partida es el maximo de sus jugadas    

def p_jugada(t):
    '''jugada : NUM PUNTO ESPACIO movimiento primerComentario movimiento segundoComentario '''
    print("Jugada numero", t[1], "se jugo:", t[4], t[6])

    if t[1] == "9":
        t[1] = t[1]

    t[0] = Jugada(t[1], maxNivel(t[5], t[7]))
    if t[0].numeroJugada == 0:
        p_error(t)

def p_sigjugada(t):
    '''sigjugada : jugada sigjugada 
                 | score'''
    if t[1].numeroJugada != 0 and not (t[2].numeroJugada == t[1].numeroJugada + 1 or t[2].numeroJugada == 0):
        p_error(t)
    #pasamos el número de la jugada definida ahora como número de la siguiente jugada anterior para comparar con la anterior
    t[0] = Jugada(t[1].numeroJugada, t[1].nivelMaxSinCaptura)
        
def p_movimiento(t):
    ''' movimiento : pieza casillas mate calidad ESPACIO '''
    t[0] = t[1] + t[2].mensaje + t[3] + t[4]
    
    numCasilla = t[2].numeroDeFila
    if numCasilla == 0 or numCasilla >= 9:
        p_error(t)

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
    '''casillas : NUM captura COLUMNA NUM'''
    t[0] = Casillas(t[1] + t[2] + t[3] + t[4], int(t[4]))

def p_casillas_Captura(t):
    '''casillas : EQUIS COLUMNA NUM'''
    t[0] = Casillas(t[1]+t[2]+t[3], int(t[3]))

def p_casillas_Columna(t):
    '''casillas : COLUMNA NUM destinoPosible Empty
                | COLUMNA captura COLUMNA NUM'''
    if t[4] == '' : 
        if t[3].numeroDeFila == 0 :
            t[0] = Casillas(t[1] + t[2], t[2])
        else: 
            t[0] = Casillas(t[1] + t[2] + t[3].mensaje, t[3].numeroDeFila)
    else:
        t[0] = Casillas(t[1]+t[2]+t[3]+t[4], int(t[4]))
        

def p_destinoPosible(t):
    ''' destinoPosible : captura COLUMNA NUM
                       | Empty Empty Empty'''
    if t[3] == '' : 
        t[0] = Casillas('', 0)
    else:
        t[0] = Casillas(t[1] + t[2] + t[3], t[3])
        
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

def p_seguimientoPieza(t):
    '''seguimientoPieza : COLUMNA seguimientoOrigenCasilla Empty
                        | NUM seguimientoOrigenNum Empty
                        | caracteresnormales Empty stringComentario
                        | EQUIS Empty stringComentario
                        | PIEZA Empty stringComentario
                        | Empty Empty Empty '''
    if t[2] == '':
        if t[1] == '' :
            t[0] = Seguimiento('', False)
        else:
            t[0] = Seguimiento(t[1] + t[3].mensaje, False)
    else:
        t[0] = Seguimiento(t[1]+t[2].mensaje, t[2].tieneCaptura)

def p_seguimientoOrigenCasilla(t):
    '''seguimientoOrigenCasilla : EQUIS seguimientoCaptura Empty
                                | NUM seguimientoOrigenNum Empty
                                | caracteresnormales Empty stringComentario
                                | COLUMNA Empty stringComentario
                                | PIEZA Empty stringComentario
                                | Empty Empty Empty'''
    if t[2] == '':
        if t[1] == '' :
            t[0] = Seguimiento('', False)
        else:
            t[0] = Seguimiento(t[1] + t[3].mensaje, False)
    else:
        t[0] = Seguimiento(t[1]+t[2].mensaje, t[2].tieneCaptura)

def p_seguimientoOrigenNum(t):
    ''' seguimientoOrigenNum : EQUIS seguimientoCaptura
                             | caracteresnormales stringComentario
                             | PIEZA stringComentario 
                             | NUM stringComentario
                             | COLUMNA stringComentario
                             | Empty Empty   '''
    if t[2] != 'x':
        if t[1] == '' :
            t[0] = Seguimiento('', False)
        else:
            t[0] = Seguimiento(t[1] + t[2].mensaje, False)
    else:
        t[0] = Seguimiento(t[1]+t[2].mensaje, t[2].tieneCaptura)

def p_seguimientoCaptura(t):
    '''seguimientoCaptura : COLUMNA NUM mate seguimientoMovConCaptura
                          | caracteresnormales stringComentario Empty Empty
                          | EQUIS stringComentario Empty Empty
                          | PIEZA stringComentario Empty Empty
                          | NUM stringComentario Empty Empty
                          | Empty Empty Empty Empty '''

    if t[4] == '' :
        if t[1] == '' :
            t[0] = Seguimiento('', False)
        else :
            t[0] = Seguimiento(t[1] + t[2].mensaje, False)
    else:
        t[0] = Seguimiento(t[1]+t[2]+t[3]+t[4].mensaje, t[4].tieneCaptura)

def p_seguimientoMovConCaptura(t):
    ''' seguimientoMovConCaptura : contenidoStringComentario stringComentario
                                 | Empty Empty '''
    if t[2] == '' :
        t[0] = Seguimiento('', True)
    else : 
        t[0] = Seguimiento(t[1] + t[2].mensaje, False)

def p_contenidoStringComentario(t):
    '''contenidoStringComentario : caracteresnormales
                                 | EQUIS
                                 | COLUMNA
                                 | PIEZA
                                 | NUM'''
    t[0] = t[1]

def p_stringComentario_delStringComent(t):
    '''stringComentario : contenidoStringComentario stringComentario
                        | Empty Empty'''
    if t[2] == '' :
        t[0] = Comentario('', 1, 1)
    else :
        t[0] = Comentario(t[1] + t[2].mensaje, 1, 1)

def p_palabraComentario_escritoEnComentarios(t):
    '''palabraComentario : caracteresnormales Empty stringComentario
                         | EQUIS Empty stringComentario 
                         | PIEZA seguimientoPieza Empty
                         | COLUMNA seguimientoOrigenCasilla Empty
                         | NUM seguimientoOrigenNum Empty
                         | comentario Empty Empty'''
    if t[3] != '':
        t[0] = Comentario(t[1]+t[3].mensaje, t[3].nivel, t[3].nivelMaxSinCaptura)
    elif t[2] == '' :
        nivelSinCaptura = 0

        if t[1].nivelMaxSinCaptura != 0 :
            nivelSinCaptura = t[1].nivelMaxSinCaptura + 1

        t[0] = Comentario(t[1].mensaje, t[1].nivel, nivelSinCaptura)
    else:
        t[0] = Comentario(t[1]+t[2].mensaje, 1, 1-int(t[2].tieneCaptura))
        
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
            t[0] = Comentario(t[1].mensaje + t[2] + t[3].mensaje, maximo_nivel, 0)
        else :
            t[0] = Comentario(t[1].mensaje + t[2] + t[3].mensaje, maximo_nivel, maximo_nivelCaptura)
            
def p_comentario(t):
    ''' comentario : LPAREN contenidoComentario RPAREN 
                   | LLLAVE contenidoComentario RLLAVE '''
    
    t[0] = Comentario(t[1] + t[2].mensaje + t[3] , t[2].nivel, t[2].nivelMaxSinCaptura)
    
    if t[0].nivel != 0 :
        print("Comentario: ", t[0].mensaje, ". Con nivel: ", t[0].nivel, "y max coment sin capturas: ", t[0].nivelMaxSinCaptura)


def p_tresPuntos(t):
    ''' tresPuntos : NUM PUNTO PUNTO PUNTO ESPACIO
                   | Empty'''
    if t[1]=='' : 
        t[0] = 0
    else: 
        t[0] = int(t[1])

def p_primerComentario(t):
    ''' primerComentario : comentario ESPACIO tresPuntos
                         | Empty Empty Empty '''

    if(t[1] == ''):
        t[0] = Comentario('', 0, 0)
    else:
        t[0] = Comentario(t[1].mensaje + t[2], t[1].nivel, t[1].nivelMaxSinCaptura)
    
    if t[0].nivel != 0 :
        print("Comentario: ", t[0].mensaje, ". Con nivel: ", t[0].nivel, "y max coment sin capturas: ", t[0].nivelMaxSinCaptura)


def p_segundoComentario(t):
    ''' segundoComentario : comentario ESPACIO
                          | Empty Empty '''
    if(t[1] == ''):
        t[0] = Comentario('', 0, 0)
    else:
        t[0] = Comentario(t[1].mensaje + t[2], t[1].nivel, t[1].nivelMaxSinCaptura)
    
    if t[0].nivel != 0 :
        print("Comentario: ", t[0].mensaje, ". Con nivel: ", t[0].nivel, "y max coment sin capturas: ", t[0].nivelMaxSinCaptura)

def p_score_simplificado(t):
    '''score : NUM MENOS NUM'''
    t[0] = Jugada(0, 0)
    if int(t[1]) > 1 or int(t[3]) > 1:
        p_error(t)

def p_score_fraccion(t):
    '''score : NUM SLASH NUM MENOS NUM SLASH NUM'''
    t[0] = Jugada(0, 0)
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

# Test 7: partida con enrroque corto y largo
testsToRun.append(('''[prueba "loca"]
1. a4! Bxg5 2. O-O h3++ 3. O-O-O N2d4 0-1''', 1))

# Test 8: partida con parentesis y llaves en los strings y comentarios
testsToRun.append(('''[prueba "loca"]
1. a4! (aisjdoaijdqoiwdj31124oqjd13jiqdjq) Bxg5 {sakdasidasda8g+sdi} 2. O-O h3++ 3. O-O-O {sdlajsid JUH775753DdffP-+KJ} N2d4 0-1''', 1))

# Test 9: partida con comentarios dentro de comentarios
testsToRun.append(('''[test9 "loca"]
1. a4! (aisjdoaijdqoiwdj Pe6 31124oqjd13jiqdjq) Bxg5 {sakdasid Bxg5!+ asdasdi (asdjas324jsadi3j qefi)} 2. O-O h3++ 3. O-O-O {sdlajsid JUH775753DdffP-+KJ {dqdoi h3++ sajd8998 {odaoausd0} sds3 (lsaks iji ksdi)}} N2d4 0-1''', 1))

# Test 10: partida con comentarios con capturas dentro
testsToRun.append(('''[test "loca"]
1. a4! (Bxg5 h3++) Bxg5 {h3++ Bxg5!+ a3+ (asdasd)} 2. O-O h3++ 3. O-O-O {Bxg5 JUH775753DdffP-+KJ {dqdoi {Bxg5} sds3 (lsaks iji Bxg5 ksdi)}} N2d4 0-1''', 1))

# Test 11: Multiples partidas en un archivo
testsToRun.append(('''[test "loca"]
1. a4! (Bxg5 h3++) Bxg5 {h3++ Bxg5!+ a3+ (asdasd)} 0-1

[test "loca"]
1. a4! (Bxg5 h3++) Bxg5 2. a5 a6 0-1
''', 1))

# Test 12: Comentario con 3 puntos
testsToRun.append(('''[test "loca"]
1. a4! (Bxg5 h3++) 1... Bxg5 {h3++ Bxg5!+ a3+ (asdasd)} 2. a2! (maravillosa jugada) 2... e5 0-1''', 1))

# Test 13:
testsToRun.append(('''[prueba "loca"]
[Nzscf5qWgtg~NVX "56B~n~nQIeAhy"]
[gvk7dXkliRpR "2LAkQJGhz81"]
[~NFS5lBHW4Mm~NmJsP "e4ZhVulzl"]
[yZ1PSI4r78KP "XwWzscEtUqkAu~nNt7Hq5"]
[GArzOdNa~nITcsbFO9ES "WUodxeqxI"]

1. 1d7 d7 2. Rf8 gg7 1-0

[2ujZrN6LTmOBGss5jzqw "pnAGk"]
[kRM "lihgftp5kLaiAvuNSub2"]
[vUPhgAiKx "a9C7isOkq0vyep7svNE"]
[Lbfh "j6htrD1wKNFryNGHdUcG"]

1. Pxe7 Pad3 2. Be6 b6 3. Bb2 h3 4. Qc1 Kh3 5. Pb1 Pb2 6. Ra1 a7! 7. Nce4 Qxa3 8. Kd4 Qh1 9. Kd8 fh6 10. Nc1 Pg1 11. Nh2 Bf4 12. ca6 Kd8 13. Nb4 d5 14. e1 Ra5 15. f8 K5xd3 16. b6 (Ka4 h 5a2) 16... g7 17. e5 Bg2 18. f3 Re2 19. Qc6 Kb4 20. Rg4 Rg3 21. g3 N2c7 22. Pb7 Rh7 23. Qd3 {bf8 B b3 K Nxf5 wuFzW c1 Pbd2 T c8 ka Pg3 K Ke6+ n Kg5 Pb7 f8 e2 O 1c5 Rxe4 Pxc5} 23... e6 24. d5 Nh7 25. Qxc6 Bxc3 26. Bf5 Qfa3 27. f4 Ka7 28. Nxb6 d6 29. Bg1 Qf2 30. Pb3 d6 31. Ba3 e7 32. Bab4 Kda1 33. Ph1 e2 34. cf4 Nxd7 35. Nc7 (gr Pfg2 iONp utl Pcd2 t (Pd3 Rc2 Bxd6 Kxg8 Kxh2 h6 Bxc8 zAx g2 qX Nh2 N c3 ~n Bxb5 D Nd1 h8 a1 c7 PVAO Rg7 g5 Kb6 oGq) rt Pf8 Qp) 35... e2 36. Ra6 Bhb8 37. Q5a4 c5 38. Qg7 g1 39. g6 Pg7 40. Kd6 d1 41. h7+ Kcc5 42. Qd8 ce1 43. Qxh3 Pa6 44. Bxe2 e4 45. Bh7 d2+ 1/2-1/2

[BYsR4sFynE2R~n2 "lNykA4WPhvh2kKPTjfaD"]
[loCuhQ "WDOTwZIISKjDik~n6"]
1. Pb7 ec6 2. f4 Nxf7 3. Kxe5 d7 4. Kc7 Rd6 5. e7 Qc7 6. h1 {sRxb7 iI d5 Nh7} 6... e4+ 7. 7d6 Nf7a3 8. Pa7 e2 9. h8 h4 10. g8 Kxf6 11. 2b3 Bxg3 12. Q5h1 Pb6 13. fd4 e5 14. 5c6 f3 15. cb6 {lPb6} 15... Pb1 16. Nb3 h7 17. b2 Nb7 18. Ra1 N8h6 19. f2 c8 20. P5g1 e1 21. Pg3 c3 22. f5 Kh1 23. Pd7 Nf3 24. Nd1 Rd1 25. Kd5 Ng8 26. e3 Nxg6 27. Rh8 fc3 28. Kxf1 Ncc4 29. c1+ e3 30. cc6 (aKdxa3 e7 JQ Qe2 VLzeFq c7 FU f4 N Qxb7 Nd8++ Tf Nd2 yN ba2 me1b6 hu Kd7 R Pxe6 Nxg7 DaR Ba8 Kxd5 Nd7 ttxI fe7 GK a2 m f6 Skp) 30... h8 31. Qh1 a1 32. fb7 b7 0-1

[4e "ws20"]

1. Bxd1 Pa6 0-1''', 1))

# Otras partidas para depues testear

'''[Event "Mannheim"]
[Site "Mannheim GER"]
[Date "1914.08.01"]
[EventDate "1914.07.20"]
[Round "11"]
[Result "1-0"]
[White "Alexander Alekhine"]
[Black "Hans Fahrni"]
[ECO "C13"]
[WhiteElo "?"]
[BlackElo "?"]
[PlyCount "45"]

1. e4 {Notes by Richard Reti} 1... e6 2. d4 d5 3. Nc3 Nf6 4. Bg5 Be7 5. e5 Nfd7 6. h4 {This ingenious method of play which has subsequently been adopted by all modern masters is characteristic of Alekhine’s style.} 6... Bxg5 7. hxg5 Qxg5 8. Nh3 {! The short-stepping knight is always brought as near as possible to the actual battle field. Therefore White does not make the plausible move 8 Nf3 but 8 Nh3 so as to get the knight to f4.} 8... Qe7 9. Nf4 Nf8 10. Qg4 f5 {The only move. Not only was 11 Qxg7 threatened but also Nxd5.} 11. exf6 gxf6 12. O-O-O {He again threatens Nxd5.} 12... c6 13. Re1 Kd8 14. Rh6 e5 15. Qh4 Nbd7 16. Bd3 e4 17. Qg3 Qf7 {Forced - the sacrifice of the knight at d5 was threatened and after 17...Qd6 18 Bxe4 dxe4 19 Rxe4 and 20 Qg7 wins.} 18. Bxe4 dxe4 19. Nxe4 Rg8 20. Qa3 {Here, as so often happens, a surprising move and one difficult to have foreseen, forms the kernel of an apparently simple Alekhine combination.} 20... Qg7 {After 20.Qe7 21.Qa5+ b6 22.Qc3 would follow.} 21. Nd6 Nb6 22. Ne8 Qf7 {White mates in three moves.} 23. Qd6+ 1-0'''

'''[a "b"]

1. e4 d5 {defensa escandinava (es com´un 2. exd5 Da5 {no es com´un 2... c6})} 1/2-1/2'''

# Se puede descomentar una linea en runTest para que los test sean los paths
# a los txt y no la cadena directa a parsear
runTests(testsToRun, parser.parse)