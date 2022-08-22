"""Python unittests."""

import unittest

from siglent_emulator import emulator

import siglent_device

IP_ADDR="127.0.0.1"
PORT=21111

class Test(unittest.TestCase):
    """Test cases."""

    @classmethod
    def setUpClass(cls):
        emulator.start(port=PORT, daemon=True)

    def test_set_amplitude(self):
        """Confirm the amplitude we set was actually set."""
        device = siglent_device.Amplitude()
        device.connect(ip_addr=IP_ADDR, port=PORT)
        device.set_amplitude(channel=1, amplitude=13.67)
        self.assertEqual(device.get_amplitude(channel=1), 13.67)
        device.close()

if __name__ == "__main__":
    unittest.main()
