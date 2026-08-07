from typing import Dict, List, Optional
from src.models import Drone, Network, Zone
from src.simulation.pathfinder import PathFinder


class SimulationEngine:
    """Gestor del ciclo de vida y la ejecución de la simulación."""

    def __init__(self, network: Network, drones: List[Drone]) -> None:
        """Inicializa el motor de simulación."""
        self.network: Network = network
        self.drones: List[Drone] = drones
        self.pathfinder: PathFinder = PathFinder(network)

        self.routes: Dict[int, List[Zone]] = {}
        self.route_indices: Dict[int, int] = {}

    def setup(self) -> bool:
        """Calcula las rutas iniciales para todos los drones."""
        path = self.pathfinder.find_shortest_path(
            self.network.start_hub, self.network.end_hub
        )
        if not path:
            return False

        for drone in self.drones:
            self.routes[drone.id] = path
            self.route_indices[drone.id] = 0

        self.network.start_hub.current_drones_count = len(self.drones)
        return True

    def _get_next_zone(self, drone: Drone) -> Optional[Zone]:
        """Devuelve la siguiente zona en la ruta de un dron."""
        route = self.routes.get(drone.id, [])
        idx = self.route_indices.get(drone.id, 0)
        if idx + 1 < len(route):
            return route[idx + 1]
        return None

    def run(self) -> int:
        """Ejecuta el bucle de simulación turno por turno."""
        if not self.setup():
            print("Error: No existe ruta entre start_hub y end_hub.")
            return 0

        turn = 0
        total_drones = len(self.drones)

        while True:
            delivered_count = sum(1 for d in self.drones if d.is_delivered)
            if delivered_count == total_drones:
                break

            turn += 1
            moves_this_turn: List[str] = []
            link_capacity_used: Dict[str, int] = {}

            for drone in self.drones:
                if drone.is_delivered:
                    continue

                if drone.in_transit:
                    drone.turns_remaining_in_transit -= 1
                    if drone.turns_remaining_in_transit == 0:
                        drone.in_transit = False
                        if drone.destination_zone:
                            drone.current_zone = drone.destination_zone
                            drone.destination_zone = None
                            moves_this_turn.append(
                                f"{drone.name}-{drone.current_zone.name}"
                            )
                    continue

                next_zone = self._get_next_zone(drone)
                if not next_zone:
                    continue

                conn = self.network.get_connection(
                    drone.current_zone, next_zone
                )

                if conn is None:
                    continue

                conn_key = f"{conn.zone1.name}<->{conn.zone2.name}"
                current_link_usage = link_capacity_used.get(conn_key, 0)

                if (
                    next_zone.can_enter()
                    and current_link_usage < conn.max_link_capacity
                ):
                    drone.current_zone.current_drones_count -= 1
                    link_capacity_used[conn_key] = current_link_usage + 1
                    self.route_indices[drone.id] += 1

                    if next_zone.zone_type == "restricted":
                        drone.in_transit = True
                        drone.destination_zone = next_zone
                        drone.turns_remaining_in_transit = 1
                        next_zone.current_drones_count += 1
                    else:
                        drone.current_zone = next_zone
                        next_zone.current_drones_count += 1
                        moves_this_turn.append(
                            f"{drone.name}-{drone.current_zone.name}"
                        )

            if moves_this_turn:
                print(f"Turn {turn}: " + " ".join(moves_this_turn))

        return turn
