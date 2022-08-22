"""Emulate an SDG1062X Siglent function generator.

This model is identical to the SDG1032X with the exception of identification()."""

from siglent_emulator.function_generator import sdg1032x


class SDG1062X(sdg1032x.SDG1032X):
    """Emulate a Siglent function generator."""

    def identification(self) -> str:
        """Process the command, update state, optionally return a result."""
        return "Siglent Technologies,SDG1062X,SDG1XCBD5R6027,1.01.01.33R1B6"


def new() -> SDG1062X:
    """Return an instance of this device."""
    return SDG1062X()
