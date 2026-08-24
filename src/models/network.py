from typing import Dict, List, Optional
from src.models.connection import Connection
from src.models.zone import Zone


class Network:

    def __init__(
        self,
        zones: Dict[str, Zone],
        connections: List[Connection],
        start_hub: Zone,
        end_hub: Zone
    ) -> None:
        self.zones: Dict[str, Zone] = zones
        self.connections: List[Connection] = connections
        self.start_hub: Zone = start_hub
        self.end_hub: Zone = end_hub

    def get_neighbors(self, zone: Zone) -> List[Zone]:
        neighbors: List[Zone] = []
        for conn in self.connections:
            dest = conn.get_destination(zone)
            if dest is not None and dest.zone_type != "blocked":
                neighbors.append(dest)
        return neighbors

    def get_connection(
        self, zone1: Zone, zone2: Zone
    ) -> Optional[Connection]:
        for conn in self.connections:
            if (
                (conn.zone1.name == zone1.name and
                 conn.zone2.name == zone2.name) or
                (conn.zone1.name == zone2.name and
                 conn.zone2.name == zone1.name)
            ):
                return conn
        return None
