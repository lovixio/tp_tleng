def green(mes):
    return '\033[92m' + mes + '\033[0m'

def red(mes):
    return '\033[91m' + mes + '\033[0m'

def runTests(listOfTests, parser):
    i = 1
    for test in listOfTests:
        res = parserF(test[0], parser)
        if res == test[1]:
            print(green("Paso el test " + str(i)))
        else:
            print(red('Error en el test ' + str(i)))
        i = i + 1

class RejectStringError(Exception):
    def __init__(self, t):
        self.t = t

def parserF(cadena, parser):
    try:
        parser(cadena)
        #openAndParse(cadena, parser) "Descomentar esta linea si cadena es un path a un txt"
        return 1
    except RejectStringError as inst:
        print(inst)
        return -1

def openAndParse(file, parser):
    with open(file, 'r') as file:
        partida = file.read()
        return parser(partida)
