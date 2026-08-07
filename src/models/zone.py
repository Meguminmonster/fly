from typing import Union


class Zone:
    """Representa un hub o nodo en la red de movimiento de drones."""

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: str = "normal",
        color: str = "none",
        max_drones: int = 1,
        is_start: bool = False,
        is_end: bool = False,
    ) -> None:
        """Inicializa una zona con sus propiedades y restricciones."""
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.zone_type: str = zone_type
        self.color: str = color
        self.is_start: bool = is_start
        self.is_end: bool = is_end

        self.max_drones: Union[int, float] = (
            float("inf") if (is_start or is_end) else max_drones
        )
        self.current_drones_count: int = 0

    def can_enter(self) -> bool:
        """Comprueba si un dron puede ingresar a esta zona."""
        if self.zone_type == "blocked":
            return False
        return self.current_drones_count < self.max_drones

    def __repr__(self) -> str:
        """Representación legible del objeto Zone."""
        return f"Zone(name='{self.name}', type='{self.zone_type}')"
