![Code Formatter](https://github.com/erikbryant/siglent_emulator/actions/workflows/formatter.yml/badge.svg)
![Type Checking](https://github.com/erikbryant/siglent_emulator/actions/workflows/mypy.yml/badge.svg)
![Pylint](https://github.com/erikbryant/siglent_emulator/actions/workflows/pylint.yml/badge.svg)
![Tests](https://github.com/erikbryant/siglent_emulator/actions/workflows/tests.yml/badge.svg)

# Siglent Emulator

Software emulator for Siglent devices.

# Usage

The emulator mimics your Siglent device. Start the emulator.

```python
from siglent_emulator import emulator

PORT = 21111
emulator.start(port=PORT, daemon=True)
```

Then execute your code just as if you were talking to a physical Siglent device.

```python
    self.func_gen.connect(ip_addr="127.0.0.1", port=PORT)
    self.func_gen.set_amplitude(channel=1, amplitude=13.67)
    self.assertEqual(self.func_gen.get_amplitude(channel=1), 13.67)
    self.func_gen.close()
```

Here's a fully working example that uses the unittest framework.

```python
"""Tests."""

import unittest

from siglent_emulator import emulator

import my_siglent_func_gen as my_func_gen

PORT = 21111

class Test(unittest.TestCase):
    """Test cases."""

    func_gen = my_func_gen.FuncGen()

    @classmethod
    def setUpClass(cls):
        emulator.start(port=PORT, daemon=True)

    def test_set_amplitude(self):
        """Confirm the amplitude we set is actually set."""
        self.func_gen.connect(ip_addr="127.0.0.1", port=PORT)
        self.func_gen.set_amplitude(channel=1, amplitude=13.67)
        self.assertEqual(self.func_gen.get_amplitude(channel=1), 13.67)
        self.func_gen.close()

    def test_set_frequency(self):
        """Confirm the frequency we set is actually set."""
        self.func_gen.connect(ip_addr="127.0.0.1", port=PORT)
        self.func_gen.set_frequency(channel=2, frequency=54.9)
        self.assertEqual(self.func_gen.get_frequency(channel=2), 54.9)
        self.func_gen.close()

if __name__ == "__main__":
    unittest.main()
```
