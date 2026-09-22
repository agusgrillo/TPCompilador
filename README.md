# TPCompilador

Trabajo Práctico de **Compiladores**.

Este proyecto implementa un analizador léxico y sintáctico utilizando **Python** y la librería **SLY**.

## Requisitos

Para ejecutar el proyecto es necesario tener instalado:

* Python 3

* Git

Se puede comprobar la instalación de Python ejecutando:

```
python --version
```

En Linux/macOS puede ser necesario utilizar: `python3 --version`

## Instalación

### 1. Clonar el repositorio

Primero, clonar el repositorio:

```
git clone https://github.com/agusgrillo/TPCompilador.git
cd TPCompilador
```

### 2. Crear el entorno virtual

Para evitar conflictos entre las dependencias del proyecto y las instaladas globalmente, se recomienda utilizar un entorno virtual. El entorno debe llamarse **`entornoCompi`** (está ignorado en `.gitignore`).

* **Windows:** `python -m venv entornoCompi`

* **Linux / macOS:** `python3 -m venv entornoCompi`

### 3. Activar el entorno virtual

* **Windows - CMD:** `entornoCompi\Scripts\activate`

* **Windows - PowerShell:** `entornoCompi\Scripts\Activate.ps1`

* **Linux / macOS:** `source entornoCompi/bin/activate`

Si se activó correctamente, aparecerá `(entornoCompi)` al comienzo de la línea de comandos.

### 4. Instalar las dependencias

Con el entorno virtual activado, ejecutar:

```
pip install -r requirements.txt
```

## Ejecución

El analizador recibe como argumento por consola el archivo que contiene el **código fuente a analizar**.

La sintaxis para ejecutar el programa es:

```
python main.py <archivo_fuente>
```

Por ejemplo:

```
python main.py codigo.txt
```

*(En Linux o macOS utilizar `python3 main.py codigo.txt`)*

## Ejemplo completo (Windows)

```
git clone https://github.com/agusgrillo/TPCompilador.git
cd TPCompilador
python -m venv entornoCompi
entornoCompi\Scripts\activate
pip install -r requirements.txt
python main.py codigo.txt
```

## Características del Lenguaje

El compilador soporta un lenguaje fuertemente tipado con las siguientes características:

* **Tipos de datos:** Enteros (`LONGINT` con sufijo `$l`), Flotantes (`SINGLEF` con `s`), Cadenas de texto.

* **Control de flujo:** `IF - ELSE - END_IF`, ciclos `REPEAT - UNTIL`.

* **Estructuras complejas:** Funciones (`FUNCTION`), Clases (`CLASS`) con herencia (`EXTENDS`), importación/exportación de métodos/atributos (`IMPORT`, `EXPORT`).

* **Tipos definidos por usuario:** Enumeraciones con `TYPEDEF`.

* **Salida estándar:** `POUT`.

**Ejemplo de código fuente (`codigo.txt`):**

```
programa_ejemplo

// Ejemplo de código fuente
LONGINT mivariable;

BEGIN

mivariable := 10$l;

    IF (mivariable > 5$l)
        POUT("La variable es mayor a 5");
    END_IF;

END
```

## Salida del Compilador

Al ejecutar `main.py`, el sistema procesará el archivo y generará un reporte completo por consola dividido en 4 secciones:

1. **TOKENS DETECTADOS:** Lista ordenada de todos los componentes léxicos válidos encontrados.

2. **ESTRUCTURAS SINTÁCTICAS:** Detalle de las construcciones reconocidas por el parser (asignaciones, declaraciones, bloques IF, etc.).

3. **ERRORES Y WARNINGS:** Listado unificado de errores léxicos (caracteres inválidos, fuera de rango) y sintácticos (falta de punto y coma, tipos incompatibles, falta de operandos).

4. **TABLA DE SÍMBOLOS:** Estado final de todas las variables, funciones y clases detectadas, junto con sus tipos y valores.

## Estructura del proyecto

```
TPCompilador/
│
├── main.py                # Punto de entrada y generador del reporte
├── Lexico.py              # Analizador Léxico (SLY)
├── Sintactico.py          # Analizador Sintáctico (SLY)
├── requirements.txt       # Dependencias (sly)
├── README.md              # Documentación
├── caso_prueba_error.txt  # Ejemplo codigo con errores
├── caso_prueba_exito.txt  # Ejemplo codigo sin errores
└── .gitignore             # Archivos ignorados por Git
```
