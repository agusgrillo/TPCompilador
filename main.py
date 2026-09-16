import Lexico
import Sintactico
import sys

if __name__ == '__main__':
    # 1. Verificamos que el usuario haya enviado el parámetro desde la consola
    if len(sys.argv) < 2:
        print("Error: Falta especificar el archivo de código fuente.")
        print("Uso correcto: python main.py <nombre_del_archivo>")
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

    lexer = Lexico.Lexico()
    sintax = Sintactico.Sintactico()

    # 4. Analizar léxicamente y guardar los tokens en una lista para no consumirlos[cite: 13]
    lista_tokens = list(lexer.tokenize(data))

    # 5. Ejecutar el análisis sintáctico pasándole el iterador de los tokens[cite: 13]
    sintax.parse(iter(lista_tokens))

    # ==========================================
    # GENERACIÓN DEL REPORTE DE SALIDA (Requisitos del TP)
    # ==========================================
    print("\n" + "="*50)
    print(" SALIDA DEL COMPILADOR ".center(50, "="))
    print("="*50 + "\n")

    # A) Tokens detectados en orden[cite: 12, 13]
    print("1) TOKENS DETECTADOS:")
    for tok in lista_tokens:
        print(tok)

    print("\n" + "-"*50 + "\n")

    # B) Estructuras sintácticas detectadas[cite: 12, 13]
    print("2) ESTRUCTURAS SINTÁCTICAS:")
    if len(sintax.estructuras_detectadas) == 0:
        print("No se detectaron estructuras.")
    else:
        for est in sintax.estructuras_detectadas:
            print(est)

    print("\n" + "-"*50 + "\n")

    # C) Errores y Warnings (Léxicos y Sintácticos)[cite: 12, 13]
    print("3) ERRORES Y WARNINGS:")
    todos_los_errores = lexer.errores_lexicos + sintax.errores_sintacticos
    
    if len(todos_los_errores) == 0:
        print("Compilación exitosa. No se encontraron errores.")
    else:
        for error in todos_los_errores:
            print(error)

    print("\n" + "-"*50 + "\n")

    # D) Contenido de la Tabla de Símbolos[cite: 12, 13]
    print("4) TABLA DE SÍMBOLOS:")
    if len(sintax.tabla_de_simbolos) == 0:
        print("La tabla de símbolos está vacía.")
    else:
        for clave, atributos in sintax.tabla_de_simbolos.items():
            print(f"ID: {clave} -> {atributos}")
            
    print("\n" + "="*50)
    print(" Análisis finalizado ".center(50, "="))
    print("="*50 + "\n")