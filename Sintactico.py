import sly
from Lexico import Lexico

class Sintactico(sly.Parser):
    tokens = Lexico.tokens

    precedence = (
        ('left', 'MAS', 'MENOS'),
        ('left', 'MULT', 'DIV'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.variables = {}
        self.estructuras_detectadas = []
        self.errores_sintacticos = []

    @_('ID ASIGN expr')
    def statement(self, p):
        self.estructuras_detectadas.append(f"Línea {p.lineno}: Asignación")
        self.variables[p.ID] = p.expr
        return f"{p.ID} = {p.expr}"

    @_('expr')
    def statement(self, p):
        self.estructuras_detectadas.append(f"Línea {p.lineno}: Expresión")
        return p.expr

    @_('expr MAS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MENOS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr MULT expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIV expr')
    def expr(self, p):
        if p.expr1 == 0:
            raise ZeroDivisionError("Error: División por cero.")
        return p.expr0 / p.expr1

    @_('MENOS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('NUMBER')
    def expr(self, p):
        numero = int(p.NUMBER)
        if numero < -2147483648 or numero > 2147483647:
            raise ValueError(f"Error: Constante entera fuera del rango permitido: {numero}")
        else:
            return int(p.NUMBER)

    @_('FLOAT')
    def expr(self, p):
        return float(p.FLOAT)