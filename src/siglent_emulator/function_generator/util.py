"""Functions common across multiple Siglent devices."""

import logging
from typing import Dict, List

# pylint: disable=broad-except


Short_to_long: Dict[str, str] = {
    "*IDN?": "*IDN?",
    "*OPC?": "*OPC?",
    "*RST": "*RST",
    "CHDR": "COMM_HEADER",
    "OUTP": "OUTPUT",
    "C1": "C1",
    "C2": "C2",
    "SYST": "SYSTEM",
    "SRATE": "SAMPLERATE",
    "SRATE?": "SAMPLERATE?",
    "COMM": "COMMUNICATE",
    "LAN": "LAN",
    "IPAD": "IPADDRESS",
    "IPAD?": "IPADDRESS?",
}

Long_to_short: Dict[str, str] = {long: short for (short, long) in Short_to_long.items()}


def resize_verbs(command: str, resizer: Dict[str, str]) -> str:
    """Given a command, replace the command verb with its alternate form."""
    if command == "":
        return command
    command = command.strip().upper()
    params = command.split(" ")
    resized_verbs: List[str] = []
    for verb in params[0].split(":"):
        if verb in resizer:
            resized_verbs.append(resizer[verb])
        else:
            resized_verbs.append(verb)
    params[0] = ":".join(resized_verbs)
    command = " ".join(params)
    return command


def shorten_verbs(command: str) -> str:
    """Replace the command verbs with their short form."""
    return resize_verbs(command=command, resizer=Long_to_short)


def lengthen_verbs(command: str) -> str:
    """Replace the command verbs with their long form."""
    return resize_verbs(command=command, resizer=Short_to_long)


def strip_verbs(command: str) -> str:
    """Remove the command verbs."""
    command = command.strip().upper()
    params = command.split(" ")
    if len(params) <= 1:
        return ""
    return " ".join(params[1:])


def format_verbs(command: str, length: str) -> str:
    """Replace the command verb with its short form, long form, or none."""
    if length == "OFF":
        return strip_verbs(command)
    if length == "LONG":
        return lengthen_verbs(command=command)
    return shorten_verbs(command=command)


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
