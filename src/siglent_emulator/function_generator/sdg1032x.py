"""Emulate an SDG1032X Siglent function generator."""

import logging

from siglent_emulator.function_generator import sdg_series

# pylint: disable=fixme


class SDG1032XChannel(sdg_series.SDGChannel):
    """Emulate a function generator output channel."""

    def outp(self, command: str) -> str:
        """Proccess all variants of the OUTP command."""
        # TODO: implement
        return sdg_series.SDGChannel.outp(self, command)

    def bswv(self, command) -> str:
        """Proccess all variants of the BSWV command."""
        # TODO: implement
        return sdg_series.SDGChannel.bswv(self, command)


class SDG1032X(sdg_series.SDG):
    """Emulate a Siglent function generator."""

    channels = [SDG1032XChannel(1), SDG1032XChannel(2)]

    def identification(self) -> str:
        """Process the command, update state, optionally return a result."""
        return "Siglent Technologies,SDG1032X,SDG1XCBD5R6027,1.01.01.33R1B6"

    def operation_complete(self) -> str:
        """Process the command, update state, optionally return a result."""
        # TODO: implement
        return ""

    def comm_header(self) -> str:
        """Process the command, update state, optionally return a result."""
        # The SDG1000X series does not implement this command
        return ""

    def parameter_copy(self, command: str) -> str:
        """Process the command, update state, optionally return a result."""
        # TODO: implement
        return sdg_series.SDG.parameter_copy(self, command)

    def store_list(self, command: str) -> str:
        """Process the command, update state, optionally return a result."""
        # TODO: implement
        return sdg_series.SDG.store_list(self, command)


errlog = logging.getLogger(__name__)
