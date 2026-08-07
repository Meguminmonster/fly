from typing import Dict, List, Optional
from src.models.connection import Connection
from src.models.zone import Zone


class Network:
    """Contiene la estructura completa de la red de transporte."""

    def __init__(
        self,
        zones: Dict[str, Zone],
        connections: List[Connection],
        start_hub: Zone,
        end_hub: Zone
    ) -> None:
        """Inicializa la red del grafo con sus nodos y conexiones."""
        self.zones: Dict[str, Zone] = zones
        self.connections: List[Connection] = connections
        self.start_hub: Zone = start_hub
        self.end_hub: Zone = end_hub

    def get_neighbors(self, zone: Zone) -> List[Zone]:
        """Devuelve todas las zonas adyacentes no bloqueadas."""
        neighbors: List[Zone] = []
        for conn in self.connections:
            dest = conn.get_destination(zone)
            if dest is not None and dest.zone_type != "blocked":
                neighbors.append(dest)
        return neighbors

    def get_connection(
        self, zone1: Zone, zone2: Zone
    ) -> Optional[Connection]:
        """Obtiene la conexión existente entre dos zonas si esta existe."""
        for conn in self.connections:
            if (
                (conn.zone1.name == zone1.name and
                 conn.zone2.name == zone2.name) or
                (conn.zone1.name == zone2.name and
                 conn.zone2.name == zone1.name)
            ):
                return conn
        return None
