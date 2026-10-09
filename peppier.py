"""Python utilities including PEP-8 wrappers."""

from collections.abc import Mapping
from textwrap import dedent


def compact[K, V](mapping: Mapping[K, V | None], /) -> dict[K, V]:
    """Copy mapping, dropping None values but keeping other falsy values."""
    return {key: value for key, value in mapping.items() if value is not None}


def identity[T](value: T, /) -> T:
    """Return value unchanged, for interfaces requiring a function."""
    return value


def undent(string: str) -> str:
    """Dedent, then strip the leading newline of a triple-quoted literal."""
    return dedent(string).lstrip()
