""" Custom errors for stikb """


class StikbError(Exception):
    """Base class for exceptions in this module."""

    pass


class NoStikbRathInContextError(StikbError):
    """Raised when there is no StikbRath in the context"""

    pass
