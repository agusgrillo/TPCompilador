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
        self.tabla_de_simbolos = {}
        self.estructuras_detectadas = []
        self.errores_sintacticos = []


    # Definición de reglas de producción  
    @_('ID sentencias_declarativas BEGIN sentencias_ejecutables END')
    def programa(self, p):
        self.estructuras_detectadas.append(f"Línea {p.lineno}: Estructura de Programa '{p.ID}'")
        return ('PROGRAMA', p.ID, p.sentencias_declarativas, p.sentencias_ejecutables)

    #Definición de reglas de producción para sentencias declarativas y ejecutables
    #parte declarativa
    @_('sentencia_declarativa')
    def sentencias_declarativas(self, p):
        return [p.sentencia_declarativa]

    @_('sentencias_declarativas sentencia_declarativa')
    def sentencias_declarativas(self, p):
        p.sentencias_declarativas.append(p.sentencia_declarativa)
        return p.sentencias_declarativas

    
    @_('SINGLEF lista_variables ";"')
    def sentencia_declarativa(self, p):
        self.estructuras_detectadas.append(f"Línea {p.lineno}: Declaración de singlef para variables: {p.lista_variables}")
        for var in p.lista_variables:
            self.tabla_de_simbolos[var] = 0.0  # inicializamos las variables en 0.0
        return f"Declaración de singlef: {p.lista_variables}"

    @_('LONGINT lista_variables ";"')
    def sentencia_declarativa(self, p):
        self.estructuras_detectadas.append(f"Línea {p.lineno}: Declaración de longint para variables: {p.lista_variables}")
        for var in p.lista_variables:
            self.tabla_de_simbolos[var] = 0  # inicializamos las variables en 0
        return f"Declaración de longint: {p.lista_variables}"

    @_('lista_variables "," ID')
    def lista_variables(self, p):
        lista_actual = p.lista_variables
        lista_actual.append(p.ID)
        return lista_actual

    @_('ID')
    def lista_variables(self, p):
        return [p.ID]
    
    #Fin de la parte declarativa
    #Parte ejecutable
    @_('sentencias_ejecutables sentencia_ejecutable')
    def sentencias_ejecutables(self, p):
        p.sentencias_ejecutables.append(p.sentencia_ejecutable)
        return p.sentencias_ejecutables
    

    @_('ID ASIGN  expr',
       'ID ASIGN_IGUAL expr')
    def sentencia_ejecutable(self, p):
        self.estructuras_detectadas.append(f"Línea {p.lineno}: Asignación")
        self.tabla_de_simbolos[p.ID] = p.expr
        return f"{p.ID} = {p.expr}"

    @_('expr')
    def sentencia_ejecutable(self, p):
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
            self.errores_sintacticos.append(f"Línea {p.lineno}: Error: División por cero.")
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