import Lexico
import Sintactico
import sys

lexer = Lexico.Lexico()
sintax = Sintactico.Sintactico()

# 1. Verificamos que el usuario haya enviado el parámetro desde la consola
if len(sys.argv) < 2:
    print("Error: Falta especificar el archivo de código fuente.")
    print("Uso correcto: python Lexico.py <nombre_del_archivo>")
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



resultado =sintax.parse(lexer.tokenize(data))

print("Análisis finalizado.")