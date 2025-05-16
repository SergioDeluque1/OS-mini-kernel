#!/usr/bin/env python3
from collections import deque
from process import ProcessState

class Semaphore:
    """Implementación de un semáforo"""
    def __init__(self, initial_value=1):
        self.value = initial_value
        self.waiting_queue = deque()

    def wait(self, process):
        """Operación P (wait)"""
        if self.value > 0:
            self.value -= 1
            return True
        else:
            process.state = ProcessState.WAITING
            self.waiting_queue.append(process)
            return False

    def signal(self):
        """Operación V (signal)"""
        if self.waiting_queue:
            process = self.waiting_queue.popleft()
            process.state = ProcessState.READY
            return process
        else:
            self.value += 1
            return None

class ProducerConsumer:
    """Implementación del problema productor-consumidor"""
    def __init__(self, buffer_size=5):
        self.buffer = deque(maxlen=buffer_size)
        self.mutex = Semaphore(1)
        self.empty = Semaphore(buffer_size)
        self.full = Semaphore(0)
        self.history = []

    def produce(self, producer, item):
        """Produce un item"""
        if not self.empty.wait(producer):
            return False

        if not self.mutex.wait(producer):
            return False

        self.buffer.append(item)
        self.history.append(('P', producer.pid, item))
        self.mutex.signal()
        self.full.signal()
        return True

    def consume(self, consumer):
        """Consume un item"""
        if not self.full.wait(consumer):
            return False, None

        if not self.mutex.wait(consumer):
            return False, None

        item = self.buffer.popleft()
        self.history.append(('C', consumer.pid, item))
        self.mutex.signal()
        self.empty.signal()
        return True, item

    def get_state(self):
        return {
            'buffer_content': list(self.buffer),
            'buffer_size': len(self.buffer),
            'history': self.history[-10:]  # Últimas 10 operaciones
        }

class ReadersWriters:
    """Implementación del problema lectores-escritores"""
    def __init__(self):
        self.mutex = Semaphore(1)
        self.write_lock = Semaphore(1)
        self.readers_count = 0
        self.history = []

    def start_read(self, reader):
        """Inicia una operación de lectura"""
        if not self.mutex.wait(reader):
            return False

        self.readers_count += 1
        if self.readers_count == 1:
            if not self.write_lock.wait(reader):
                self.readers_count -= 1
                self.mutex.signal()
                return False

        self.history.append(('R', reader.pid, 'start'))
        self.mutex.signal()
        return True

    def end_read(self, reader):
        """Finaliza una operación de lectura"""
        if not self.mutex.wait(reader):
            return False

        self.readers_count -= 1
        if self.readers_count == 0:
            self.write_lock.signal()

        self.history.append(('R', reader.pid, 'end'))
        self.mutex.signal()
        return True

    def start_write(self, writer):
        """Inicia una operación de escritura"""
        if not self.write_lock.wait(writer):
            return False

        self.history.append(('W', writer.pid, 'start'))
        return True

    def end_write(self, writer):
        """Finaliza una operación de escritura"""
        self.history.append(('W', writer.pid, 'end'))
        self.write_lock.signal()
        return True

    def get_state(self):
        return {
            'readers_count': self.readers_count,
            'writing': self.write_lock.value == 0,
            'history': self.history[-10:]  # Últimas 10 operaciones
        }

class DiningPhilosophers:
    """Implementación del problema de la cena de los filósofos"""
    def __init__(self, num_philosophers=5):
        self.num_philosophers = num_philosophers
        self.forks = [Semaphore(1) for _ in range(num_philosophers)]
        self.states = ['THINKING'] * num_philosophers
        self.history = []

    def take_forks(self, philosopher_id):
        """Intenta tomar los tenedores"""
        left = philosopher_id
        right = (philosopher_id + 1) % self.num_philosophers

        # Solución al interbloqueo: los filósofos pares toman primero
        # el tenedor derecho, los impares el izquierdo
        first = right if philosopher_id % 2 == 0 else left
        second = left if philosopher_id % 2 == 0 else right

        if not self.forks[first].wait(None):
            return False

        if not self.forks[second].wait(None):
            self.forks[first].signal()
            return False

        self.states[philosopher_id] = 'EATING'
        self.history.append((philosopher_id, 'start_eating'))
        return True

    def put_forks(self, philosopher_id):
        """Deja los tenedores"""
        left = philosopher_id
        right = (philosopher_id + 1) % self.num_philosophers

        self.forks[left].signal()
        self.forks[right].signal()
        self.states[philosopher_id] = 'THINKING'
        self.history.append((philosopher_id, 'end_eating'))
        return True

    def get_state(self):
        return {
            'states': self.states.copy(),
            'history': self.history[-10:],  # Últimas 10 operaciones
            'forks': [fork.value for fork in self.forks]
        } 