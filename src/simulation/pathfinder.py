import heapq
from typing import Dict, List, Optional
from src.models import Network, Zone


class PathFinder:
    """Calculador de rutas basado en el algoritmo de Dijkstra adaptado."""

    def __init__(self, network: Network) -> None:
        """Inicializa el buscador con la red del mapa."""
        self.network: Network = network

    def _get_zone_cost(self, zone: Zone) -> int:
        """Determina el coste en turnos para ingresar a una zona."""
        if zone.zone_type == "blocked":
            return 999999
        if zone.zone_type == "restricted":
            return 2
        return 1

    def find_shortest_path(
        self, start: Zone, end: Zone
    ) -> Optional[List[Zone]]:
        """Calcula el camino más corto entre dos zonas considerando costes."""
        distances: Dict[str, float] = {
            name: float("inf") for name in self.network.zones
        }
        distances[start.name] = 0.0

        previous: Dict[str, Optional[Zone]] = {
            name: None for name in self.network.zones
        }

        pq: List[tuple[float, str]] = [(0.0, start.name)]

        while pq:
            current_dist, current_name = heapq.heappop(pq)

            if current_dist > distances[current_name]:
                continue

            current_zone = self.network.zones[current_name]
            if current_zone.name == end.name:
                break

            for neighbor in self.network.get_neighbors(current_zone):
                cost = self._get_zone_cost(neighbor)
                distance = current_dist + float(cost)

                if distance < distances[neighbor.name]:
                    distances[neighbor.name] = distance
                    previous[neighbor.name] = current_zone
                    heapq.heappush(pq, (distance, neighbor.name))

        path: List[Zone] = []
        curr: Optional[Zone] = end

        while curr is not None:
            path.append(curr)
            curr = previous[curr.name]

        path.reverse()

        if not path or path[0].name != start.name:
            return None

        return path
