"""Functions common to SDG1000X Siglent function generators."""

import logging

from siglent_emulator.function_generator import sdg_common

# pylint: disable=fixme


class SDG1000XChannel(sdg_common.SDGChannel):
    """Emulate a function generator output channel."""


class SDG1000X(sdg_common.SDG):
    """Emulate a Siglent function generator."""

    def operation_complete(self, _: str) -> str:
        """Process the command, update state, optionally return a result."""
        # TODO: implement
        return ""

    def comm_header(self, _: str) -> str:
        """Process the command, update state, optionally return a result."""
        # The SDG1000X series does not implement this command
        return ""

    def parameter_copy(self, command: str) -> str:
        """Process the command, update state, optionally return a result."""
        # TODO: implement
        return sdg_common.SDG.parameter_copy(self, command=command)

    def store_list(self, command: str) -> str:
        """Process the command, update state, optionally return a result."""
        # TODO: implement
        return sdg_common.SDG.store_list(self, command=command)


errlog = logging.getLogger(__name__)
