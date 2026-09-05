# TPCompilador

Trabajo Práctico de **Compiladores**.

Este proyecto implementa un analizador léxico utilizando **Python** y la librería **SLY (Sly Lex Yacc)**.

## Requisitos

Para ejecutar el proyecto es necesario tener instalado:

* [Python 3](https://www.python.org/)
* Git

Se puede comprobar la instalación de Python ejecutando:

```bash
python --version
```

En Linux/macOS puede ser necesario utilizar:

```bash
python3 --version
```

---

## Instalación

### 1. Clonar el repositorio

Primero, clonar el repositorio:

```bash
git clone https://github.com/agusgrillo/TPCompilador.git
```

Luego, ingresar a la carpeta del proyecto:

```bash
cd TPCompilador
```

### 2. Crear el entorno virtual

Para evitar conflictos entre las dependencias del proyecto y las instaladas globalmente en el sistema, se recomienda utilizar un entorno virtual.

El entorno virtual debe crearse con el nombre **`entornoCompi`**, ya que esta carpeta se encuentra incluida en el `.gitignore` del proyecto.

#### Windows

```bash
python -m venv entornoCompi
```

#### Linux / macOS

```bash
python3 -m venv entornoCompi
```

Esto creará una carpeta llamada `entornoCompi` dentro del proyecto.

### 3. Activar el entorno virtual

Una vez creado, se debe activar el entorno virtual.

#### Windows - CMD

```bash
entornoCompi\Scripts\activate
```

#### Windows - PowerShell

```powershell
entornoCompi\Scripts\Activate.ps1
```

#### Linux / macOS

```bash
source entornoCompi/bin/activate
```

Si se activó correctamente, aparecerá `(entornoCompi)` al comienzo de la línea de comandos.

Por ejemplo:

```text
(entornoCompi) C:\...\TPCompilador>
```

### 4. Instalar las dependencias

Con el entorno virtual activado, ejecutar:

```bash
pip install -r requirements.txt
```

Esto instalará automáticamente las dependencias necesarias para ejecutar el proyecto, incluyendo **SLY**.

---

## Ejecución

El analizador recibe como argumento por consola el archivo que contiene el **código fuente a analizar**.

La sintaxis para ejecutar el programa es:

```bash
python Analizador.py <archivo_fuente>
```

Por ejemplo, si el código fuente se encuentra en un archivo llamado `codigo.txt`:

```bash
python Analizador.py codigo.txt
```

También se puede indicar la ruta al archivo:

```bash
python Analizador.py ejemplos/codigo.txt
```

### Linux / macOS

En Linux o macOS puede ser necesario utilizar `python3`:

```bash
python3 Analizador.py codigo.txt
```

---

## Ejemplo completo

A continuación se muestra el proceso completo desde cero.

### Windows

```bash
git clone https://github.com/agusgrillo/TPCompilador.git

cd TPCompilador

python -m venv entornoCompi

entornoCompi\Scripts\activate

pip install -r requirements.txt

python Analizador.py codigo.txt
```

### Linux / macOS

```bash
git clone https://github.com/agusgrillo/TPCompilador.git

cd TPCompilador

python3 -m venv entornoCompi

source entornoCompi/bin/activate

pip install -r requirements.txt

python3 Analizador.py codigo.txt
```

---

## Código fuente

El archivo que se pasa como argumento debe contener el código escrito en el lenguaje definido para el compilador.

Por ejemplo:

```text
codigo.txt
```

Luego se ejecuta:

```bash
python Analizador.py codigo.txt
```

El analizador procesará el contenido del archivo y mostrará los tokens generados y/o los errores detectados.

---

## Desactivar el entorno virtual

Cuando se termine de trabajar con el proyecto, se puede desactivar el entorno virtual ejecutando:

```bash
deactivate
```

Para volver a trabajar en el proyecto posteriormente, solamente es necesario ingresar a la carpeta del proyecto y volver a activar el entorno virtual.

### Windows

```bash
entornoCompi\Scripts\activate
```

### Linux / macOS

```bash
source entornoCompi/bin/activate
```

---

## Estructura del proyecto

```text
TPCompilador/
│
├── Analizador.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Archivos principales

* **`Analizador.py`**: contiene la implementación del analizador.
* **`requirements.txt`**: contiene las dependencias necesarias para ejecutar el proyecto.
* **`README.md`**: contiene la documentación e instrucciones de instalación y ejecución.
* **`.gitignore`**: especifica archivos y carpetas que no deben ser incluidos en el repositorio.

> **Nota:** La carpeta `entornoCompi/` se genera localmente al crear el entorno virtual y está incluida en el `.gitignore`, por lo que no debe subirse al repositorio.
