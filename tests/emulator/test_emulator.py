"""Tests."""

import logging
import unittest

from siglent_emulator import emulator

logging.basicConfig(level=logging.CRITICAL)


class Test(unittest.TestCase):
    """Test cases."""

    def test_0___init__(self) -> None:
        """Can start a supported emulator."""
        emulator.start(device="SDG1032X", daemon=True)

    def test_1___init__(self) -> None:
        """Fails to start an unsupported emulator."""
        with self.assertRaises(KeyError):
            emulator.start(device="ABC1000", daemon=False)


if __name__ == "__main__":
    unittest.main()
