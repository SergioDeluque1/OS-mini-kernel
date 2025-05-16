#!/usr/bin/env python3
from enum import Enum
from collections import deque
import time

class ProcessState(Enum):
    """Estados posibles de un proceso"""
    NEW = "Nuevo"
    READY = "Listo"
    RUNNING = "En ejecución"
    WAITING = "Esperando"
    TERMINATED = "Terminado"

class Process:
    """Clase que representa un proceso en el sistema"""
    _next_pid = 1

    def __init__(self, name, burst_time, priority=0, memory_size=10):
        self.pid = Process._next_pid
        Process._next_pid += 1
        self.name = name
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.state = ProcessState.NEW
        self.memory_size = memory_size
        self.waiting_time = 0
        self.turnaround_time = 0
        self.start_time = None
        self.pages = []

    def execute(self, time_slice=1):
        """Ejecuta el proceso por un tiempo determinado"""
        if self.state != ProcessState.RUNNING:
            self.state = ProcessState.RUNNING
            if not self.start_time:
                self.start_time = time.time()

        executed_time = min(time_slice, self.remaining_time)
        self.remaining_time -= executed_time

        if self.remaining_time <= 0:
            self.state = ProcessState.TERMINATED
            self.turnaround_time = time.time() - self.start_time

        return executed_time

    def __str__(self):
        return f"Proceso {self.pid}: {self.name} ({self.state.value})"

class Scheduler:
    """Clase base para los planificadores"""
    def __init__(self):
        self.ready_queue = deque()
        self.running_process = None
        self.waiting_queue = deque()
        self.terminated_processes = []
        self.current_time = 0

    def add_process(self, process):
        process.state = ProcessState.READY
        self.ready_queue.append(process)

    def get_next_process(self):
        raise NotImplementedError

    def update_waiting_times(self):
        for process in self.ready_queue:
            process.waiting_time += 1

class RoundRobinScheduler(Scheduler):
    """Implementación del algoritmo Round Robin"""
    def __init__(self, quantum=2):
        super().__init__()
        self.quantum = quantum

    def get_next_process(self):
        if not self.ready_queue:
            return None
        return self.ready_queue.popleft()

    def execute_step(self):
        if not self.running_process:
            self.running_process = self.get_next_process()

        if self.running_process:
            executed_time = self.running_process.execute(self.quantum)
            self.current_time += executed_time
            self.update_waiting_times()

            if self.running_process.state == ProcessState.TERMINATED:
                self.terminated_processes.append(self.running_process)
                self.running_process = None
            else:
                self.ready_queue.append(self.running_process)
                self.running_process = None

            return True
        return False

class SJFScheduler(Scheduler):
    """Implementación del algoritmo Shortest Job First"""
    def get_next_process(self):
        if not self.ready_queue:
            return None
        
        shortest_job = min(self.ready_queue, key=lambda p: p.remaining_time)
        self.ready_queue.remove(shortest_job)
        return shortest_job

    def execute_step(self):
        if not self.running_process:
            self.running_process = self.get_next_process()

        if self.running_process:
            executed_time = self.running_process.execute()
            self.current_time += executed_time
            self.update_waiting_times()

            if self.running_process.state == ProcessState.TERMINATED:
                self.terminated_processes.append(self.running_process)
                self.running_process = None

            return True
        return False 