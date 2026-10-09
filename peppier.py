"""Python utilities including PEP-8 wrappers."""

from collections.abc import Iterable, Mapping
from textwrap import dedent


def compact[K, V](items: Mapping[K, V | None] | Iterable[tuple[K, V | None]], /) -> dict[K, V]:
    """Build a dict like dict(), dropping None values but keeping other falsy values."""
    return {key: value for key, value in dict(items).items() if value is not None}


def identity[T](value: T, /) -> T:
    """Return value unchanged, for interfaces requiring a function."""
    return value


def undent(string: str) -> str:
    """Dedent, then strip the leading newline of a triple-quoted literal."""
    return dedent(string).lstrip()
