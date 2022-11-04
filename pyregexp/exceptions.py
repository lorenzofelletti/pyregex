class PyregexpException(Exception):
    """Base class for all exceptions in this library."""
    pass


class BadTokenException(PyregexpException):
    """Exception raised when a bad token is found in the regular expression."""
    pass


class BadCurlyQuantifierException(PyregexpException):
    """Exception raised when a curly quantifier is not well formed."""
    pass


class MissingClosingBracketException(PyregexpException):
    """Exception raised when a closing bracket is missing."""

    def __init__(self, message="Missing closing ']'."):
        super().__init__(message)


class ReversedRangeException(PyregexpException):
    """Exception raised when a range is not well formed."""

    def __init__(self, message="Range is not well formed."):
        super().__init__(message)

    def __init__(self, char1, char2) -> None:
        super().__init__(
            f"Raversed range values. Start '{char1}' char code is greater than end '{char2}' char code.")


class UnterminatedGroupException(PyregexpException):
    """Exception raised when a group is not terminated."""

    def __init__(self, message="Unterminated group."):
        super().__init__(message)

    def __init__(self, index: int, message="Unterminated group.") -> None:
        super().__init__(message + f" near ${index}.")


class UnterminatedNamedGroupNameException(PyregexpException):
    """Exception raised when a named group is not terminated."""

    def __init__(self, message="Unterminated named group name."):
        super().__init__(message)


class ParsingException(PyregexpException):
    """Exception raised when a parsing error occurs."""
    pass
