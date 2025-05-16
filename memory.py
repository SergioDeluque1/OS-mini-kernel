#!/usr/bin/env python3
from collections import deque
import time

class Page:
    """Clase que representa una página en memoria virtual"""
    def __init__(self, page_id, process_id):
        self.page_id = page_id
        self.process_id = process_id
        self.last_access = 0
        self.load_time = time.time()

class Frame:
    """Clase que representa un marco de página en memoria física"""
    def __init__(self, frame_id):
        self.frame_id = frame_id
        self.page = None
        self.is_free = True

    def load_page(self, page):
        self.page = page
        self.is_free = False
        page.last_access = time.time()

    def unload_page(self):
        self.page = None
        self.is_free = True

class MemoryManager:
    """Gestor de memoria virtual con paginación"""
    def __init__(self, total_frames=64, algorithm="LRU"):
        self.total_frames = total_frames
        self.frames = [Frame(i) for i in range(total_frames)]
        self.page_table = {}  # Mapeo de páginas a marcos
        self.algorithm = algorithm
        self.page_faults = 0
        self.page_hits = 0

    def set_replacement_algorithm(self, algorithm):
        """Cambia el algoritmo de reemplazo de páginas"""
        if algorithm in ["LRU", "FIFO"]:
            self.algorithm = algorithm
            return True
        return False

    def allocate_memory(self, process):
        """Asigna memoria a un proceso"""
        pages_needed = (process.memory_size + 3) // 4  # 4KB por página
        pages = []

        for i in range(pages_needed):
            page = Page(i, process.pid)
            pages.append(page)
            process.pages.append(page)

            # Buscar un marco libre o reemplazar según el algoritmo
            frame = self._get_free_frame()
            if frame:
                frame.load_page(page)
                self.page_table[page] = frame
            else:
                self._replace_page(page)

        return pages

    def _get_free_frame(self):
        """Busca un marco libre"""
        for frame in self.frames:
            if frame.is_free:
                return frame
        return None

    def _replace_page(self, new_page):
        """Reemplaza una página según el algoritmo configurado"""
        self.page_faults += 1

        if self.algorithm == "LRU":
            # Least Recently Used
            victim_frame = min(
                [f for f in self.frames if not f.is_free],
                key=lambda f: f.page.last_access
            )
        else:  # FIFO
            # First In First Out
            victim_frame = min(
                [f for f in self.frames if not f.is_free],
                key=lambda f: f.page.load_time
            )

        # Eliminar la página víctima de la tabla
        if victim_frame.page in self.page_table:
            del self.page_table[victim_frame.page]

        # Cargar la nueva página
        victim_frame.load_page(new_page)
        self.page_table[new_page] = victim_frame

    def access_page(self, process, page_id):
        """Accede a una página de un proceso"""
        page = next((p for p in process.pages if p.page_id == page_id), None)
        if not page:
            return False

        if page in self.page_table:
            frame = self.page_table[page]
            page.last_access = time.time()
            self.page_hits += 1
            return True
        else:
            self._replace_page(page)
            return False

    def get_statistics(self):
        """Obtiene estadísticas del uso de memoria"""
        used_frames = sum(1 for f in self.frames if not f.is_free)
        return {
            'total_frames': self.total_frames,
            'used_frames': used_frames,
            'free_frames': self.total_frames - used_frames,
            'usage_percent': (used_frames / self.total_frames) * 100,
            'page_faults': self.page_faults,
            'page_hits': self.page_hits,
            'hit_ratio': self.page_hits / (self.page_hits + self.page_faults) if (self.page_hits + self.page_faults) > 0 else 0
        }

    def print_memory_map(self):
        """Imprime un mapa de la memoria física"""
        print("\nMapa de Memoria Física:")
        print("Marco | PID | Página | Último Acceso")
        print("-" * 40)
        for frame in self.frames:
            if not frame.is_free:
                last_access = time.strftime('%H:%M:%S', 
                    time.localtime(frame.page.last_access))
                print(f"{frame.frame_id:5d} | {frame.page.process_id:3d} | {frame.page.page_id:6d} | {last_access}")
            else:
                print(f"{frame.frame_id:5d} | --- | ------ | --------") 