Sistema Gestor de Flujos de Trabajo | Proyecto de Investigación Aplicada #1

Sistema Gestor de Flujos de Trabajo (Workflow Manager) desarrollado para el curso de Estructuras de Datos.

El proyecto simula la administración, priorización y ejecución de procesos dentro de una organización mediante diferentes estructuras de datos implementadas desde cero.

1. Objetivo
Desarrollar un sistema capaz de administrar usuarios y tareas, controlar permisos según roles, gestionar diferentes tipos de colas, representar dependencias mediante árboles, mantener un historial de acciones con Undo/Redo y almacenar la información de manera persistente mediante archivos CSV.

2. Tecnologías utilizadas
Python 3
CSV para persistencia de datos
Git
GitHub
Pytest para pruebas unitarias
Estructuras de datos implementadas desde cero

3. Estructura del proyecto
.
├── data/
│   ├── auditoria_log.csv
│   ├── tareas.csv
│   └── usuarios.csv
│
├── models/
│   ├── accion.py
│   ├── prioridad.py
│   ├── tarea.py
│   └── usuario.py
│
├── persistence/
│   ├── tarea_repository.py
│   └── usuario_repository.py
│
├── services/
│   ├── historial_service.py
│   ├── ordenador_tareas.py
│   ├── sistema_service.py
│   ├── tarea_service.py
│   └── usuario_service.py
│
├── structures/
│   ├── arbol_tareas.py
│   ├── cola_fifo.py
│   ├── cola_prioridad.py
│   ├── lista_doble.py
│   ├── nodo_arbol.py
│   ├── nodo_pila.py
│   ├── nodo_usuario.py
│   └── pila.py
│
├── tests/
│   ├── test_completo.py
│   ├── test_global.py
│   ├── test_historial_service.py
│   ├── test_persistencia.py
│   ├── test_tarea_service.py
│   └── test_usuario_service.py
│
└── main.py

4. Funcionalidades
Gestión de usuarios

El sistema permite:
Agregar usuarios.
Modificar usuarios.
Eliminar usuarios.
Listar usuarios.
Buscar usuarios por ID.
Validar IDs duplicados.
Validar nombres.
Validar roles.

Se utilizan dos roles:

Administrador(Tiene acceso completo al sistema).

Puede:
Administrar usuarios.
Administrar tareas.
Asignar responsables.
Modificar tareas.
Eliminar tareas.
Utilizar Undo/Redo.
Consultar la auditoría.

Usuario Normal (Tiene permisos restringidos).

Puede:
Consultar tareas.
Consultar sus tareas asignadas.
Cambiar el estado de las tareas que tiene asignadas.

5. Gestión de tareas

Las tareas contienen información como:

ID.
Descripción.
Prioridad.
Responsable.
Estado.
Tarea padre.
Ciclos de espera para SLA.

El administrador puede:

Crear tareas.
Modificar tareas.
Eliminar tareas.
Buscar tareas.
Listar tareas pendientes.
Asignar responsables.
Crear subtareas.

6. Estructuras de datos
El proyecto implementa las estructuras requeridas por el enunciado.

Lista doblemente enlazada (Se utiliza para almacenar los usuarios).

Permite:
Inserción.
Búsqueda.
Eliminación.
Recorrido.

Archivo principal: structures/lista_doble.py

Pila
Se utiliza para implementar el historial de acciones.

Se mantienen dos pilas:
pila_deshacer
pila_rehacer

Esto permite implementar: Undo y Redo.
Archivo: structures/pila.py

Cola FIFO
Las tareas regulares se gestionan mediante una cola FIFO.
Las tareas se procesan respetando el orden de llegada.

Archivo: structures/cola_fifo.py

Cola de prioridad
Las tareas urgentes utilizan una cola de prioridad.
Las tareas con mayor prioridad son procesadas antes que las tareas de menor prioridad.

Archivo: structures/cola_prioridad.py

Árbol de tareas
Las relaciones entre tareas principales y subtareas se representan mediante un árbol.

Ejemplo:

Respaldar Base de Datos
│
├── Comprimir archivos
│
├── Copiar respaldo
│
└── Verificar respaldo

El recorrido del árbol utiliza recursividad.

Archivos relacionados: structures/arbol_tareas.py y structures/nodo_arbol.py

7. Algoritmos de ordenamiento
El sistema incorpora tres algoritmos de ordenamiento:

Bubble Sort.
Merge Sort.
Quick Sort.

Estos algoritmos permiten ordenar las tareas según diferentes criterios.

Complejidad
Algoritmo	Mejor caso	Caso promedio	Peor caso
Bubble Sort	O(n)	O(n²)	O(n²)
Merge Sort	O(n log n)	O(n log n)	O(n log n)
Quick Sort	O(n log n)	O(n log n)	O(n²)

Bubble Sort: Tiene una implementación sencilla, pero presenta un costo cuadrático en los casos promedio y peor.

Merge Sort:
Divide el conjunto de datos en partes y posteriormente las combina ordenadamente. Su complejidad temporal es O(n log n).

Quick Sort:
Utiliza un elemento pivote para dividir el conjunto de datos. Su complejidad promedio es O(n log n), aunque su peor caso puede llegar a O(n²).

8. Persistencia

La información se almacena en archivos CSV.

Archivos utilizados: data/usuarios.csv, data/tareas.csv y data/auditoria_log.csv

La persistencia permite recuperar la información cuando el programa vuelve a ejecutarse. Las operaciones de modificación actualizan los archivos correspondientes.

9. Auditoría
El sistema mantiene una bitácora de auditoría en: data/auditoria_log.csv

La bitácora registra eventos importantes como:
Cambio de estado.
Escalamiento por SLA.
Deshacer.
Rehacer.

El formato utilizado es: Fecha y Hora | ID Usuario | Acción Realizada | ID Tarea

Ejemplo:
2026-08-31 10:30:15 | 1 | CAMBIAR_ESTADO:Completada | 10
2026-08-31 10:31:20 | 1 | ESCALAMIENTO_SLA | 15
2026-08-31 10:32:05 | 1 | DESHACER | 10

La auditoría funciona bajo un modelo append-only: los registros existentes no deben modificarse ni eliminarse.

10. Escalamiento SLA
Para evitar la inanición de tareas regulares, el sistema mantiene un contador de ciclos de espera.
Una tarea regular incrementa su contador cada vez que otra tarea es procesada mientras continúa esperando.

Cuando alcanza el límite definido por el sistema, la tarea:
Es retirada de la cola regular.
Es escalada automáticamente.
Es ingresada a la cola de prioridad.
Se registra el evento en la auditoría.

Esto evita que las tareas regulares permanezcan indefinidamente esperando debido a la existencia de tareas urgentes.

11. Autenticación
El sistema utiliza autenticación mediante: ID de usuario y Contraseña.

Las contraseñas se solicitan mediante el módulo getpass de Python para evitar que sean visibles directamente en la consola.

Ejemplo:
ID de usuario: 1
Contraseña:           (La contraseña no se muestra mientras es introducida).

12. Validaciones
El sistema maneja las entradas inválidas mediante excepciones y validaciones.
Entre las validaciones implementadas se encuentran:
IDs numéricos.
IDs positivos.
IDs únicos.
Nombre obligatorio.
Rol válido.
Prioridad válida.
Estado válido.
Existencia del responsable.
Existencia de tareas padre.
Permisos según el rol.

El sistema evita finalizar abruptamente ante entradas inválidas.

13. Pruebas
Las pruebas automatizadas fueron desarrolladas utilizando pytest.

Para ejecutar todas las pruebas: pytest
Para ejecutar un archivo específico: pytest tests/test_usuario_service.py
Para obtener mayor detalle: pytest -v

Las pruebas cubren:
Gestión de usuarios.
Gestión de tareas.
Validaciones.
Lista doblemente enlazada.
Pila.
Cola FIFO.
Cola de prioridad.
Historial.
Undo/Redo.
Cambio de estados.
Permisos.
Ordenamiento.
Persistencia.
Flujo completo del sistema.

14. Uso de Git y GitHub
El proyecto se desarrolló mediante Git y GitHub utilizando ramas independientes.
El flujo de trabajo utilizado consiste en:

main
 │
 ├── rama de desarrollo
 │
 ├── rama de funcionalidad
 │
 └── Pull Request
          │
          ↓
        revisión
          │
          ↓
         merge

Las funcionalidades se desarrollan en ramas independientes y posteriormente se integran mediante Pull Requests.
Los commits deben utilizar mensajes descriptivos relacionados con los cambios realizados.

Ejemplos:
feat: implementar gestion de usuarios
feat: agregar cola de prioridad
feat: implementar escalamiento SLA
feat: agregar auditoria
test: agregar pruebas de tareas
fix: corregir persistencia CSV

15. Bitácora de Inteligencia Artificial

Durante el desarrollo del proyecto se utilizó Inteligencia Artificial como herramienta de apoyo para análisis, generación de pruebas, detección de errores, revisión de código, refactorización y documentación.

La Inteligencia Artificial no sustituyó el trabajo del equipo. Las respuestas obtenidas fueron revisadas, adaptadas, ejecutadas y verificadas manualmente antes de incorporar cualquier cambio al proyecto.

A continuación se documentan algunos de los principales usos realizados.

Uso de IA #1 — Generación de pruebas unitarias para usuarios

Función trabajada:
Generación de pruebas para: services/usuario_service.py

Objetivo:
Comprobar el funcionamiento de las operaciones principales de gestión de usuarios y sus validaciones.

Prompt utilizado:
"Genera pruebas unitarias en Python utilizando pytest para un servicio de usuarios que permita agregar, modificar, eliminar, buscar y listar usuarios. Incluye pruebas para IDs duplicados, IDs inválidos, nombres vacíos y roles inválidos. El código debe ser sencillo y apropiado para un proyecto universitario de estructuras de datos."

Resultado:
Se generaron pruebas para las operaciones de:
Agregar usuarios.
Buscar usuarios.
Modificar usuarios.
Eliminar usuarios.
Listar usuarios.
Validar IDs duplicados.
Validar IDs inválidos.
Validar nombres vacíos.
Validar roles inválidos.

Validación humana:
El equipo revisó las pruebas generadas y verificó:
Que correspondieran a la implementación real.
Que las excepciones esperadas fueran correctas.
Que los nombres de los métodos coincidieran con el proyecto.
Que las pruebas fueran ejecutables.
Que los casos cubrieran los requisitos del enunciado.

Posteriormente se realizaron ajustes manuales para adaptar las pruebas a las estructuras y servicios utilizados en el proyecto.

Uso de IA #2 — Generación de pruebas para el servicio de tareas

Función trabajada:
Generación y revisión de pruebas para: services/tarea_service.py

Prompt utilizado:
"Genera pruebas unitarias con pytest para un servicio de tareas de un Workflow Manager. El servicio debe permitir crear, buscar, modificar y eliminar tareas, cambiar estados, validar responsables, crear subtareas y ordenar tareas mediante Bubble Sort, Merge Sort y Quick Sort. Incluye pruebas de permisos para que un usuario normal solamente pueda cambiar el estado de tareas asignadas a él."

Resultado
Se generaron pruebas para:
Creación de tareas.
Búsqueda.
Modificación.
Eliminación.
Cambio de estado.
Creación de subtareas.
Validación de tareas duplicadas.
Validación de responsables.
Control de permisos.
Listado de tareas.
Ordenamiento por ID.

Revisión humana:
El equipo ejecutó las pruebas y comparó los resultados con el comportamiento esperado del sistema.
Cuando aparecieron errores relacionados con diferencias entre los nombres de métodos, parámetros o estructuras utilizadas, las pruebas fueron modificadas manualmente para corresponder a la implementación final.

Uso de IA #3 — Diagnóstico de errores durante las pruebas

Función trabajada:
Análisis de errores obtenidos mediante pytest.

Objetivo:
Comprender errores de integración entre los servicios, repositorios y estructuras de datos.

Prompt utilizado:
"Analiza este error de pytest y explícame qué significa, cuál es la causa y qué debería revisar en mi código. No modifiques la arquitectura del proyecto solamente para hacer pasar el test."

Ejemplo de error analizado:
AttributeError: 'ListaDoble' object has no attribute 'cargar'

Resultado:
Se identificó que el problema no correspondía a la implementación de la lista doblemente enlazada, sino a que el servicio esperaba recibir un repositorio con un método cargar() mientras la prueba estaba proporcionando directamente una instancia de ListaDoble.

Esto permitió corregir la configuración de las pruebas en lugar de modificar innecesariamente la estructura de datos.

Validación humana:
El equipo verificó manualmente:
La firma del constructor del servicio.
Las responsabilidades del repositorio.
Las funciones disponibles en ListaDoble.
El comportamiento esperado según la arquitectura del proyecto.

Uso de IA #4 — Adaptación de mocks y repositorios para pruebas

Función trabajada:
Pruebas de servicios que dependen de persistencia.

Prompt utilizado:
Crea un RepositoryMock sencillo para utilizar en pruebas unitarias de un servicio que guarda y carga información mediante un repositorio. El mock debe funcionar en memoria y no utilizar archivos reales.

Resultado:
Se utilizaron repositorios simulados para evitar que las pruebas dependieran directamente de archivos CSV.
Esto permitió probar los servicios de forma aislada y evitar que una prueba modificara permanentemente los datos del proyecto.

Validación humana:
El equipo comprobó que los métodos del mock coincidieran con los métodos realmente utilizados por los servicios, realizando ajustes cuando fue necesario.

Uso de IA #5 — Revisión de la lista doblemente enlazada

Función trabajada:
structures/lista_doble.py

Objetivo:
Revisar la implementación de:
Inserción.
Búsqueda.
Eliminación.
Modificación.
Recorrido.
Manejo de cabeza y cola.

Prompt utilizado:
"Revisa esta implementación de una lista doblemente enlazada utilizada para almacenar objetos Usuario. Identifica errores en los enlaces anterior y siguiente, eliminación de nodos, actualización de cabeza y cola y manejo del tamaño de la lista. No cambies la estructura general de la implementación."

Validación humana:
Las recomendaciones fueron comparadas con la implementación existente y se verificó mediante pruebas que:
La inserción funcionara correctamente.
La búsqueda recorriera la lista.
La eliminación actualizara correctamente los enlaces.
La cabeza y la cola fueran consistentes.
El tamaño de la estructura se actualizara.

Uso de IA #6 — Revisión de pila y colas

Función trabajada:
structures/pila.py
structures/cola_fifo.py
structures/cola_prioridad.py

Prompt utilizado:
"Revisa estas implementaciones de una pila, una cola FIFO y una cola de prioridad. Comprueba que respeten LIFO, FIFO y el orden de prioridad correspondiente. Identifica posibles errores sin cambiar innecesariamente la interfaz utilizada por el resto del proyecto."

Resultado:
Se revisó el comportamiento esperado de las estructuras:

Pila
A → B → desapilar() = B

Cola FIFO
A → B → desencolar() = A

Cola de prioridad
Las tareas de mayor prioridad deben procesarse antes que las de menor prioridad.

Validación humana:
Se verificó el comportamiento mediante pruebas automatizadas y pruebas manuales.

Uso de IA #7 — Revisión del árbol de tareas

Función trabajada:
structures/arbol_tareas.py

Objetivo:
Revisar la representación jerárquica de tareas y subtareas.

Prompt utilizado:
"Revisa este árbol de tareas implementado en Python. Comprueba que permita agregar tareas raíz, agregar subtareas, buscar nodos recursivamente, eliminar subárboles y recorrer todos los niveles mediante recursividad. No reemplaces la estructura por una lista o estructura externa."

Resultado:
Se verificó que el árbol permitiera representar relaciones como:
Tarea principal
├── Subtarea 1
├── Subtarea 2
└── Subtarea 3

También se revisó el uso de recursividad en la búsqueda, recorrido y eliminación.

Validación humana:
El equipo comprobó el funcionamiento mediante las pruebas de integración y las pruebas específicas del servicio de tareas.

Uso de IA #8 — Revisión del historial Undo/Redo

Función trabajada:
services/historial_service.py

Objetivo:
Comprobar el comportamiento de las dos pilas utilizadas para implementar Undo/Redo.

Prompt utilizado:
"Revisa este servicio de historial que utiliza dos pilas para implementar Undo y Redo. Comprueba que una acción nueva se registre en deshacer, que al hacer Undo pase a rehacer y que al hacer una nueva acción se limpie correctamente la pila de rehacer."

Resultado:
Se verificó el flujo:
Nueva acción
     ↓
Pila Deshacer
     ↓
    Undo
     ↓
Pila Rehacer
     ↓
    Redo
     ↓
Pila Deshacer

Revisión humana:
El comportamiento fue comprobado mediante pruebas automatizadas de:
Registro de acciones.
Deshacer.
Rehacer.

Uso de IA #9 — Revisión de persistencia CSV

Función trabajada:
persistence/usuario_repository.py
persistence/tarea_repository.py

Prompt utilizado"
"Revisa esta implementación de persistencia mediante archivos CSV. Comprueba que los datos puedan guardarse y cargarse correctamente, que los encabezados sean consistentes y que los valores almacenados puedan reconstruirse como objetos del modelo correspondiente."

Resultado:
Se revisaron las operaciones de escritura y lectura de usuarios y tareas.
También se revisó que las modificaciones realizadas mediante los servicios pudieran persistirse nuevamente.

Validación humana:
El equipo ejecutó pruebas específicas de persistencia y comprobó que los archivos CSV fueran generados correctamente.

Uso de IA #10 — Revisión del escalamiento SLA

Función trabajada:
services/tarea_service.py

Objetivo:
Revisar el mecanismo de prevención de inanición de tareas.

Prompt utilizado:
"Analiza este mecanismo de escalamiento SLA para una cola de tareas. Una tarea regular debe incrementar sus ciclos de espera y, al alcanzar un límite determinado, pasar a la cola de prioridad. Verifica que no se procese dos veces y que el evento quede registrado en auditoría."

Resultado"
Se revisó el flujo:

Tarea regular
      ↓
Incrementa ciclos de espera
      ↓
¿Alcanza el límite?
      ↓
     Sí
      ↓
Sale de FIFO
      ↓
Entra a cola de prioridad
      ↓
Se registra en auditoría

Validación humana:
"El equipo verificó que el mecanismo no eliminara las estructuras de datos requeridas y que el escalamiento mantuviera la lógica establecida en el proyecto."

Uso de IA #11 — Revisión de algoritmos de ordenamiento

Función trabajada:
services/ordenador_tareas.py

Objetivo:
Revisar las implementaciones de Bubble Sort, Merge Sort y Quick Sort.

Prompt utilizado:
"Revisa estas implementaciones de Bubble Sort, Merge Sort y Quick Sort para una lista de objetos Tarea. Verifica que ordenen correctamente utilizando una función clave y que sus complejidades temporales correspondan a los algoritmos implementados."

Resultado:
Se verificó que los algoritmos permitieran ordenar las tareas por diferentes criterios, como:
ID.
Prioridad.

También se revisaron las complejidades:
Algoritmo	Mejor caso	Promedio	Peor caso
Bubble Sort	O(n)	O(n²)	O(n²)
Merge Sort	O(n log n)	O(n log n)	O(n log n)
Quick Sort	O(n log n)	O(n log n)	O(n²)

Validación humana:
El equipo comprobó los resultados mediante pruebas automatizadas y verificó que los algoritmos fueran implementaciones propias y no funciones de ordenamiento externas.

Uso de IA #12 — Revisión general de arquitectura

Función trabajada:
Revisión general del proyecto.

Prompt utilizado:
"Revisa la arquitectura de este proyecto de estructuras de datos y determina si existe una separación adecuada entre modelos, estructuras de datos, servicios y persistencia. Identifica dependencias innecesarias y posibles problemas de diseño sin reemplazar las estructuras implementadas desde cero."

Resultado:
Se revisó la separación entre:

models/
    ↓
structures/
    ↓
services/
    ↓
persistence/

La revisión permitió identificar responsabilidades de cada componente y detectar dependencias que podían provocar errores durante las pruebas.

Validación humana:
Las recomendaciones fueron evaluadas manualmente. No se aplicaron cambios únicamente por recomendación de la IA; cada modificación fue comparada con los requisitos del proyecto y posteriormente probada.

Uso de IA #13 — Revisión de documentación

Función trabajada:
README.md

Objetivo:
Mejorar la documentación del proyecto y explicar:

Objetivo.
Arquitectura.
Estructuras de datos.
Algoritmos.
Persistencia.
Auditoría.
SLA.
Pruebas.
Uso de Git.
Uso de Inteligencia Artificial.

Prompt utilizado:
Revisa este README de un proyecto universitario de estructuras de datos y mejora su organización, claridad y documentación técnica. Mantén la información existente y evita agregar funcionalidades que no estén implementadas.

Validación humana:
El equipo verificó que la documentación describiera únicamente funcionalidades realmente implementadas en el proyecto.

16. Responsabilidad sobre el código generado o asistido por IA

La Inteligencia Artificial fue utilizada como herramienta de apoyo durante el desarrollo, pero la responsabilidad final sobre el código corresponde al equipo.

La utilización de IA se realizó bajo los siguientes principios:
Revisión humana: ninguna sugerencia fue incorporada automáticamente sin ser revisada.
Ejecución: las modificaciones propuestas fueron ejecutadas y probadas dentro del proyecto.
Validación: se comprobó que el comportamiento coincidiera con los requisitos del proyecto.
Comprensión: el equipo debe ser capaz de explicar durante la defensa el funcionamiento del código utilizado.
Adaptación: las respuestas de IA fueron modificadas cuando no coincidían con las interfaces, estructuras o arquitectura del proyecto.
Pruebas: los cambios fueron comprobados mediante pruebas automatizadas y pruebas manuales.
Conservación de los requisitos: no se utilizaron recomendaciones que eliminaran las estructuras de datos solicitadas por el enunciado.
Responsabilidad: la utilización de una herramienta de Inteligencia Artificial no sustituye la responsabilidad del equipo sobre las decisiones de diseño, implementación y funcionamiento del sistema.

La IA se utilizó principalmente para acelerar tareas de análisis, detectar posibles errores y servir como apoyo durante el proceso de desarrollo. El código final fue revisado, adaptado y validado por los integrantes del equipo.

Resultado final de las pruebas:
Al finalizar el proceso de revisión, el proyecto cuenta con:

33 pruebas ejecutadas
33 pruebas exitosas
0 pruebas fallidas
100% de pruebas exitosas

La ejecución se realizó mediante: python -m pytest -v
Resultado: 33 passed in 0.08s

17. Ejecución

Desde la carpeta raíz del proyecto: python main.py

También es posible ejecutar las pruebas: pytest -v

18. Requisitos del proyecto cubiertos
Requisito	Implementado
Lista doblemente enlazada	✅
Pila	✅
Cola FIFO	✅
Cola de prioridad	✅
Árbol de tareas	✅
Recursividad	✅
Bubble Sort	✅
Merge Sort	✅
Quick Sort	✅
Persistencia CSV	✅
Gestión de usuarios	✅
Gestión de tareas	✅
Roles y permisos	✅
Login	✅
Contraseña oculta	✅
Validaciones	✅
Undo	✅
Redo	✅
SLA / Anti-starvation	✅
Auditoría	✅
Pruebas automatizadas	✅
Git / GitHub	✅
Pull Requests	✅
Bitácora de IA	✅

19. Conclusión

El Workflow Manager integra estructuras de datos, algoritmos de ordenamiento, persistencia, control de acceso, auditoría y gestión de tareas en una aplicación de consola.
La arquitectura separa modelos, estructuras, servicios y persistencia para facilitar el mantenimiento, las pruebas y la evolución del sistema.