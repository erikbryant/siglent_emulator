"""Emulate an SDG1032X Siglent function generator."""

import logging

from siglent_emulator.function_generator import sdg1000x_series

# pylint: disable=fixme


class SDG1032XChannel(sdg1000x_series.SDG1000XChannel):
    """Emulate a function generator output channel."""

    def outp(self, command: str) -> str:
        """Proccess all variants of the OUTP command."""
        # TODO: implement
        return sdg1000x_series.SDG1000XChannel.outp(self, command)

    def bswv(self, command: str) -> str:
        """Proccess all variants of the BSWV command."""
        # TODO: implement
        return sdg1000x_series.SDG1000XChannel.bswv(self, command)


class SDG1032X(sdg1000x_series.SDG1000X):
    """Emulate a Siglent function generator."""

    channels = [SDG1032XChannel(channel=1), SDG1032XChannel(channel=2)]

    def identification(self) -> str:
        """Process the command, update state, optionally return a result."""
        return "Siglent Technologies,SDG1032X,SDG1XCBD5R6027,1.01.01.33R1B6"


def new() -> SDG1032X:
    """Return an instance of this device."""
    return SDG1032X()


errlog = logging.getLogger(__name__)
