from sly import Lexer
import sys

class Lexico(Lexer):
    tokens = {ID,
              LONGINT,
              NUMBER,
              SINGLEF,
              FLOAT,
              STRINGM,
              SCOMENT,
              ASIGN,
              ASIGN_IGUAL,
              MAYOR,
              MENOR,
              MAYORIGUAL,
              MENORIGUAL,
              IGUAL,
              DIFERENTE,
              IF,
              END_IF,
              ELSE,
              END,
              POUT,
              RET,
              CLASS,
              FUNCTION,
              BEGIN,
              MAS,
              MENOS,
              MULT,
              DIV,
              REPEAT,
              UNTIL,
              TYPEDEF,
              IMPORT,FROM,EXPORT,TO,
              TOSF,
              EXTENDS
              }
    def __init__(self):
        self.errores_lexicos = []
        self.tabla_simbolos = {} # Se recomienda una estructura dinámica como diccionario
    def error(self, t):
        # 1. Informar el error léxico con la línea y el símbolo que falló
        self.errores_lexicos.append(f"Línea {t.lineno}: Error léxico: Carácter inválido '{t.value[0]}'")
        # 2. Recuperación (Modo pánico): avanzar el índice para descartar el carácter y continuar
        self.index += 1

    @_(r'\d*\.\d+s(?:[+-](?!\d)|(?![+-]|\d))')
    def SINGLEF_EXP_ERROR(self, t):
        self.errores_lexicos.append(f"Línea {self.lineno}: Error léxico: Constante flotante mal formada '{t.value}'. Faltan dígitos en el exponente.")
        return None
    ignore = ' \t' # Ignorar espacios y tabs
    ignore_comentarios = r'//.*'  # Ignorar comentarios de una línea

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
   

    
    @_(r'\d*\.\d+(?:s[+-]?\d+)?')
    def FLOAT(self, t):
        # La parte exponencial puede estar ausente, pero el '.' y los decimales son obligatorios.
        # Reemplazamos la 's' por 'e' para que Python pueda evaluarlo matemáticamente
        val_str = t.value.replace('s', 'e')
        valor = float(val_str)
        
        # Considerar el rango para 32 bits
        limite_inf = 1.17549435e-38
        limite_sup = 3.40282347e+38
        
        if valor != 0.0 and (valor < limite_inf or valor > limite_sup):
            self.errores_lexicos.append(f"Línea {self.lineno}: Error léxico: Constante flotante '{t.value}' fuera de rango permitdo.")
            t.value = 0.0 # Valor por defecto para recuperación de errores
            
        return t

    @_(r'\d+\.(?:s[+-]?\d+)?')
    def SINGLEF_ERROR(self, t):
        #la parte decimal es obligatoria
        # Si entra acá, es porque se escribió "12." o "12.s-5" en lugar de "12.0"
        self.errores_lexicos.append(f"Línea {self.lineno}: Error léxico: Constante flotante mal formada '{t.value}'. La parte decimal es obligatoria.")
        # Como es un error léxico, aplicamos "Modo pánico" descartando el token
        return None


    @_(r'\d+\$l')
    def NUMBER(self, t):
        val_str = t.value[:-2]
        t.value = int(val_str)
        # Considerar el rango para 32 bits
    
        limite = 2147483647
        #Aca no sabemos si tirar warning o error
        if t.value > limite:
            self.errores_lexicos.append(f"Línea {self.lineno}: Error léxico: Constante entera fuera del rango permitido")
            return None
        return t

    @_(r'\"[^\"]*\"')
    def STRINGM(self, t):
        # Eliminamos las comillas dobles al inicio y al final
        t.value = t.value[1:-1]
        # como tenemos varias lineas tenemos que seguir contando las lineas
        t.lineno += t.value.count('\n')
        #Como se guarda sin saltos de linea remplazamos los saltos de linea por espacios
        t.value = t.value.replace('\n', ' ')
        return t

    @_(r'[a-zA-Z][a-zA-Z0-9_]*')
    def ID(self, t):
        if len(t.value) > 22:
            self.errores_lexicos.append(f"Línea {self.lineno}: Warning: Identificador '{t.value}' excede el límite de 22 caracteres.")
            t.value = t.value[:22]  # Truncar a 22 caracteres

        # hacemos los casos especiales de las palabras reservadas
        palabras_reservadas = {
            'IF': 'IF',
            'END_IF': 'END_IF',
            'ELSE': 'ELSE',
            'BEGIN': 'BEGIN',
            'END': 'END',
            'POUT': 'POUT',
            'RET': 'RET',
            'CLASS': 'CLASS',
            'FUNCTION': 'FUNCTION',
            'SINGLEF': 'SINGLEF',
            'REPEAT': 'REPEAT',
            'UNTIL': 'UNTIL',
            'TYPEDEF': 'TYPEDEF',
            'IMPORT': 'IMPORT',
            'FROM': 'FROM',
            'EXPORT': 'EXPORT',
            'TO': 'TO',
            'TOSF': 'TOSF',
            'LONGINT': 'LONGINT',
            'EXTENDS': 'EXTENDS'
        }
        if t.value.upper() in palabras_reservadas:
            t.type = palabras_reservadas[t.value.upper()]
            return t
        if any(c.isupper() for c in t.value):
            self.errores_lexicos.append(f"Línea {self.lineno}: Error léxico: Identificador '{t.value}' no puede tener mayúsculas.")
            return None
        return t
    literals = { '(', ')', ';',',','[',']' }
    MAYORIGUAL  = r'>='
    MENORIGUAL  = r'<='
    IGUAL       = r'=='
    DIFERENTE   = r'!='
    MAYOR       = r'>'
    MENOR       = r'<'
    ASIGN       = r':='
    ASIGN_IGUAL = r'='
    MENOS       = r'-'
    MAS         = r'\+'
    MULT        = r'\*'
    DIV         = r'/'

    