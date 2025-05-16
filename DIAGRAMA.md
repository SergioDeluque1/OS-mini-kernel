# Arquitectura del Simulador de Sistema Operativo

## 1. Estructura General

```
+-------------------+
|    OSSimulator    |
|    (main.py)      |
+--------+----------+
         |
         v
+--------+----------+     +-----------------+     +------------------+
|  Gestión de      |     |   Memoria       |     |  Sincronización  |
|   Procesos       |<--->|    Virtual      |<--->|   de Procesos    |
| (process.py)     |     | (memory.py)     |     |   (sync.py)      |
+--------+----------+     +-----------------+     +------------------+
         |                                              ^
         v                                              |
+--------+----------+                                   |
| Entrada/Salida    |<----------------------------------+
| (io_devices.py)   |
+------------------+
```

## 2. Flujo de Ejecución

```
Usuario
   |
   v
[Interfaz CLI] --> [Comando] --> [Procesamiento]
   ^                                   |
   |                                   v
[Resultado] <-- [Actualización] <-- [Módulos]
```

## 3. Componentes Principales

### 3.1 Gestión de Procesos

```
  [Proceso]
     |
     +---> [Estado]
     |      - NEW
     |      - READY
     |      - RUNNING
     |      - WAITING
     |      - TERMINATED
     |
     +---> [Planificador]
            - Round Robin
            - SJF
```

### 3.2 Memoria Virtual

```
  [Página]  <---+
     |          |
  [Marco]       +--- [Algoritmos]
     |               - LRU
  [Tabla]            - FIFO
```

### 3.3 Sincronización

```
[Semáforos]
    |
    +---> [Productor/Consumidor]
    |           |
    |           +---> Buffer Compartido
    |
    +---> [Lectores/Escritores]
    |           |
    |           +---> Recurso Compartido
    |
    +---> [Filósofos]
            |
            +---> Tenedores Compartidos
```

### 3.4 E/S y Disco

```
[Dispositivos]
    |
    +---> [Impresora]
    |      - Cola de impresión
    |      - Prioridades
    |
    +---> [Disco]
           |
           +---> Algoritmos
                 - FCFS
                 - SSTF
                 - SCAN
```

## 4. Flujo de Datos

```
[Usuario] -> [Comando] -> [Parser]
                           |
                    [Validación]
                           |
                    [Ejecución]
                     |    |    |
            [Proceso] [Memoria] [E/S]
                     |    |    |
                    [Actualización]
                           |
                    [Resultado]
                           |
                    [Usuario]
```

## 5. Ejemplo de Interacción

```
Usuario: proceso crear navegador 10 1 64
    |
    v
[Validación de Comando]
    |
    v
[Crear Proceso]
    |
    +---> [Asignar PID]
    |
    +---> [Asignar Memoria]
    |      |
    |      +---> [Crear Páginas]
    |      |
    |      +---> [Asignar Marcos]
    |
    +---> [Añadir a Planificador]
    |
    v
[Mostrar Resultado]
```

## 6. Ciclo de Vida de un Proceso

```
   [NEW]
     |
     v
  [READY] <-----------------+
     |                      |
     v                      |
[RUNNING] ---> [WAITING] ---+
     |
     v
[TERMINATED]
```

Este diagrama representa la estructura y funcionamiento del simulador, mostrando cómo interactúan los diferentes componentes y cómo fluye la información entre ellos. Los módulos están diseñados para ser independientes pero cooperativos, permitiendo una simulación realista de un sistema operativo.
