
class RejectStringError(Exception):
    def __init__(self, t):
        self.t = t

def maxNivel(attrComentario1, attrComentario2):
    return max(attrComentario1.nivelMaxSinCaptura, attrComentario2.nivelMaxSinCaptura)
