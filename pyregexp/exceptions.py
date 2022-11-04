class PyregexpException(Exception):
    """Base class for all exceptions in this library."""
    pass

class LexerException(PyregexpException):
    """Base class for all lexer exceptions in this library."""
    pass

class BadTokenException(LexerException):
    """Exception raised when a bad token is found in the regular expression."""
    pass

class BadCurlyQuantifierException(LexerException):
    """Exception raised when a curly quantifier is not well formed."""
    pass

class ParserException(PyregexpException):
    """Base class for all parser exceptions in this library."""
    pass
