#!/usr/bin/env python3
from collections import deque
from enum import Enum
import heapq

class IORequestType(Enum):
    """Tipos de solicitudes de E/S"""
    READ = "Lectura"
    WRITE = "Escritura"
    PRINT = "Impresión"

class IORequest:
    """Solicitud de E/S"""
    def __init__(self, process, request_type, data=None, priority=0):
        self.process = process
        self.type = request_type
        self.data = data
        self.priority = priority
        self.arrival_time = 0
        self.completion_time = 0

    def __lt__(self, other):
        return self.priority > other.priority  # Mayor prioridad primero

class IODevice:
    """Dispositivo de E/S genérico"""
    def __init__(self, name, processing_time=1):
        self.name = name
        self.processing_time = processing_time
        self.current_request = None
        self.queue = []  # Cola de prioridad
        self.busy = False
        self.time = 0
        self.completed_requests = []

    def add_request(self, request):
        """Añade una solicitud a la cola"""
        request.arrival_time = self.time
        heapq.heappush(self.queue, request)

    def process_next(self):
        """Procesa la siguiente solicitud"""
        if self.busy:
            self.time += 1
            if self.time - self.current_request.arrival_time >= self.processing_time:
                self.current_request.completion_time = self.time
                self.completed_requests.append(self.current_request)
                self.busy = False
                self.current_request = None
                return True
            return False

        if self.queue:
            self.current_request = heapq.heappop(self.queue)
            self.busy = True
            return self.process_next()

        return False

    def get_statistics(self):
        """Obtiene estadísticas del dispositivo"""
        if not self.completed_requests:
            return {
                'total_requests': 0,
                'avg_wait_time': 0,
                'avg_turnaround_time': 0,
                'device_utilization': 0
            }

        total = len(self.completed_requests)
        wait_times = [r.completion_time - r.arrival_time - self.processing_time 
                     for r in self.completed_requests]
        turnaround_times = [r.completion_time - r.arrival_time 
                           for r in self.completed_requests]

        return {
            'total_requests': total,
            'avg_wait_time': sum(wait_times) / total,
            'avg_turnaround_time': sum(turnaround_times) / total,
            'device_utilization': (self.processing_time * total) / self.time if self.time > 0 else 0
        }

class Printer(IODevice):
    """Impresora simulada"""
    def __init__(self, name="Printer", processing_time=5):
        super().__init__(name, processing_time)
        self.print_history = []

    def process_next(self):
        """Procesa la siguiente solicitud de impresión"""
        if super().process_next():
            if self.current_request:
                self.print_history.append({
                    'time': self.time,
                    'process': self.current_request.process.pid,
                    'data': self.current_request.data
                })
            return True
        return False

class DiskScheduler:
    """Planificador de disco"""
    def __init__(self, total_tracks=200):
        self.total_tracks = total_tracks
        self.current_track = 0
        self.direction = 1  # 1 hacia arriba, -1 hacia abajo
        self.queue = []
        self.algorithm = "FCFS"
        self.history = []
        self.total_seeks = 0

    def add_request(self, track):
        """Añade una solicitud de acceso a pista"""
        if 0 <= track < self.total_tracks:
            self.queue.append(track)

    def set_algorithm(self, algorithm):
        """Cambia el algoritmo de planificación"""
        self.algorithm = algorithm
        if algorithm == "SCAN":
            self.direction = 1

    def process_next(self):
        """Procesa la siguiente solicitud según el algoritmo actual"""
        if not self.queue:
            return False

        next_track = None

        if self.algorithm == "FCFS":
            next_track = self.queue.pop(0)

        elif self.algorithm == "SSTF":
            # Encuentra la pista más cercana
            closest_idx = min(range(len(self.queue)), 
                            key=lambda i: abs(self.queue[i] - self.current_track))
            next_track = self.queue.pop(closest_idx)

        elif self.algorithm == "SCAN":
            # Encuentra la siguiente pista en la dirección actual
            candidates = [t for t in self.queue if 
                        (t - self.current_track) * self.direction > 0]
            
            if not candidates:
                self.direction *= -1
                candidates = [t for t in self.queue if 
                            (t - self.current_track) * self.direction > 0]

            if candidates:
                next_track = min(candidates) if self.direction > 0 else max(candidates)
                self.queue.remove(next_track)
            elif self.queue:
                next_track = self.queue.pop(0)

        if next_track is not None:
            seek_time = abs(self.current_track - next_track)
            self.total_seeks += seek_time
            self.history.append((self.current_track, next_track))
            self.current_track = next_track
            return True

        return False

    def get_statistics(self):
        """Obtiene estadísticas del planificador"""
        return {
            'current_track': self.current_track,
            'pending_requests': len(self.queue),
            'total_seeks': self.total_seeks,
            'avg_seek_time': self.total_seeks / len(self.history) if self.history else 0,
            'algorithm': self.algorithm,
            'last_movements': self.history[-10:]  # Últimos 10 movimientos
        } 