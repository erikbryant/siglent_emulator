"""Functions common across multiple Siglent devices."""

import logging

# pylint: disable=broad-except


def channel_to_index(channel: str) -> int:
    """Given a string like 'C2' return the digit as an int (-1 on failure)."""
    try:
        chan = int(channel[1])
    except Exception as err:
        errlog.exception(err)
        return -1

    # Channels are 1-based, but the index is zero-based
    return chan - 1


def float_to_str(val: float) -> str:
    """Convert a float to a string with some pretty formatting."""
    if val == int(val):
        val = int(val)
    return f"{val:g}"


def sub(a: str, b: str) -> str:  # pylint: disable=invalid-name
    """Return a-b. All values are strings."""
    val = float(a) - float(b)
    return float_to_str(val=val)


def mul(a: str, b: str) -> str:  # pylint: disable=invalid-name
    """Return a*b. All values are strings."""
    val = float(a) * float(b)
    return float_to_str(val=val)


def div(n: str, d: str) -> str:  # pylint: disable=invalid-name
    """Return n/d using high precision. All values are strings."""
    if float(d) == 0:
        return "inf"
    places = 1e10
    val = (float(n) * places) / (float(d) * places)
    return float_to_str(val=val)


errlog = logging.getLogger(__name__)
