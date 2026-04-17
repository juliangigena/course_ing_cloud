Guía Práctica: Instalación de Linux en macOS (Apple Silicon/Intel)

Esta guía detalla los pasos para la "Demo en vivo" de la Clase 2. El objetivo es que los alumnos vean cómo convertir hardware físico en recursos lógicos.

1. Requisitos Previos (Preparar antes de la clase)

Software: Descargar e instalar UTM (Recomendado para M1/M2/M3) o VMware Fusion.

Imagen ISO: Descargar Ubuntu 25.10 (Versión ARM64 para Mac modernos o x86_64 para Mac Intel).

Tiempo estimado de demo: 30-35 minutos.

2. El Paso a Paso (Para dictar en clase)

Paso A: Creación de la "Carcasa" (Hardware Virtual)

Abrir UTM y seleccionar "Create a New Virtual Machine".

Elegir "Virtualize" (Explicar que esto usa la aceleración nativa del procesador, a diferencia de "Emulate").

Seleccionar el sistema operativo (Linux) y buscar la imagen .iso descargada.

Paso B: Asignación de Recursos (Concepto de Hipervisor)

Memoria: Asignar 2GB (Explicar que esto se resta de la RAM física de la Mac mientras la VM corre).

CPU: Asignar 2 núcleos.

Almacenamiento: Crear un disco de 20GB (Aclarar que es un archivo .utm o .vmdk en el disco duro, no una partición física).

Paso C: Instalación y Red

Network: Explicar el modo Shared Network (NAT): "La VM sale a internet usando la IP de la Mac".

Iniciar la VM y mostrar la pantalla de carga de Ubuntu.

3. Puntos Clave para "Vender" el concepto durante la Demo

Snapshot: Si el software lo permite, muestra cómo tomar una "foto" del estado. "Si borro algo importante, vuelvo atrás en un segundo. En On-premise, esto requiere backups de horas".

Monitor de Actividad: Abre el Monitor de Actividad de macOS para mostrar cómo el proceso de la VM consume CPU real. "Aquí ven al Hipervisor mediando entre el software y mi procesador".

4. Tarea para los alumnos

Pedirles que para la Clase 3 traigan instalado su propio Linux local, ya que lo usaremos para conectar con los primeros servicios de AWS (CLI).
