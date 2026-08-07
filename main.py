import os
import sys
from typing import List, Optional
from src.models import Drone, Network
from src.parser import MapParser, MapParserError
from src.simulation import SimulationEngine
from src.visualization import Visualizer


def list_available_maps(maps_dir: str = "maps") -> List[str]:
    """Obtiene la lista de mapas .txt buscando en subcarpetas."""
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
    """Muestra un menú para seleccionar un mapa de forma interactiva."""
    maps = list_available_maps(maps_dir)
    if not maps:
        print(f"Error: No se encontraron archivos .txt en '{maps_dir}'.")
        return None

    print(f"--- Mapas disponibles en '{maps_dir}' ---")
    for idx, map_file in enumerate(maps, 1):
        print(f"  [{idx:>2}] {map_file}")
    print("----------------------------------------")

    while True:
        try:
            prompt = f"Seleccione un mapa (1-{len(maps)}) o 'q' para salir: "
            user_input = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperación cancelada.")
            return None

        if user_input.lower() == 'q':
            return None

        if user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= len(maps):
                return os.path.join(maps_dir, maps[choice - 1])

        print("Selección no válida. Intente de nuevo.")


def get_map_path() -> Optional[str]:
    """Obtiene la ruta del mapa desde los argumentos o de forma interactiva."""
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
            print("Error: El mapa no define start_hub o end_hub.")
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
            print("Error: No se pudo completar la simulación.")
            sys.exit(1)

    except MapParserError as e:
        print(f"Error de parseo: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado durante la ejecución: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
