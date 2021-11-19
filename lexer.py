from ply import lex


# Tokens

tokens = (
    'NUM', 'LETRAS', 
    'LPAREN' , 'RPAREN' , 'LLLAVE' , 'RLLAVE' , 'LCORCHETE' , 'RCORCHETE' ,
    'EQUIS' , 'CIRCULO' , 'MENOS' , 'MAS' , 'SLASH' , 'EXCLAMACION' , 'PREGUNTA' , 'PUNTO', 'COMILLAS' 
)

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LLLAVE = r'\{'
t_RLLAVE = r'\}'
t_LCORCHETE = r'\['
t_RCORCHETE = r'\]'

t_LETRAS = r'[a-zA-Z]'
t_CRUZ = r'x'
t_CIRCULO = r'O'
t_MENOS = r'-'
t_SLASH = r'/'
t_EXCLAMACION = r'\!'
t_PREGUNTA = r'\?'
t_PUNTO = r'\.'
t_COMILLA = r'\''



def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    #raise LexerError("Illegal character '%s'" % t.value)
    #t.lexer.skip(1)
 
def t_NUM(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer too large, %d", t.value)
        t.value = 0
    return t

precedence = ()