from src.models import Network


class Visualizer:

    def __init__(self, network: Network) -> None:
        self.network: Network = network

    def print_map_summary(self) -> None:
        print("========================================")
        print("      SUMMARY OF THE DRONE NETWORK      ")
        print("========================================")
        print(f"Start Hub        : {self.network.start_hub.name}")
        print(f"End Hub          : {self.network.end_hub.name}")
        print(f"Total Zones      : {len(self.network.zones)}")
        print(f"Total Connections: {len(self.network.connections)}")
        print("----------------------------------------")
        print("Registered Areas:")
        for zone in self.network.zones.values():
            print(
                f"  - {zone.name:<12} (x:{zone.x:>2}, y:{zone.y:>2}) | "
                f"Type: {zone.zone_type:<10} | Capacity: {zone.max_drones}"
            )
        print("========================================\n")

    def print_simulation_start(self, nb_drones: int) -> None:
        print(f"Starting simulation with {nb_drones} drones...\n")

    def print_simulation_end(self, total_turns: int) -> None:
        print("\n========================================")
        print("    SIMULATION SUCCESSFULLY COMPLETED     ")
        print("========================================")
        print(f"Total time spent: {total_turns} turns")
        print("========================================")
