from sly import Lexer
import sys

class Analizador(Lexer):
    tokens = {ID,
              LARGEINT,
              SINGLEF,
              STRINGM,
              SCOMENT,
              NUMERO,
              ASIGN,
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
              DIV
              }
    ignore = ' \t'
    def error(self, t):
        # 1. Informar el error léxico con la línea y el símbolo que falló
        print(f"Error Léxico (Línea {self.lineno}): Carácter inválido '{t.value[0]}' inesperado.")
        
        # 2. Recuperación (Modo pánico): avanzar el índice para descartar el carácter y continuar
        self.index += 1

    @_(r'\d*\.\d+s(?:[+-](?!\d)|(?![+-]|\d))')
    def SINGLEF_EXP_ERROR(self, t):
        print(f"Error Léxico (Línea {self.lineno}): Constante flotante mal formada '{t.value}'. Faltan dígitos en el exponente.")
        return None
    
    ignore_espacios = ' \t' # Ignorar espacios y tabs
    ignore_comentarios = r'//.*'  # Ignorar comentarios de una línea

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
   

    
    @_(r'\d*\.\d+(?:s[+-]?\d+)?')
    def SINGLEF(self, t):
        # La parte exponencial puede estar ausente, pero el '.' y los decimales son obligatorios.
        # Reemplazamos la 's' por 'e' para que Python pueda evaluarlo matemáticamente
        val_str = t.value.replace('s', 'e')
        valor = float(val_str)
        
        # Considerar el rango para 32 bits
        limite_inf = 1.17549435e-38
        limite_sup = 3.40282347e+38
        
        if valor != 0.0 and (valor < limite_inf or valor > limite_sup):
            print(f"Error Léxico (Línea {self.lineno}): Constante flotante '{t.value}' fuera de rango permitdo.")
            t.value = 0.0 # Valor por defecto para recuperación de errores
            
        return t
    # Manejo de errores léxicos para constantes flotantes mal formadas, Preguntar
    # si esta bien que descarte el token y siga o como cortamos la ejecución
    @_(r'\d+\.(?:s[+-]?\d+)?')
    def SINGLEF_ERROR(self, t):
        # Según el TP, la parte decimal es obligatoria[cite: 1, 4]
        # Si entra acá, es porque se escribió "12." o "12.s-5" en lugar de "12.0"
        print(f"Error Léxico (Línea {self.lineno}): Constante flotante mal formada '{t.value}'. La parte decimal es obligatoria.")
        
        # Como es un error léxico, aplicamos "Modo pánico" descartando el token[cite: 3, 5]
        return None


    @_(r'\d+\$l')
    def LARGEINT(self, t):
        val_str = t.value[:-2]
        t.value = int(val_str)
        # Considerar el rango para 32 bits
    
        limite_sup = 2147483647
        #Aca no sabemos si tirar warning o error
        if t.value > limite_sup:
            print(f"Error Léxico en Línea {self.lineno}: Constante entera fuera del rango permitido")
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
            print(f"Warning: Identificador '{t.value}' excede el límite de 22 caracteres.")
            print(f"Truncando a: '{t.value[:22]}'")
            t.value = t.value[:22]  # Truncar a 22 caracteres

        # hacemos los casos especiales de las palabras reservadas
        palabras_reservadas = {
            'if': 'IF', 'IF': 'IF',
            #ponemos las 3 variantes
            'end_if': 'END_IF', 'END_IF': 'END_IF','END_if': 'END_IF',
            'else': 'ELSE', 'ELSE': 'ELSE',
            'begin': 'BEGIN', 'BEGIN': 'BEGIN',
            'end': 'END', 'END': 'END',
            'pout': 'POUT', 'POUT': 'POUT',
            'ret': 'RET', 'RET': 'RET',
            'class': 'CLASS', 'CLASS': 'CLASS',
            'function': 'FUNCTION', 'FUNCTION': 'FUNCTION',
            'singlef': 'SINGLEF', 'SINGLEF': 'SINGLEF'
        }
        if t.value in palabras_reservadas:
            t.type = palabras_reservadas[t.value]
            return t
        # Preguntar a los profes si para manejar que las palabras reservadas sean escritas solo con mayuscula o minuscula
        # y si se intercalan las puedo descartar
        if any(c.isupper() for c in t.value):
            print(f"Error Léxico (Línea {self.lineno}): Identificador '{t.value}' no puede tener mayúsculas.")
            return None
        return t
    literals = { '(', ')', ';',',' }
    MAYORIGUAL = r'>='
    MENORIGUAL = r'<='
    IGUAL      = r'=='
    DIFERENTE  = r'!='
    MAYOR      = r'>'
    MENOR      = r'<'
    ASIGN      = r':=|='
    MENOS      = r'-'
    MAS        = r'\+'
    MULT       = r'\*'
    DIV        = r'/'



if __name__ == '__main__':
    # 1. Verificamos que el usuario haya enviado el parámetro desde la consola
    if len(sys.argv) < 2:
        print("Error: Falta especificar el archivo de código fuente.")
        print("Uso correcto: python Analizador.py <nombre_del_archivo>")
        sys.exit(1)

    # 2. Capturamos la ruta que el usuario eligió y pasó como parámetro
    ruta_archivo = sys.argv[1]

    # 3. Leemos el archivo
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            data = archivo.read()
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{ruta_archivo}'.")
        sys.exit(1)

    # 4. Inicializamos el analizador e imprimimos los tokens detectados
    lexer = Analizador()
    print(f"--- Iniciando Análisis Léxico para: {ruta_archivo} ---\n")
    
    for tok in lexer.tokenize(data):
        print(tok)