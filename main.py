import os
import sys
from typing import List, Optional
from src.models import Drone, Network
from src.parser import MapParser, MapParserError
from src.simulation import SimulationEngine
from src.visualization import Visualizer


def list_available_maps(maps_dir: str = "maps") -> List[str]:
    map_files: List[str] = []
    if not os.path.exists(maps_dir) or not os.path.isdir(maps_dir):
        return map_files

    for root, _, files in os.walk(maps_dir):
        for file in files:
            if file.endswith(".txt"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, maps_dir)
                map_files.append(rel_path)

    return sorted(map_files)


def select_map_interactively(maps_dir: str = "maps") -> Optional[str]:
    maps = list_available_maps(maps_dir)
    if not maps:
        print(f"Error: No .txt files were found in '{maps_dir}'.")
        return None

    print(f"--- Maps available at '{maps_dir}' ---")
    for idx, map_file in enumerate(maps, 1):
        print(f"  [{idx:>2}] {map_file}")
    print("----------------------------------------")

    while True:
        try:
            prompt = f"Select a map (1-{len(maps)}) or 'q' to cancel: "
            user_input = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperation canceled.")
            return None

        if user_input.lower() == 'q':
            return None

        if user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= len(maps):
                return os.path.join(maps_dir, maps[choice - 1])

        print("Invalid selection. Please try again.")


def get_map_path() -> Optional[str]:
    if len(sys.argv) >= 2:
        return sys.argv[1]
    return select_map_interactively()


def main() -> None:
    """Coordinador principal de la carga del mapa y simulación."""
    map_path = get_map_path()
    if not map_path:
        sys.exit(0)

    try:
        parser = MapParser(map_path)
        nb_drones, zones, connections = parser.parse()

        if not parser.start_hub or not parser.end_hub:
            print("Error: The map does not define start_hub or end_hub.")
            sys.exit(1)

        network = Network(
            zones, connections, parser.start_hub, parser.end_hub
        )
        drones = [Drone(i + 1, parser.start_hub) for i in range(nb_drones)]

        visualizer = Visualizer(network)
        visualizer.print_map_summary()
        visualizer.print_simulation_start(nb_drones)

        engine = SimulationEngine(network, drones)
        total_turns = engine.run()

        if total_turns > 0:
            visualizer.print_simulation_end(total_turns)
        else:
            print("Error: The simulation could not be completed.")
            sys.exit(1)

    except MapParserError as e:
        print(f"Parsing error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during executionn: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
