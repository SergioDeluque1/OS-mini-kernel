# Simulador de Sistema Operativo

Este es un simulador de sistema operativo que implementa varios conceptos fundamentales como gestión de procesos, memoria virtual, sincronización y planificación de disco.

## Requisitos

- Python 3.x

## Instalación

1. Clona o descarga todos los archivos del simulador:

   - main.py
   - process.py
   - memory.py
   - sync.py
   - io_devices.py

2. No se requieren dependencias adicionales.

## Ejecución

Para iniciar el simulador, ejecuta:

```bash
python main.py
```

## Funcionalidades y Comandos

### 1. Gestión de Procesos

```bash
proceso crear <nombre> <tiempo_cpu> [prioridad] [memoria]
proceso listar
proceso info <pid>
proceso suspender <pid>
proceso reanudar <pid>
proceso terminar <pid>
```

Ejemplo:

```bash
SO> proceso crear navegador 10 1 64
SO> proceso listar
```

### 2. Planificador de Procesos

```bash
planificador info                    # Muestra información del planificador actual
planificador ejecutar [pasos]        # Ejecuta n pasos de simulación
planificador cambiar <RR|SJF> [quantum]  # Cambia el algoritmo de planificación
```

Ejemplo:

```bash
SO> planificador cambiar RR 2
SO> planificador ejecutar 5
```

### 3. Memoria Virtual

```bash
memoria info                     # Muestra estadísticas de memoria
memoria marcos                   # Muestra el mapa de marcos de página
memoria paginas <pid>           # Muestra páginas de un proceso
memoria acceder <pid> <pagina>  # Simula acceso a una página
memoria algoritmo <LRU|FIFO>    # Cambia algoritmo de reemplazo
```

Ejemplo:

```bash
SO> memoria info
SO> memoria algoritmo LRU
```

### 4. Sincronización

#### Productor-Consumidor

```bash
sincronizacion productor <pid> <item>
sincronizacion consumidor <pid>
```

#### Lectores-Escritores

```bash
sincronizacion lector <pid> [iniciar|terminar]
sincronizacion escritor <pid> [iniciar|terminar]
```

#### Cena de los Filósofos

```bash
sincronizacion filosofo <pid> <posicion> [tomar|dejar]
```

Ejemplo:

```bash
SO> proceso crear productor 10 1 32
SO> sincronizacion productor 1 "dato1"
SO> proceso crear consumidor 10 1 32
SO> sincronizacion consumidor 2
```

### 5. Planificación de Disco

```bash
disco algoritmo <FCFS|SSTF|SCAN>  # Cambia algoritmo de planificación
disco solicitar <sector>          # Añade solicitud de acceso
disco ejecutar [pasos]            # Procesa n solicitudes
disco estado                      # Muestra estado actual
```

Ejemplo:

```bash
SO> disco algoritmo SCAN
SO> disco solicitar 50
SO> disco ejecutar 1
```

## Ejemplo de Sesión Completa

```bash
# Iniciar el simulador
python main.py

# Crear algunos procesos
SO> proceso crear navegador 10 1 64
SO> proceso crear editor 5 2 32
SO> proceso listar

# Configurar y ejecutar el planificador
SO> planificador cambiar RR 2
SO> planificador ejecutar 5

# Ver estado de la memoria
SO> memoria info
SO> memoria marcos

# Probar sincronización
SO> proceso crear productor 10 1 32
SO> proceso crear consumidor 10 1 32
SO> sincronizacion productor 1 "dato1"
SO> sincronizacion consumidor 2

# Probar planificación de disco
SO> disco algoritmo SCAN
SO> disco solicitar 50
SO> disco solicitar 120
SO> disco ejecutar 2
SO> disco estado

# Salir del simulador
SO> salir
```

## Notas Importantes

1. Los PIDs se asignan automáticamente empezando desde 1.
2. La memoria se gestiona en páginas de 4KB.
3. El planificador Round Robin usa un quantum por defecto de 2.
4. Los algoritmos de reemplazo de páginas disponibles son LRU y FIFO.
5. La sincronización incluye soluciones a problemas clásicos como productor-consumidor, lectores-escritores y la cena de los filósofos.
6. La planificación de disco implementa los algoritmos FCFS, SSTF y SCAN.

## Solución de Problemas

1. Si ves el error "ImportError", asegúrate de que todos los archivos están en el mismo directorio.
2. Si un comando no funciona, usa `help <comando>` para ver la sintaxis correcta.
3. Para ver todos los comandos disponibles, escribe `ayuda` o `help`.

## Contribuir

Este es un proyecto educativo diseñado para demostrar conceptos de sistemas operativos. Si encuentras errores o tienes sugerencias, por favor crea un issue o un pull request.
