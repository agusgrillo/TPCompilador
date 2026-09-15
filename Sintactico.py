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

    @_('tipo lista_variables ";"')
    def sentencia_declarativa(self, p):

        for variable in p.lista_variables:

            if variable in self.tabla_de_simbolos:
                self.errores_sintacticos.append(
                    f"Variable '{variable}' declarada más de una vez."
                )

            else:
                if p.tipo == 'LONGINT':
                    self.tabla_de_simbolos[variable] = {
                        'tipo': 'LONGINT',
                        'valor': 0
                    }

                elif p.tipo == 'SINGLEF':
                    self.tabla_de_simbolos[variable] = {
                        'tipo': 'SINGLEF',
                        'valor': 0.0
                    }

        self.estructuras_detectadas.append(
            f"Declaración {p.tipo}: {p.lista_variables}"
        )

        return (
            'DECLARACION',
            p.tipo,
            p.lista_variables
        )
    #Funcion como declaracion
    @_('sentencia_funcion')
    def sentencia_declarativa(self, p):
        return p.sentencia_function

    # Enumeración / TYPEDEF
    @_('TYPEDEF ID ASIGN_IGUAL "[" lista_valores "]" ";"')
    def sentencia_declarativa(self, p):
        self.tabla_de_simbolos[p.ID] = {
            'tipo': 'TYPEDEF',
            'valores': p.lista_valores
        }
        self.estructuras_detectadas.append(f"Línea {p.lineno}:TYPEDEF '{p.ID}'")
        return (
            'TYPEDEF',
            p.ID,
            p.lista_valores
        )
    #asignacion de tipo declarado del typedef
    @_('ID lista_variables ";"')
    def sentencia_declarativa(self, p):

        self.estructuras_detectadas.append(
            f"Declaración del tipo '{p.ID}': {p.lista_variables}"
        )
        return (
            'DECLARACION_TIPO_USUARIO',
            p.ID,
            p.lista_variables
        )
    #Declaracion de variables separadas por comas
    @_('lista_variables "," ID')
    def lista_variables(self, p):
        lista_actual = p.lista_variables
        lista_actual.append(p.ID)
        return lista_actual

    @_('ID')
    def lista_variables(self, p):
        return [p.ID]

    #declaracion de clases
    @_('sentencia_clase')
    def sentencia_declarativa(self, p):
        return p.sentencia_clase

    #tipos
    @_('LONGINT')
    def tipo(self, p):
        return 'LONGINT'
    @_('SINGLEF')
    def tipo(self, p):
        return 'SINGLEF'

    #-------------------------------------------------------------------
    #Fin de la parte declarativa
    #-------------------------------------------------------------------
    
    #Parte ejecutable
    @_('sentencias_ejecutables sentencia_ejecutable')
    def sentencias_ejecutables(self, p):
        p.sentencias_ejecutables.append(p.sentencia_ejecutable)
        return p.sentencias_ejecutables
    @_('sentencia_ejecutable')
    def sentencias_ejecutables(self, p):
        return [p.sentencia_ejecutable]

    #Asignacion
    @_('asignacion ";"')
    def sentencia_ejecutable(self,p):
        return p.asignacion
    #if
    @_('sentencia_if')
    def sentencia_ejecutable(self, p):
        return p.sentencia_if
    #repeat
    @_('sentencia_repeat')
    def sentencia_ejecutable(self, p):
        return p.sentencia_repeat
    #pout
    @_('salida ";"')
    def sentencia_ejecutable(self, p):
        return p.salida
    #llamado de funcion
    @_('llamado_funcion ";"')
    def sentencia_ejecutable(self, p):
        return p.llamado_funcion
    #tosf
    @_('sentencia_conv ";"')
    def sentencia_ejecutable(self, p):
        return p.sentencia_conv
    #retorno
    @_('retorno')
    def sentencia_ejecutable(self, p):
        return p.retorno

    #ASIGNACIONES

    @_('referencia ASIGN expresion'
       'referencia ASIGN_IGUAL expresion')
    def asignacion(self,p):
        if p[1] == ':=':
            self.estructuras_detectadas.append(f"Línea {p.lineno}:Asignación ':=' sobre {p.referencia}")
        elif p[1] == '=':
            self.estructuras_detectadas.append(f"Línea {p.lineno}:Asignación '=' sobre {p.referencia}")
        #si la variable ya esta asignada
        if isinstance(p.referencia, str):
            if p.referencia not in self.tabla_de_simbolos:
                self.errores_sintacticos.append(f"Variable '{p.referencia}' no declarada" )
            else:
                self.tabla_de_simbolos[p.referencia]['valor'] = p.expresion
        return('ASIGNACION',p.referencia,p.expresion)

    #REFERENCIAS

    @_('ID')
    def referencia(self, p):
        return p.ID

    @_('referencia "." ID')
    def referencia(self, p):
        return ('REFERENCIA',p.referencia, p.ID)

    #EXPRESIONES MATEMATICAS
    @_('expresion MAS termino', 
       'expresion MENOS termino')
    def expresion(self, p):
        return ('OP_BINARIA', p[1], p.expresion, p.termino)

    @_('termino')
    def expresion(self, p):
        return p.termino

    @_('termino MULT factor', 
       'termino DIV factor')
    def termino(self, p):
        return ('OP_BINARIA', p[1], p.termino, p.factor)

    @_('factor')
    def termino(self, p):
        return p.factor

    @_('numero','FLOAT','referencia','asign_expresion','llamado_funcion','sentencia_conv')
    def factor(self, p):
        return(p[0])
    
    @_('MENOS NUMBER %prec UMINUS')
    def factor(self, p):
        return ('NEGATIVO',-p.NUMBER)


    @_('ID ASIGN_IGUAL "(" expresion_estricta ")"')
    def asign_expresion(self,p):
        return ('ASIGNACION_EN_EXPRESION', p.ID, p.expresion_estricta)

    @_('expresion_estricta MAS termino_estricto',
       'expresion_estricta MENOS termino_estricto')
    def expresion_estricta (self,p):
        return('OP_BINARIA',p[1],p.expresion_estricta,p.termino_estricto)

    @_('termino_estricto')
    def expresion_estricta(self,p):
        return(p.termino_estricto)

    @_('termino_estricto MULT factor_estricto',
       'termino_estricto DIV factor_estricto')
    def termino_estricto (self , p):
        if p[1] == 'DIV':
            if p[2] == 0:
                self.errores_sintacticos.append(f"Línea {p.lineno}: Error: División por cero.")
                raise ZeroDivisionError("Error: División por cero.")
        return('OP_BINARIA',p[1],p.termino_estricto,p.factor_estricto)

    @_('factor_estricto')
    def termino_estricto (self , p):
        return(p.factor_estricto)

    @_('numero','FLOAT','ID','llamado_funcion','sentencia_conv')
    def factor_estricto(self,p):
        return p[0]

    @_('MENOS NUMBER %prec UMINUS')
    def factor_estricto(self, p):
        return ('NEGATIVO',-p.NUMBER)

    @_('NUMBER')
    def numero(self, p):
        if p.NUMBER > 2147483647:
            raise ValueError(f"Constante entera positiva fuera de rango: {p.NUMBER}")
        return p.NUMBER

    #Estructura Condicion
    @_('expresion comparador expresion')
    def condicion(self,p):
        return('CONDICION',p[1],p[0],p[2])

    #comparadores
    @_('MAYOR', 'MENOR', 'MAYORIGUAL', 'MENORIGUAL', 'IGUAL', 'DIFERENTE')
    def comparador (self, p):
        return p[0]

    #bloque de control
    @_('sentencia_ejecutable')
    def bloque_control(self, p):
        return [p.sentencia_ejecutable]

    @_('BEGIN sentencias_ejecutables END')
    def bloque_control(self, p):
        return p.sentencias_ejecutables

    # Estructura IF
    @_('IF "(" condicion ")" bloque_control END_IF ";"')
    def sentencia_if (self,p):
        self.estructuras_detectadas.append(f"Línea {p.lineno}:Estructura IF")
        return ('IF', p.condicion, p.bloque_control)
    #IF-ELSE
    @_('IF "(" condicion ")" bloque_control ELSE bloque_control END_IF ";"')
    def sentencia_if (self,p):
        self.estructuras_detectadas.append(f"Línea {p.lineno}:Estructura IF-ELSE")
        return ('IF-ELSE', p.condicion, p.bloque_control)

    #REPEAT UNTIL
    @_('REPEAT bloque_control UNTIL "(" condicion ")" ";"')
    def sentencia_repeat(self, p):
        self.estructuras_detectadas.append(f"Línea {p.lineno}: Sentencia REPEAT")
        return ('REPEAT', p.bloque_control, p.condicion)

    #FUNCIONES
    @_('tipo FUNCTION ID "(" parametros_formales ")" sentencias_declarativas BEGIN sentencias_ejecutables END ";"')
    def declaracion_funcion(self, p):
        return ('FUNCION', p.tipo, p.ID, p.parametros_formales, p.sentencias_declarativas, p.sentencias_ejecutables)

    #para mas de una variable
    @_('tipo ID')
    def parametros_formales(self, p):
        return [(p.tipo, p.ID)]
    @_('parametros_formales "," tipo ID')
    def parametros_formales(self, p):
        p.parametros_formales.append((p.tipo, p.ID))
        return p.parametros_formales
    @_('RET "(" expresion ")" ";"')
    def retorno(self, p):
        return ('RETORNO', p.expresion)