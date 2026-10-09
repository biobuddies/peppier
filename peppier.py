"""Python utilities including PEP-8 wrappers."""

from collections.abc import Mapping
from textwrap import dedent


def compact[K, V](
    mapping: Mapping[K, V | None] | None = None, /, **kwargs: V | None
) -> dict[K | str, V]:
    """Build a dict like dict(), dropping None, '', and b'' values.

    Keep other falsy values like 0, False, and []. Django and type-annotated code favor '' over
    None for absent strings. This rule is the best forecast balance of usability; revisit as real
    usage examples accrue.
    """
    return {
        key: value
        for key, value in {**(mapping or {}), **kwargs}.items()
        if value is not None and not (isinstance(value, str | bytes) and not value)
    }


def identity[T](value: T, /) -> T:
    """Return value unchanged, for interfaces requiring a callable."""
    return value


def undent(string: str) -> str:
    """Dedent, then strip the leading newline of a triple-quoted literal."""
    return dedent(string).lstrip()
