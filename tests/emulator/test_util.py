"""Tests."""

import unittest

from siglent_emulator.function_generator import util


class Test(unittest.TestCase):
    """Test cases."""

    def test_0_channel_to_index(self) -> None:
        """Can successfully compute the channel number."""
        self.assertEqual(util.channel_to_index(channel="C1"), 0)

    def test_1_channel_to_index(self) -> None:
        """Returns -1 on error."""
        self.assertEqual(util.channel_to_index(channel="foo"), -1)

    def test_0_long_to_short(self) -> None:
        """Verify Long_to_short is the inverse of Short_to_long."""
        for key, val in util.Short_to_long.items():
            self.assertEqual(util.Long_to_short[val], key)
        for key, val in util.Long_to_short.items():
            self.assertEqual(util.Short_to_long[val], key)

    def test_0_shorten_verbs(self) -> None:
        """Uppercase one param."""
        command = "*rSt"
        self.assertEqual(util.shorten_verbs(command=command), "*RST")

    def test_1_shorten_verbs(self) -> None:
        """Uppercase multiparams."""
        command = "c1:OuTpUT LOAD,hz"
        self.assertEqual(util.shorten_verbs(command=command), "C1:OUTP LOAD,HZ")

    def test_2_shorten_verbs(self) -> None:
        """Unknown command verb."""
        command = "xYzzY LOAD,hz"
        self.assertEqual(util.shorten_verbs(command=command), "XYZZY LOAD,HZ")

    def test_3_shorten_verbs(self) -> None:
        """Multi-verb command."""
        command = "C1:OutPUT LOAD,hz"
        self.assertEqual(util.shorten_verbs(command=command), "C1:OUTP LOAD,HZ")

    def test_4_shorten_verbs(self) -> None:
        """Multi-verb command no params."""
        command = "SYSTem:COMMunicate:LAN:IPADdress?"
        self.assertEqual(util.shorten_verbs(command=command), "SYST:COMM:LAN:IPAD?")

    def test_0_format_verbs(self) -> None:
        """length==OFF, verb-only"""
        command = "*RST"
        self.assertEqual(util.format_verbs(command=command, length="OFF"), "")

    def test_1_format_verbs(self) -> None:
        """length==OFF, verb-query-only"""
        command = "*IDN?"
        self.assertEqual(util.format_verbs(command=command, length="OFF"), "")

    def test_2_format_verbs(self) -> None:
        """length==OFF, multi-verb"""
        command = "SYSTem:COMMunicate:LAN:IPADdress"
        self.assertEqual(util.format_verbs(command=command, length="OFF"), "")

    def test_3_format_verbs(self) -> None:
        """length==OFF, multi-verb with params"""
        command = "SYSTem:COMMunicate:LAN:IPADdress 1,2"
        self.assertEqual(util.format_verbs(command=command, length="OFF"), "1,2")

    def test_4_format_verbs(self) -> None:
        """length==LONG, verb-only"""
        command = "CHDR"
        self.assertEqual(
            util.format_verbs(command=command, length="LONG"), "COMM_HEADER"
        )

    def test_5_format_verbs(self) -> None:
        """length==LONG, verb-query-only"""
        command = "SRATE?"
        self.assertEqual(
            util.format_verbs(command=command, length="LONG"), "SAMPLERATE?"
        )

    def test_6_format_verbs(self) -> None:
        """length==LONG, multi-verb"""
        command = "SYST:COMM:LAN:IPAD"
        self.assertEqual(
            util.format_verbs(command=command, length="LONG"),
            "SYSTEM:COMMUNICATE:LAN:IPADDRESS",
        )

    def test_7_format_verbs(self) -> None:
        """length==LONG, multi-verb with params"""
        command = "SYST:COMM:LAN:IPAD 1,2"
        self.assertEqual(
            util.format_verbs(command=command, length="LONG"),
            "SYSTEM:COMMUNICATE:LAN:IPADDRESS 1,2",
        )


if __name__ == "__main__":
    unittest.main()
