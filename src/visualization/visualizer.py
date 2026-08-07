from src.models import Network


class Visualizer:
    """Visualizador para representar el estado de la red y de la simulación."""

    def __init__(self, network: Network) -> None:
        """Inicializa el visualizador con la red del mapa.

        Args:
            network: Objeto Network con la información de zonas y conexiones.
        """
        self.network: Network = network

    def print_map_summary(self) -> None:
        """Imprime un resumen formateado de la estructura de la red."""
        print("========================================")
        print("         RESUMEN DE LA RED DE DRONES    ")
        print("========================================")
        print(f"Start Hub       : {self.network.start_hub.name}")
        print(f"End Hub         : {self.network.end_hub.name}")
        print(f"Total Zonas     : {len(self.network.zones)}")
        print(f"Total Conexiones: {len(self.network.connections)}")
        print("----------------------------------------")
        print("Zonas registradas:")
        for zone in self.network.zones.values():
            print(
                f"  - {zone.name:<12} (x:{zone.x:>2}, y:{zone.y:>2}) | "
                f"Tipo: {zone.zone_type:<10} | Capacidad: {zone.max_drones}"
            )
        print("========================================\n")

    def print_simulation_start(self, nb_drones: int) -> None:
        """Imprime la cabecera de inicio de la simulación.

        Args:
            nb_drones: Número total de drones a desplegar.
        """
        print(f"Iniciando simulación con {nb_drones} drones...\n")

    def print_simulation_end(self, total_turns: int) -> None:
        """Imprime el resumen de finalización de la simulación.

        Args:
            total_turns: Cantidad total de turnos que tomó la entrega.
        """
        print("\n========================================")
        print("       SIMULACIÓN FINALIZADA CON ÉXITO  ")
        print("========================================")
        print(f"Tiempo total empleado: {total_turns} turnos")
        print("========================================")
