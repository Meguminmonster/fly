from typing import Optional
from src.models.zone import Zone


class Connection:
    """Representa una arista bidireccional entre dos zonas."""

    def __init__(
        self,
        zone1: Zone,
        zone2: Zone,
        max_link_capacity: int = 1
    ) -> None:
        self.zone1: Zone = zone1
        self.zone2: Zone = zone2
        self.max_link_capacity: int = max_link_capacity
        self.current_drones_in_transit: int = 0

    def get_destination(self, from_zone: Zone) -> Optional[Zone]:
        if from_zone.name == self.zone1.name:
            return self.zone2
        if from_zone.name == self.zone2.name:
            return self.zone1
        return None

    def can_traverse(self) -> bool:
        return self.current_drones_in_transit < self.max_link_capacity

    def __repr__(self) -> str:
        """Representación legible del objeto Connection."""
        return (
            f"Connection({self.zone1.name} <-> {self.zone2.name}, "
            f"capacity={self.max_link_capacity})"
        )
