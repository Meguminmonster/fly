from typing import Dict, List, Optional, Tuple
from src.models.connection import Connection
from src.models.zone import Zone
from src.parser.exceptions import (
    DuplicateConnectionError,
    InvalidCoordinateError,
    InvalidMapSyntaxError,
    InvalidZoneTypeError,
    MapParserError,
    MissingHubError,
)


class MapParser:

    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
        self.nb_drones: int = 0
        self.zones: Dict[str, Zone] = {}
        self.connections: List[Connection] = []

        self.start_hub: Optional[Zone] = None
        self.end_hub: Optional[Zone] = None

        self.VALID_ZONE_TYPES = {
            "normal", "blocked", "restricted", "priority"
        }

    def _parse_metadata(self, metadata_str: str) -> Dict[str, str]:
        """Extrae metadatos de formato 'key=value'."""
        metadata: Dict[str, str] = {}
        if not metadata_str:
            return metadata
        for pair in metadata_str.split():
            if '=' in pair:
                key, value = pair.split('=', 1)
                metadata[key] = value
        return metadata

    def _parse_zone(self, line: str, line_num: int) -> None:
        """Parsea una zona y la añade al diccionario self.zones."""
        parts = line.split('[', 1)
        base = parts[0].strip()
        meta_str = (
            parts[1].replace(']', '').strip() if len(parts) > 1 else ""
        )

        tokens = base.replace(':', ' ').split()
        if len(tokens) < 4:
            raise InvalidMapSyntaxError(
                "Definition of an incomplete zone.", line_num, line
            )

        prefix, name = tokens[0], tokens[1]

        if '-' in name:
            raise InvalidMapSyntaxError(
                "Zone names cannot contain hyphens.",
                line_num,
                line
            )

        if name in self.zones:
            raise InvalidMapSyntaxError(
                f"The ‘{name}’ zone is already defined.", line_num, line
            )

        try:
            x, y = int(tokens[2]), int(tokens[3])
        except ValueError:
            raise InvalidCoordinateError(
                f"Invalid coordinates for '{name}'.", line_num, line
            )

        meta = self._parse_metadata(meta_str)
        zone_type = meta.get('zone', 'normal')

        if zone_type not in self.VALID_ZONE_TYPES:
            raise InvalidZoneTypeError(
                f"Zone type '{zone_type}' not allowed.",
                line_num,
                line
            )

        color = meta.get('color', 'none')
        try:
            max_drones = int(meta.get('max_drones', 1))
            if max_drones <= 0:
                raise ValueError()
        except ValueError:
            raise InvalidMapSyntaxError(
                "max_drones must be a positive.",
                line_num,
                line
            )

        is_start = (prefix == "start_hub")
        is_end = (prefix == "end_hub")

        new_zone = Zone(
            name, x, y, zone_type, color, max_drones, is_start, is_end
        )
        self.zones[name] = new_zone

        if is_start:
            if self.start_hub:
                raise InvalidMapSyntaxError(
                    "There cannot be more than one start_hub.", line_num, line
                )
            self.start_hub = new_zone

        if is_end:
            if self.end_hub:
                raise InvalidMapSyntaxError(
                    "There cannot be more than one end_hub.", line_num, line
                )
            self.end_hub = new_zone

    def _parse_connection(self, line: str, line_num: int) -> None:
        """Parsea una conexión y verifica que no esté duplicada."""
        parts = line.split('[', 1)
        base = parts[0].strip()
        meta_str = (
            parts[1].replace(']', '').strip() if len(parts) > 1 else ""
        )

        tokens = base.replace(':', ' ').split()
        if len(tokens) < 2:
            raise InvalidMapSyntaxError(
                "Incomplete connection.", line_num, line
            )

        link_str = tokens[1]
        if '-' not in link_str:
            raise InvalidMapSyntaxError(
                "Invalid connection format (missing '-').",
                line_num,
                line
            )

        z1_name, z2_name = link_str.split('-', 1)

        if z1_name not in self.zones or z2_name not in self.zones:
            raise InvalidMapSyntaxError(
                "Connection to an Undefined Zone.", line_num, line
            )

        for conn in self.connections:
            if (
                (conn.zone1.name == z1_name and conn.zone2.name == z2_name)
                or (conn.zone1.name == z2_name and conn.zone2.name == z1_name)
            ):
                raise DuplicateConnectionError(
                    f"Duplicate connection: {link_str}", line_num, line
                )

        meta = self._parse_metadata(meta_str)
        try:
            max_link = int(meta.get('max_link_capacity', 1))
            if max_link <= 0:
                raise ValueError()
        except ValueError:
            raise InvalidMapSyntaxError(
                "max_link_capacity must be a positive.",
                line_num,
                line
            )

        new_connection = Connection(
            self.zones[z1_name], self.zones[z2_name], max_link
        )
        self.connections.append(new_connection)

    def parse(self) -> Tuple[int, Dict[str, Zone], List[Connection]]:
        """Función principal."""
        try:
            with open(self.filepath, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            raise MapParserError(
                f"The file could not be found: {self.filepath}"
            )

        found_nb_drones = False

        for i, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()

            if not line or line.startswith('#'):
                continue

            if not found_nb_drones:
                if not line.startswith("nb_drones:"):
                    raise InvalidMapSyntaxError(
                        "The first instruction should be 'nb_drones: <num>'.",
                        i,
                        line
                    )
                try:
                    self.nb_drones = int(line.split(':')[1].strip())
                    if self.nb_drones <= 0:
                        raise ValueError()
                except ValueError:
                    raise InvalidMapSyntaxError(
                        "nb_drones must be a positive.",
                        i,
                        line
                    )
                found_nb_drones = True
                continue

            if (
                line.startswith("start_hub:")
                or line.startswith("end_hub:")
                or line.startswith("hub:")
            ):
                self._parse_zone(line, i)
            elif line.startswith("connection:"):
                self._parse_connection(line, i)
            else:
                raise InvalidMapSyntaxError(
                    "Unknown prefix.", i, line
                )

        if not found_nb_drones:
            raise MapParserError("Instruction is missing 'nb_drones'")

        if not self.start_hub or not self.end_hub:
            raise MissingHubError(
                "The map must contain exactly one start_hub and one end_hub."
            )

        return self.nb_drones, self.zones, self.connections
