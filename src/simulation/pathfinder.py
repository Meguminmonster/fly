import heapq
from typing import Dict, List, Optional
from src.models import Network, Zone


class PathFinder:

    def __init__(self, network: Network) -> None:
        """Inicializa el buscador con la red del mapa."""
        self.network: Network = network

    def _get_zone_cost(self, zone: Zone) -> float:
        if zone.zone_type == "restricted":
            return 2.0
        if zone.zone_type == "priority":
            return 0.9  # Preferencia en Dijkstra sin alterar los turnos reales
        return 1.0

    def find_shortest_path(
        self,
        start: Zone,
        end: Zone,
        zone_penalties: Optional[Dict[str, float]] = None,
    ) -> Optional[List[Zone]]:
        if zone_penalties is None:
            zone_penalties = {}

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
                if neighbor.zone_type == "blocked":
                    continue

                base_cost = self._get_zone_cost(neighbor)
                penalty = zone_penalties.get(neighbor.name, 1.0)
                distance = current_dist + (base_cost * penalty)

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

    def find_multiple_paths(
        self, start: Zone, end: Zone, max_paths: int = 5
    ) -> List[List[Zone]]:
        paths: List[List[Zone]] = []
        zone_penalties: Dict[str, float] = {}

        for _ in range(max_paths):
            path = self.find_shortest_path(
                start, end, zone_penalties=zone_penalties
            )
            if not path or path in paths:
                break

            paths.append(path)

            for zone in path:
                if not zone.is_start and not zone.is_end:
                    zone_penalties[zone.name] = (
                        zone_penalties.get(zone.name, 1.0) + 1.5
                    )

        return paths
