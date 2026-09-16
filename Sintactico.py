import sly
from Lexico import Lexico

class Sintactico(sly.Parser):
    tokens = Lexico.tokens
    debugfile = 'parser.out'
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
    @_('ID sentencias_declarativas bloque_delimitado')
    def programa(self, p):
        self.estructuras_detectadas.append(f"Línea {p.lineno}: Estructura de Programa '{p.ID}'")
        return ('PROGRAMA', p.ID, p.sentencias_declarativas, p.bloque_delimitado)

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
    #manejo de errores: falta de ";" en las declaraciones
    #Funcion como declaracion
    @_('sentencia_funcion')
    def sentencia_declarativa(self, p):
        return p.sentencia_funcion

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
    #Manejo de errores: falta ;
    @_('TYPEDEF ID ASIGN_IGUAL "[" lista_valores "]" error')
    def sentencia_declarativa(self, p):
        self.errores_sintacticos.append(
            f"Línea {p.lineno}: Error Sintáctico: Falta ';' al final de la sentencia TYPEDEF."
        )
        return ('TYPEDEF', p.ID, p.lista_valores)
    @_('NUMBER')
    def lista_valores(self, p):
        return [p.NUMBER]

    @_('lista_valores "," NUMBER')
    def lista_valores(self, p):
        p.lista_valores.append(p.NUMBER)
        return p.lista_valores
    
    #asignacion de tipo declarado del typedef
    @_('ID lista_variables ";"')
    def sentencia_declarativa(self, p):
        self.estructuras_detectadas.append(
            f"Declaración del tipo '{p.ID}': {p.lista_variables}"
        )
        return ('DECLARACION_TIPO_USUARIO', p.ID,p.lista_variables)
    # TYPEDEF pero sin ";"
    @_('ID lista_variables error')
    def sentencia_declarativa(self, p):
        self.errores_sintacticos.append(
            f"Línea {p.lineno}: Error Sintáctico: Falta ';' al final de la declaración de variables de tipo '{p.ID}'."
        )
        return ('DECLARACION_TIPO_USUARIO', p.ID, p.lista_variables)

    #Declaracion de variables separadas por comas
    @_('lista_variables "," ID')
    def lista_variables(self, p):
        lista_actual = p.lista_variables
        lista_actual.append(p.ID)
        return lista_actual

    @_('ID')
    def lista_variables(self, p):
        return [p.ID]

    # Manejo de errores, falta de , en la declaracion
    @_('tipo lista_variables error ";"')
    def sentencia_declarativa(self, p):
        lista_recuperada = list(p.lista_variables)
        if hasattr(p.error, 'type') and p.error.type == 'ID':
            lista_recuperada.append(p.error.value)

        for variable in lista_recuperada:
            if variable in self.tabla_de_simbolos:
                self.errores_sintacticos.append(
                    f"Variable '{variable}' declarada más de una vez."
                )
            elif p.tipo == 'LONGINT':
                self.tabla_de_simbolos[variable] = {
                    'tipo': 'LONGINT',
                    'valor': 0
                }
            elif p.tipo == 'SINGLEF':
                self.tabla_de_simbolos[variable] = {
                    'tipo': 'SINGLEF',
                    'valor': 0.0
                }

        self.errores_sintacticos.append(
            f"Línea {p.lineno}: Error Sintáctico: "
            f"Falta ',' en la declaración de variables."
        )
        return (
            'DECLARACION',
            p.tipo,
            lista_recuperada
        )
    
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
 # CUERPO O CONTENIDO DE SENTENCIAS EJECUTABLES (Sin el ';')
    @_('asignacion',
       'salida',
       'llamado_funcion',
       'sentencia_conv',
       'retorno')
    def sentencia_base(self, p):
        return p[0]


    # Caso correcto: Cualquier sentencia_base seguida de ';'
    @_('sentencia_base ";"')
    def sentencia_ejecutable(self, p):
        return p.sentencia_base

    # ERROR GENERAL: Falta de ';' en cualquier sentencia_base
    @_('sentencia_base error')
    def sentencia_ejecutable(self, p):
        self.errores_sintacticos.append(
            f"Línea {p.lineno}: Error Sintáctico: Falta ';' al final de la sentencia."
        )
        return p.sentencia_base
    
    #if
    @_('sentencia_if')
    def sentencia_ejecutable(self, p):
        return p.sentencia_if
    #repeat
    @_('sentencia_repeat')
    def sentencia_ejecutable(self, p):
        return p.sentencia_repeat

    #ASIGNACIONES

    @_('referencia ASIGN expresion',
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

    @_('bloque_delimitado')
    def bloque_control(self, p):
        return p.bloque_delimitado

    # Estructura IF
    @_('IF "(" condicion ")" bloque_control END_IF ";"')
    def sentencia_if (self,p):
        self.estructuras_detectadas.append(f"Línea {p.lineno}:Estructura IF")
        return ('IF', p.condicion, p.bloque_control)
    # Estructura IF sin ";"
    @_('IF "(" condicion ")" bloque_control END_IF error')
    def sentencia_if (self,p):
        self.errores_sintacticos.append(
            f"Línea {p.lineno}: Error Sintáctico: Falta ';' al final de la sentencia IF."
        )
        return ('IF', p.condicion, p.bloque_control)
    
    #IF-ELSE
    @_('IF "(" condicion ")" bloque_control ELSE bloque_control END_IF ";"')
    def sentencia_if (self,p):
        self.estructuras_detectadas.append(f"Línea {p.lineno}:Estructura IF-ELSE")
        return ('IF-ELSE', p.condicion, p.bloque_control0, p.bloque_control1)
     #IF-ELSE sin ";"
    @_('IF "(" condicion ")" bloque_control ELSE bloque_control END_IF error')
    def sentencia_if (self,p):
        self.errores_sintacticos.append(
            f"Línea {p.lineno}: Error Sintáctico: Falta ';' al final de la sentencia IF-ELSE."
        )
        return ('IF-ELSE', p.condicion, p.bloque_control0, p.bloque_control1)

    #REPEAT UNTIL
    @_('REPEAT bloque_control UNTIL "(" condicion ")" ";"')
    def sentencia_repeat(self, p):
        self.estructuras_detectadas.append(f"Línea {p.lineno}: Sentencia REPEAT")
        return ('REPEAT', p.bloque_control, p.condicion)
    #REPEAT UNTIL sin ;
    @_('REPEAT bloque_control UNTIL "(" condicion ")" error')
    def sentencia_repeat(self, p):
        self.errores_sintacticos.append(
            f"Línea {p.lineno}: Error Sintáctico: Falta ';' al final de la sentencia REPEAT."
        )
        return ('REPEAT', p.bloque_control, p.condicion)

    #FUNCIONES
    @_('tipo FUNCTION ID "(" parametros_formales ")" sentencias_declarativas bloque_delimitado ";"')
    def sentencia_funcion(self, p):
        return ('FUNCION', p.tipo, p.ID, p.parametros_formales, p.sentencias_declarativas, p.bloque_delimitado)

    @_('tipo FUNCTION ID "(" parametros_formales ")" sentencias_declarativas bloque_delimitado error')
    def sentencia_funcion(self, p):
        self.errores_sintacticos.append(f"Línea {p.lineno}: Error Sintáctico: Falta ';' al final de la declaración de función.")
        return ('FUNCION', p.tipo, p.ID, p.parametros_formales, p.sentencias_declarativas, p.bloque_delimitado)

    #Manejo de error: falta nombre de funcion
    @_('tipo FUNCTION error "(" parametros_formales ")" sentencias_declarativas bloque_delimitado ";"')
    def sentencia_funcion(self, p):
        self.errores_sintacticos.append(
            f"Línea {p.lineno}: Error Sintáctico: Falta el nombre de la función."
        )
        return (
            'FUNCION',
            p.tipo,
            None,
            p.parametros_formales,
            p.sentencias_declarativas,
            p.bloque_delimitado
        )

    #para mas de una variable

    @_('tipo ID')
    def parametros_formales(self, p):
        return [(p.tipo, p.ID)]
    @_('parametros_formales "," tipo ID')
    def parametros_formales(self, p):
        p.parametros_formales.append((p.tipo, p.ID))
        return p.parametros_formales
    #expresion de retorno
    @_('RET "(" expresion ")"')
    def retorno(self, p):
        self.estructuras_detectadas.append("Retorno de función")
        return ('RETORNO', p.expresion)

    # invocacion
    @_('ID "(" parametros_reales ")" orden_evaluacion')
    def llamado_funcion(self,p):
        self.estructuras_detectadas.append(f"Línea {p.lineno}: Invocacion a funcion {p.ID}")
        return('LLAMADO_FUNCION',p.ID,p.parametros_reales)

    @_('expresion')
    def parametros_reales (self,p):
        return[p.expresion]
    @_('parametros_reales "," expresion')
    def parametros_reales(self, p):
        p.parametros_reales.append(p.expresion)
        return p.parametros_reales

    @_('"[" lista_valores "]"')
    def orden_evaluacion(self, p):
        return p.lista_valores

    @_('') # Regla vacía porque el orden es opcional
    def orden_evaluacion(self, p):
        return None

    @_('POUT "(" STRINGM ")"')
    def salida(self, p):
        self.estructuras_detectadas.append(
            f"En linea: {p.lineno} Salida POUT"
        )
        return ('POUT_STRING', p.STRINGM)


    @_('POUT "(" expresion ")"')
    def salida(self, p):
        self.estructuras_detectadas.append(
            f"En linea: {p.lineno} Salida POUT"
        )
        return ('POUT', p.expresion)

    #Clases
    @_('CLASS ID BEGIN cuerpo_clase END ";"')
    def sentencia_clase(self, p):
        self.estructuras_detectadas.append(f"En linea {p.lineno}: CLASE {p.ID}")
        return ('CLASE', 
                p.ID, 
                p.cuerpo_clase)

    @_('CLASS ID BEGIN cuerpo_clase END error')
    def sentencia_clase(self, p):
        self.errores_sintacticos.append(f"Línea {p.lineno}: Error Sintáctico: Falta ';' al final de la clase.")
        return ('CLASE', p.ID, p.cuerpo_clase)

    @_('CLASS ID IMPORT FROM lista_variables BEGIN cuerpo_clase END ";"')
    def sentencia_clase (self,p):
        self.estructuras_detectadas.append(f"En linea {p.lineno}: CLASE {p.ID}")
        return ('CLASE_IMPORT', 
                p.ID, 
                p.lista_variables ,
                p.cuerpo_clase)

    @_('CLASS ID IMPORT FROM lista_variables BEGIN cuerpo_clase END error')
    def sentencia_clase(self, p):
        self.errores_sintacticos.append(f"Línea {p.lineno}: Error Sintáctico: Falta ';' al final de la clase.")
        return ('CLASE_IMPORT', p.ID, p.lista_variables, p.cuerpo_clase)
    
    #Cuerpo de la clase
    @_('declaracion_clase')
    def cuerpo_clase(self, p):
        return [p.declaracion_clase]

    @_('cuerpo_clase declaracion_clase')
    def cuerpo_clase(self, p):
        p.cuerpo_clase.append(p.declaracion_clase)
        return p.cuerpo_clase
    #declaraciones de la clase
    @_('atributo_clase')
    def declaracion_clase(self, p):
        return p.atributo_clase

    @_('metodo_clase')
    def declaracion_clase(self, p):
        return p.metodo_clase

    @_('sentencia_extends')
    def declaracion_clase(self, p):
        return p.sentencia_extends

    #atributos de clase
    @_('tipo ID ";"')
    def atributo_clase(self, p):
        return ('ATRIBUTO',
                p.tipo,
                p.ID)

    @_('tipo ID error')
    def atributo_clase(self, p):
        self.errores_sintacticos.append(f"Línea {p.lineno}: Error Sintáctico: Falta ';' al final del atributo.")
        return ('ATRIBUTO', p.tipo, p.ID)

    @_('tipo ID EXPORT TO lista_variables ";"')
    def atributo_clase(self, p):

        return (
            'ATRIBUTO_EXPORT',
            p.tipo,
            p.ID,
            p.lista_variables
        )

    @_('tipo ID EXPORT TO lista_variables error')
    def atributo_clase(self, p):
        self.errores_sintacticos.append(
            f"Línea {p.lineno}: Error Sintáctico: Falta ';' al final del atributo exportado."
        )
        return ('ATRIBUTO_EXPORT', p.tipo, p.ID, p.lista_variables)
    
    #metodos
    @_('tipo ID "(" parametros_formales ")" bloque_delimitado ";"')
    def metodo_clase (self, p):
        self.estructuras_detectadas.append(f"En linea: {p.lineno}. Metodo '{p.ID}'")
        return(
            'METODO',
            p.tipo,
            p.ID,
            p.parametros_formales,
            p.bloque_delimitado
        )

    @_('tipo ID "(" parametros_formales ")" bloque_delimitado error')
    def metodo_clase(self, p):
        self.errores_sintacticos.append(
            f"Línea {p.lineno}: Error Sintáctico: Falta ';' al final del método."
        )
        return ('METODO', p.tipo, p.ID, p.parametros_formales, p.bloque_delimitado)

    @_('tipo ID "(" parametros_formales ")" bloque_delimitado EXPORT TO lista_variables ";"')
    def metodo_clase(self, p):

        self.estructuras_detectadas.append(f"En linea: {p.lineno} Metodo exportado '{p.ID}'")
        return (
            'METODO_EXPORT',
            p.tipo,
            p.ID,
            p.parametros_formales,
            p.bloque_delimitado,
            p.lista_variables
        )

    @_('tipo ID "(" parametros_formales ")" bloque_delimitado EXPORT TO lista_variables error')
    def metodo_clase(self, p):
        self.errores_sintacticos.append(
            f"Línea {p.lineno}: Error Sintáctico: Falta ';' al final del método exportado."
        )
        return (
            'METODO_EXPORT',
            p.tipo,
            p.ID,
            p.parametros_formales,
            p.bloque_delimitado,
            p.lista_variables
        )
    
    @_('EXTENDS lista_variables ";"')
    def sentencia_extends(self, p):
        self.estructuras_detectadas.append(f"En linea: {p.lineno}EXTENDS {p.lista_variables}")
        return ('EXTENDS',p.lista_variables)

    @_('EXTENDS lista_variables error')
    def sentencia_extends(self, p):
        self.errores_sintacticos.append(
            f"Línea {p.lineno}: Error Sintáctico: Falta ';' al final de EXTENDS."
        )
        return ('EXTENDS', p.lista_variables)
  #Convercion explicita
    @_('TOSF "(" expresion ")"')
    def sentencia_conv(self, p):
        self.estructuras_detectadas.append(
            f"En linea:{p.lineno}, conversion TOSF"
        )
        return (
            'TOSF',
            p.expresion
        )

    #errores
    def error(self, p):

        if p:
            tokens_de_recuperacion = {
                'BEGIN', 'END', 'IF', 'ELSE', 'END_IF', 'REPEAT', 'UNTIL',
                'RET', 'TOSF', 'POUT', 'ID', 'LONGINT', 'SINGLEF',
                'TYPEDEF', 'CLASS', 'EXTENDS', '('
            }
            if p.type in tokens_de_recuperacion:
                return

            mensaje = (
                f"Línea {p.lineno}: Error sintáctico. "
                f"Token inesperado '{p.type}' "
                f"con valor '{p.value}'."
            )
            self.errores_sintacticos.append(mensaje)

            linea_error = p.lineno
            siguiente_token = next(self.tokens, None)
            while siguiente_token and siguiente_token.lineno == linea_error:
                siguiente_token = next(self.tokens, None)

            self.errok()
            if siguiente_token:
                return siguiente_token
        else:
            mensaje = (
                "Error sintáctico: "
                "fin de archivo inesperado."
            )
            self.errores_sintacticos.append(mensaje)

    #errores Sintacticos
    # Falta de nombre de programa
    @_('sentencias_declarativas bloque_delimitado')
    def programa(self, p):
        self.errores_sintacticos.append(f"Línea {p.lineno}: Error Sintáctico: Falta el nombre del programa al inicio.")
        return ('PROGRAMA', None, p.sentencias_declarativas, p.bloque_delimitado)

    #Falta de delimitador de sentencias ejecutables (begin o end).
    #para esto tenemos que hacer un cambio grande que es generando la regla para agrupar por begin end
    @_('BEGIN sentencias_ejecutables END')
    def bloque_delimitado(self, p):
        return p.sentencias_ejecutables

    #Falta de begin en bloque
    @_('sentencias_ejecutables END')
    def bloque_delimitado(self, p):
        self.errores_sintacticos.append(f"Línea {p.lineno}: Error Sintáctico: Falta el delimitador 'BEGIN'.")
        return p.sentencias_ejecutables

    @_('BEGIN sentencias_ejecutables')
    def bloque_delimitado(self, p):
            self.errores_sintacticos.append(f"Línea {p.lineno}: Error Sintáctico: Falta el delimitador 'END'.")
            return p.sentencias_ejecutables

   