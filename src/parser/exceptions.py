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

    pass


class InvalidZoneTypeError(MapParserError):

    pass


class InvalidCoordinateError(MapParserError):

    pass


class MissingHubError(MapParserError):

    pass


class DuplicateConnectionError(MapParserError):

    pass
