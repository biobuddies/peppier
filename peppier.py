"""Python utilities including PEP-8 wrappers."""

from textwrap import dedent


def undent(string: str) -> str:
    """Dedent, then strip the leading newline of a triple-quoted literal."""
    return dedent(string).lstrip()
