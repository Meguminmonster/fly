class MapParserError(Exception):

    def __init__(
        self,
        message: str,
        line_number: int = -1,
        line_content: str = ""
    ) -> None:

        self.message: str = message
        self.line_number: int = line_number
        self.line_content: str = line_content

        full_message = "Parsing Error"
        if line_number > 0:
            full_message += f" on line {line_number}"
        full_message += f": {message}"

        if line_content:
            full_message += f"\n -> Content: '{line_content}'"

        super().__init__(full_message)


class InvalidMapSyntaxError(MapParserError):
    """Se lanza cuando una línea no es el formato esperado."""

    pass


class InvalidZoneTypeError(MapParserError):
    """Se lanza cuando el tipo de zona no es válido."""

    pass


class InvalidCoordinateError(MapParserError):
    """Se lanza cuando las coordenadas no son números enteros."""

    pass


class MissingHubError(MapParserError):
    """Se lanza si falta el start_hub o el end_hub al finalizar la lectura."""

    pass


class DuplicateConnectionError(MapParserError):
    """Se lanza cuando se intenta crear una conexión que ya existe."""

    pass
