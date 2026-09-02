from sly import Lexer


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
              MENOS
              }
    ignore = ' \t'
    @_(r'[a-z][a-z0-9_]*')
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
        
        return t
         #Con esta parte 
    
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







if __name__ == '__main__':
    data = '''
    // comentario de prueba
    x = singlef 3.14;
    if (x >= singlef 10.00)
    if (x > 200$l)
        begin
            x = x - 1$l;
            x = x + 1$l;
            pout("x es igual a 10");
        end
    letras = 
    "Hola mina xd
Sos re trola";
    '''
    for tok in Analizador().tokenize(data):
        print(tok)