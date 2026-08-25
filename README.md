# Workflow Manager

## Bitácora de Inteligencia Artificial

Durante el desarrollo del proyecto **Workflow Manager** se utilizó ChatGPT como herramienta de apoyo para comprender, revisar, organizar y comentar algunas partes del código desarrollado en Python.

El código generado con apoyo de la herramienta fue revisado y probado antes de incorporarlo al proyecto.

---

### 1. Algoritmos de ordenamiento

**Archivo trabajado:** `Ordenamientos.py`

**Herramienta utilizada:** ChatGPT

**Prompt utilizado:**

> "Necesito ayuda para realizar los algoritmos de ordenamiento Burbuja, Merge Sort y Quick Sort en Python de una manera sencilla y con comentarios que expliquen el código."

**Uso de la IA:**

Se utilizó ChatGPT como apoyo para estructurar los métodos de ordenamiento y agregar comentarios que permitieran comprender el funcionamiento de cada parte del código.

También se utilizó para realizar ajustes posteriores de acuerdo con las aclaraciones dadas para el proyecto.

**Revisión humana:**

Se revisó el código generado, se ejecutaron los métodos desde Visual Studio y se corrigieron problemas encontrados durante las pruebas, incluyendo errores de indentación.

---

### 2. Lectura y escritura de archivos CSV

**Archivo trabajado:** `CSVManager.py`

**Herramienta utilizada:** ChatGPT

**Prompt utilizado:**

> "Necesito ayuda para crear la lectura y escritura de archivos CSV en Python de una manera sencilla y completamente comentada."

**Uso de la IA:**

Se utilizó ChatGPT para comprender cómo utilizar la librería `csv` de Python y desarrollar funciones para guardar y recuperar la información utilizada por el sistema.

**Revisión humana:**

Se revisó el funcionamiento del código y se realizaron pruebas para comprobar que los archivos CSV pudieran ser creados, guardados y posteriormente leídos por el programa.

---

### 3. Menú principal

**Archivo trabajado:** `Program.py`

**Herramienta utilizada:** ChatGPT

**Prompt utilizado:**

> "Necesito ayuda para crear el menú principal del Workflow Manager en Python y dejar preparadas las opciones para después integrar los módulos realizados por los demás integrantes."

**Uso de la IA:**

ChatGPT se utilizó como apoyo para organizar las diferentes opciones del menú principal y los submenús correspondientes a usuarios, tareas y algoritmos de ordenamiento.

Las partes desarrolladas por otros integrantes se dejaron preparadas para su posterior integración sin modificar sus módulos.

**Revisión humana:**

Se ejecutó el programa y se probaron las diferentes opciones del menú para verificar que permitieran entrar, regresar y continuar utilizando el sistema correctamente.

---

### 4. Manejo de errores

**Archivo trabajado:** `Program.py`

**Herramienta utilizada:** ChatGPT

**Prompt utilizado:**

> "Necesito agregar un manejo de errores sencillo para que el programa no se cierre cuando el usuario ingrese una opción incorrecta."

**Uso de la IA:**

Se utilizó ChatGPT para agregar validaciones sencillas a las entradas del usuario y manejo de excepciones en operaciones que podrían producir errores.

**Revisión humana:**

Se realizaron pruebas ingresando opciones válidas e inválidas para comprobar que el programa mostrara un mensaje de error y continuara funcionando en lugar de cerrarse inesperadamente.

---

### 5. Auditoría del sistema

**Archivo trabajado:** `CSVManager.py`

**Herramienta utilizada:** ChatGPT

**Prompt utilizado:**

> "Necesito agregar al proyecto un archivo auditoria_log.csv que registre nuevas acciones sin borrar los registros anteriores."

**Uso de la IA:**

ChatGPT se utilizó como apoyo para implementar una función que permita registrar la fecha y hora, el usuario, la acción realizada y la tarea afectada.

Se utilizó el modo de agregado del archivo para conservar los registros anteriores.

**Revisión humana:**

Se revisó que la implementación cumpliera con la aclaratoria del proyecto y que los nuevos registros fueran agregados sin reemplazar la información existente.

---

## Validación del uso de IA

La Inteligencia Artificial fue utilizada como una herramienta de apoyo durante el desarrollo. Las sugerencias obtenidas fueron revisadas antes de ser incorporadas al proyecto y se realizaron pruebas manuales para comprobar el funcionamiento del código.

También se realizaron modificaciones cuando fue necesario para adaptar el código a los requerimientos y aclaraciones proporcionados durante el desarrollo del proyecto.

### 6. Configuración de Git y archivo .gitignore

**Archivo trabajado:** `.gitignore`

**Herramientas utilizadas:** ChatGPT y GitHub Desktop

**Prompt utilizado:**

> "Estoy teniendo problemas con GitHub y el archivo .gitignore de mi proyecto en Python. Necesito ayuda para configurarlo correctamente y entender qué archivos deben subirse al repositorio."

**Problema presentado:**

Durante la configuración del repositorio se presentaron inconvenientes relacionados con el archivo `.gitignore` y los archivos que debían ser controlados por Git. También fue necesario comprender cómo trabajar correctamente desde una rama propia utilizando GitHub Desktop sin afectar directamente la rama principal del proyecto.

**Uso de la IA:**

Se utilizó ChatGPT como apoyo para comprender la función del archivo `.gitignore`, revisar la organización del proyecto y entender el proceso de trabajo mediante ramas, commits y GitHub Desktop.

**Revisión humana:**

Después de realizar los ajustes, se verificó desde GitHub Desktop cuáles archivos estaban siendo detectados como cambios antes de realizar los commits. También se comprobó que el trabajo se estuviera realizando desde la rama correspondiente y no directamente sobre `main`.
