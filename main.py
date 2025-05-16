#!/usr/bin/env python3
import cmd
import sys
from process import Process, RoundRobinScheduler, SJFScheduler
from memory import MemoryManager
from sync import ProducerConsumer, ReadersWriters, DiningPhilosophers
from io_devices import IORequest, IORequestType, Printer, DiskScheduler

class OSSimulator(cmd.Cmd):
    """Simulador de Sistema Operativo"""
    intro = 'Bienvenido al Simulador de SO. Escribe help o ? para listar los comandos.\n'
    prompt = 'SO> '

    def __init__(self):
        super().__init__()
        # Inicialización de componentes
        self.scheduler = RoundRobinScheduler()
        self.memory = MemoryManager()
        self.producer_consumer = ProducerConsumer()
        self.readers_writers = ReadersWriters()
        self.philosophers = DiningPhilosophers()
        self.printer = Printer()
        self.disk = DiskScheduler()
        self.processes = {}

    def do_proceso(self, arg):
        """
        Gestión de procesos:
        proceso crear <nombre> <tiempo_cpu> [prioridad] [memoria]
        proceso listar
        proceso info <pid>
        proceso suspender <pid>
        proceso reanudar <pid>
        proceso terminar <pid>
        """
        args = arg.split()
        if not args:
            print("Error: Comando incompleto. Use 'help proceso' para más información.")
            return

        if args[0] == 'crear':
            if len(args) < 3:
                print("Error: Faltan argumentos para crear proceso.")
                return
            try:
                priority = int(args[3]) if len(args) > 3 else 0
                memory = int(args[4]) if len(args) > 4 else 10
                process = Process(args[1], int(args[2]), priority, memory)
                self.processes[process.pid] = process
                self.scheduler.add_process(process)
                self.memory.allocate_memory(process)
                print(f"Proceso creado con PID {process.pid}")
            except ValueError:
                print("Error: Los argumentos numéricos deben ser enteros.")

        elif args[0] == 'listar':
            if not self.processes:
                print("No hay procesos en el sistema.")
                return
            print("\nProcesos en el sistema:")
            print("PID | Nombre | Estado | Tiempo Restante")
            print("-" * 45)
            for pid, process in self.processes.items():
                print(f"{pid:3d} | {process.name:6s} | {process.state.value:15s} | {process.remaining_time:3d}")

        elif args[0] == 'info':
            if len(args) < 2:
                print("Error: Falta el PID del proceso.")
                return
            try:
                pid = int(args[1])
                if pid in self.processes:
                    process = self.processes[pid]
                    print(f"\nInformación del proceso {pid}:")
                    print(f"Nombre: {process.name}")
                    print(f"Estado: {process.state.value}")
                    print(f"Prioridad: {process.priority}")
                    print(f"Tiempo total: {process.burst_time}")
                    print(f"Tiempo restante: {process.remaining_time}")
                    print(f"Tiempo de espera: {process.waiting_time}")
                else:
                    print(f"Error: No existe el proceso con PID {pid}")
            except ValueError:
                print("Error: El PID debe ser un número entero.")

    def do_planificador(self, arg):
        """
        Gestión del planificador:
        planificador info
        planificador ejecutar [pasos]
        planificador cambiar <RR|SJF> [quantum]
        """
        args = arg.split()
        if not args:
            print("Error: Comando incompleto. Use 'help planificador' para más información.")
            return

        if args[0] == 'info':
            print("\nInformación del planificador:")
            print(f"Tipo: {'Round Robin' if isinstance(self.scheduler, RoundRobinScheduler) else 'SJF'}")
            if isinstance(self.scheduler, RoundRobinScheduler):
                print(f"Quantum: {self.scheduler.quantum}")
            print(f"Procesos en cola: {len(self.scheduler.ready_queue)}")
            if self.scheduler.running_process:
                print(f"Proceso en ejecución: {self.scheduler.running_process}")

        elif args[0] == 'ejecutar':
            steps = int(args[1]) if len(args) > 1 else 1
            for _ in range(steps):
                if not self.scheduler.execute_step():
                    print("No hay más procesos para ejecutar.")
                    break
            print("Ejecución completada.")

    def do_memoria(self, arg):
        """
        Gestión de memoria:
        memoria info
        memoria marcos
        memoria paginas <pid>
        memoria acceder <pid> <pagina>
        memoria algoritmo <LRU|FIFO>
        """
        args = arg.split()
        if not args:
            print("Error: Comando incompleto. Use 'help memoria' para más información.")
            return

        if args[0] == 'info':
            stats = self.memory.get_statistics()
            print("\nEstadísticas de memoria:")
            print(f"Marcos totales: {stats['total_frames']}")
            print(f"Marcos usados: {stats['used_frames']}")
            print(f"Marcos libres: {stats['free_frames']}")
            print(f"Uso de memoria: {stats['usage_percent']:.2f}%")
            print(f"Fallos de página: {stats['page_faults']}")
            print(f"Aciertos de página: {stats['page_hits']}")
            print(f"Tasa de aciertos: {stats['hit_ratio']:.2f}")

        elif args[0] == 'marcos':
            self.memory.print_memory_map()

        elif args[0] == 'algoritmo':
            if len(args) < 2:
                print("Error: Falta especificar el algoritmo.")
                return
            if args[1] in ['LRU', 'FIFO']:
                self.memory.set_replacement_algorithm(args[1])
                print(f"Algoritmo cambiado a {args[1]}")
            else:
                print("Error: Algoritmo no válido.")

    def do_sincronizacion(self, arg):
        """
        Gestión de sincronización:
        sincronizacion productor <pid> <item>
        sincronizacion consumidor <pid>
        sincronizacion lector <pid> [iniciar|terminar]
        sincronizacion escritor <pid> [iniciar|terminar]
        sincronizacion filosofo <pid> <posicion> [tomar|dejar]
        """
        args = arg.split()
        if not args:
            print("Error: Comando incompleto. Use 'help sincronizacion' para más información.")
            return

        if args[0] == 'productor':
            if len(args) < 3:
                print("Error: Faltan argumentos para el productor.")
                return
            try:
                pid = int(args[1])
                if pid in self.processes:
                    if self.producer_consumer.produce(self.processes[pid], args[2]):
                        print("Item producido exitosamente.")
                    else:
                        print("No se pudo producir el item (buffer lleno).")
                else:
                    print(f"Error: No existe el proceso con PID {pid}")
            except ValueError:
                print("Error: El PID debe ser un número entero.")

        elif args[0] == 'consumidor':
            if len(args) < 2:
                print("Error: Falta el PID del consumidor.")
                return
            try:
                pid = int(args[1])
                if pid in self.processes:
                    success, item = self.producer_consumer.consume(self.processes[pid])
                    if success:
                        print(f"Item consumido: {item}")
                    else:
                        print("No se pudo consumir (buffer vacío).")
                else:
                    print(f"Error: No existe el proceso con PID {pid}")
            except ValueError:
                print("Error: El PID debe ser un número entero.")

        elif args[0] == 'lector':
            if len(args) < 3:
                print("Error: Faltan argumentos para el lector.")
                return
            try:
                pid = int(args[1])
                if pid not in self.processes:
                    print(f"Error: No existe el proceso con PID {pid}")
                    return

                if args[2] == 'iniciar':
                    if self.readers_writers.start_read(self.processes[pid]):
                        print("Lectura iniciada.")
                    else:
                        print("No se pudo iniciar la lectura.")
                elif args[2] == 'terminar':
                    if self.readers_writers.end_read(self.processes[pid]):
                        print("Lectura terminada.")
                    else:
                        print("No se pudo terminar la lectura.")
                else:
                    print("Error: Acción no válida. Use 'iniciar' o 'terminar'.")
            except ValueError:
                print("Error: El PID debe ser un número entero.")

        elif args[0] == 'escritor':
            if len(args) < 3:
                print("Error: Faltan argumentos para el escritor.")
                return
            try:
                pid = int(args[1])
                if pid not in self.processes:
                    print(f"Error: No existe el proceso con PID {pid}")
                    return

                if args[2] == 'iniciar':
                    if self.readers_writers.start_write(self.processes[pid]):
                        print("Escritura iniciada.")
                    else:
                        print("No se pudo iniciar la escritura.")
                elif args[2] == 'terminar':
                    if self.readers_writers.end_write(self.processes[pid]):
                        print("Escritura terminada.")
                    else:
                        print("No se pudo terminar la escritura.")
                else:
                    print("Error: Acción no válida. Use 'iniciar' o 'terminar'.")
            except ValueError:
                print("Error: El PID debe ser un número entero.")

        elif args[0] == 'filosofo':
            if len(args) < 4:
                print("Error: Faltan argumentos para el filósofo.")
                return
            try:
                pid = int(args[1])
                position = int(args[2])
                if pid not in self.processes:
                    print(f"Error: No existe el proceso con PID {pid}")
                    return

                if args[3] == 'tomar':
                    if self.philosophers.take_forks(position):
                        print("Tenedores tomados.")
                    else:
                        print("No se pudieron tomar los tenedores.")
                elif args[3] == 'dejar':
                    if self.philosophers.put_forks(position):
                        print("Tenedores dejados.")
                    else:
                        print("No se pudieron dejar los tenedores.")
                else:
                    print("Error: Acción no válida. Use 'tomar' o 'dejar'.")
            except ValueError:
                print("Error: El PID y la posición deben ser números enteros.")

    def do_disco(self, arg):
        """
        Gestión del disco:
        disco algoritmo <FCFS|SSTF|SCAN>
        disco solicitar <sector>
        disco ejecutar [pasos]
        disco estado
        """
        args = arg.split()
        if not args:
            print("Error: Comando incompleto. Use 'help disco' para más información.")
            return

        if args[0] == 'algoritmo':
            if len(args) < 2:
                print("Error: Falta especificar el algoritmo.")
                return
            if args[1] in ['FCFS', 'SSTF', 'SCAN']:
                self.disk.set_algorithm(args[1])
                print(f"Algoritmo cambiado a {args[1]}")
            else:
                print("Error: Algoritmo no válido.")

        elif args[0] == 'solicitar':
            if len(args) < 2:
                print("Error: Falta especificar el sector.")
                return
            try:
                sector = int(args[1])
                self.disk.add_request(sector)
                print(f"Solicitud añadida para el sector {sector}")
            except ValueError:
                print("Error: El sector debe ser un número entero.")

        elif args[0] == 'ejecutar':
            steps = int(args[1]) if len(args) > 1 else 1
            for _ in range(steps):
                if not self.disk.process_next():
                    print("No hay más solicitudes pendientes.")
                    break
            print("Ejecución completada.")

        elif args[0] == 'estado':
            stats = self.disk.get_statistics()
            print("\nEstado del disco:")
            print(f"Pista actual: {stats['current_track']}")
            print(f"Solicitudes pendientes: {stats['pending_requests']}")
            print(f"Total de movimientos: {stats['total_seeks']}")
            print(f"Tiempo promedio de búsqueda: {stats['avg_seek_time']:.2f}")
            print(f"Algoritmo actual: {stats['algorithm']}")
            if stats['last_movements']:
                print("\nÚltimos movimientos:")
                for from_track, to_track in stats['last_movements']:
                    print(f"  {from_track} -> {to_track}")

    def do_salir(self, arg):
        """Salir del simulador"""
        print("Gracias por usar el Simulador de SO.")
        return True

    def do_ayuda(self, arg):
        """Muestra la ayuda del simulador"""
        print("""
Comandos disponibles:
  proceso      - Gestión de procesos
  planificador - Control del planificador
  memoria     - Gestión de memoria virtual
  sincronizacion - Mecanismos de sincronización
  disco       - Planificación de disco
  salir       - Salir del simulador
  ayuda       - Mostrar esta ayuda

Use 'help <comando>' para más información sobre un comando específico.
        """)

if __name__ == '__main__':
    OSSimulator().cmdloop() 