from typing import Dict, List, Optional
from src.models import Drone, Network, Zone
from src.simulation.pathfinder import PathFinder


class SimulationEngine:

    def __init__(self, network: Network, drones: List[Drone]) -> None:
        self.network: Network = network
        self.drones: List[Drone] = drones
        self.pathfinder: PathFinder = PathFinder(network)

        self.routes: Dict[int, List[Zone]] = {}
        self.route_indices: Dict[int, int] = {}

    def setup(self) -> bool:
        available_paths = self.pathfinder.find_multiple_paths(
            self.network.start_hub, self.network.end_hub
        )
        if not available_paths:
            return False

        path_loads = [0] * len(available_paths)
        for drone in self.drones:
            best_path_idx = min(
                range(len(available_paths)),
                key=lambda i: len(available_paths[i]) + path_loads[i],
            )
            self.routes[drone.id] = available_paths[best_path_idx]
            self.route_indices[drone.id] = 0
            path_loads[best_path_idx] += 1

        self.network.start_hub.current_drones_count = len(self.drones)
        return True

    def _get_next_zone(self, drone: Drone) -> Optional[Zone]:
        route = self.routes.get(drone.id, [])
        idx = self.route_indices.get(drone.id, 0)
        if idx + 1 < len(route):
            return route[idx + 1]
        return None

    def run(self) -> int:
        if not self.setup():
            print("Error: There is no route between start_hub and end_hub.")
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

                # 1. Procesar segundo turno en zona restricted
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

                            if drone.current_zone == self.network.end_hub:
                                drone.is_delivered = True
                    continue

                # 2. Intentar nuevo avance
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
                    origin_zone = drone.current_zone
                    origin_zone.current_drones_count -= 1
                    link_capacity_used[conn_key] = current_link_usage + 1
                    self.route_indices[drone.id] += 1

                    if next_zone.zone_type == "restricted":
                        # Turno 1 en zona restricted
                        drone.in_transit = True
                        drone.destination_zone = next_zone
                        drone.turns_remaining_in_transit = 1
                        next_zone.current_drones_count += 1

                        moves_this_turn.append(
                            f"{drone.name}-{origin_zone.name}-{next_zone.name}"
                        )
                    else:
                        # Zona normal o priority
                        drone.current_zone = next_zone
                        next_zone.current_drones_count += 1

                        moves_this_turn.append(
                            f"{drone.name}-{drone.current_zone.name}"
                        )

                        if drone.current_zone == self.network.end_hub:
                            drone.is_delivered = True

            if moves_this_turn:
                print(" ".join(moves_this_turn))

        return turn
