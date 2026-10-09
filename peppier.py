"""Python utilities including PEP-8 wrappers."""

from textwrap import dedent


def compact[V](**kwargs: V | None) -> dict[str, V]:
    """Build a dict from keyword arguments, dropping None values but keeping other falsy values."""
    return {key: value for key, value in kwargs.items() if value is not None}


def identity[T](value: T, /) -> T:
    """Return value unchanged, for interfaces requiring a function."""
    return value


def undent(string: str) -> str:
    """Dedent, then strip the leading newline of a triple-quoted literal."""
    return dedent(string).lstrip()
