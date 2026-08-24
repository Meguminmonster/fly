from typing import Optional
from src.models.zone import Zone


class Drone:

    def __init__(self, drone_id: int, current_zone: Zone) -> None:
        self.id: int = drone_id
        self.name: str = f"D{drone_id}"
        self.current_zone: Zone = current_zone

        self.in_transit: bool = False
        self.destination_zone: Optional[Zone] = None
        self.turns_remaining_in_transit: int = 0
        self._is_delivered: bool = False

    @property
    def is_delivered(self) -> bool:
        return self._is_delivered or (
            self.current_zone.is_end and not self.in_transit
        )

    @is_delivered.setter
    def is_delivered(self, value: bool) -> None:
        """Permite modificar directamente el estado de entrega."""
        self._is_delivered = value

    def __repr__(self) -> str:
        """Representación legible del objeto Drone."""
        return f"Drone(name='{self.name}', zone='{self.current_zone.name}')"
