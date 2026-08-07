from typing import Optional
from src.models.zone import Zone


class Drone:
    """Representa un dron individual con su posición y estado de vuelo."""

    def __init__(self, drone_id: int, current_zone: Zone) -> None:
        """Inicializa un dron en una zona de partida."""
        self.id: int = drone_id
        self.name: str = f"D{drone_id}"
        self.current_zone: Zone = current_zone

        self.in_transit: bool = False
        self.destination_zone: Optional[Zone] = None
        self.turns_remaining_in_transit: int = 0

    @property
    def is_delivered(self) -> bool:
        """Indica si el dron ha llegado al objetivo final."""
        return self.current_zone.is_end and not self.in_transit

    def __repr__(self) -> str:
        """Representación legible del objeto Drone."""
        return f"Drone(name='{self.name}', zone='{self.current_zone.name}')"
