from sly import Lexer


class Analizador(Lexer):
    tokens = {ID,
              LARGEINT,
              FLOAT,
              STRINGM,
              SCOMENT,
              CONST,
              LITERALES,
              ASIGN,
              MAYOR,
              MENOR,
              MAYORIGUAL,
              MENORIGUAL,
              IGUAL,
              DIFERENTE,
              LPARENT,
              RPARENT,
              COMA,
              PUNTOYCOMA,
              IF,
              END_IF,
              ELSE,
              END,
              POUT,
              RET,
              CLASS,
              FUNCTION
              }
    ignore = ' \t'
    @_(r'[a-z][a-z0-9_]*')
    def ID(self, t):
        if len(t.value) > 22:
            print(f"Warning: Identificador '{t.value}' excede el límite de 22 caracteres.")
            print(f"Truncando a: '{t.value[:22]}'")
            t.value = t.value[:22]  # Truncar a 22 caracteres
        """
        if t.value.contains(upper()):
            print(f"Warning: Identificador '{t.value}' contiene letras mayúsculas.")
            t.value = t.value.lower()  # Convertir a minúsculas
        """
         #Con esta parte 