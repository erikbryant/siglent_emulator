"""Emulate an SDG1062X Siglent function generator.

This model is identical to the SDG1032X with the exception of identification()."""

import logging

from siglent_emulator.function_generator import sdg1032x


class SDG1062XChannel(sdg1032x.SDG1032XChannel):
    """Emulate a function generator output channel."""


class SDG1062X(sdg1032x.SDG1032X):
    """Emulate a Siglent function generator."""

    channels = [SDG1062XChannel(1), SDG1062XChannel(2)]

    def identification(self) -> str:
        """Process the command, update state, optionally return a result."""
        return "Siglent Technologies,SDG1062X,SDG1XCBD5R6027,1.01.01.33R1B6"


errlog = logging.getLogger(__name__)
