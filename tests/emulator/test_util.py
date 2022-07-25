"""Tests."""

import unittest

from siglent_emulator.function_generator import util


class Test(unittest.TestCase):
    """Test cases."""

    def test_0_channel_to_index(self) -> None:
        """Can successfully compute the channel number."""
        self.assertEqual(util.channel_to_index("C1"), 0)

    def test_1_channel_to_index(self) -> None:
        """Returns -1 on error."""
        self.assertEqual(util.channel_to_index("foo"), -1)


if __name__ == "__main__":
    unittest.main()
