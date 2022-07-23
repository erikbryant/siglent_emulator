"""Tests."""

import unittest

from siglent_emulator.function_generator import sdg1032x


class Test(unittest.TestCase):
    """Test cases."""

    def test_0_channel_to_index(self):
        """Can successfully compute the channel number."""
        self.assertEqual(sdg1032x.channel_to_index("C1"), 0)

    def test_1_channel_to_index(self):
        """Returns -1 on error."""
        self.assertEqual(sdg1032x.channel_to_index("foo"), -1)


if __name__ == "__main__":
    unittest.main()
