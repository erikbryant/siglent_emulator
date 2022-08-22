![Code Formatter](https://github.com/erikbryant/siglent_emulator/actions/workflows/formatter.yml/badge.svg)
![Type Checking](https://github.com/erikbryant/siglent_emulator/actions/workflows/mypy.yml/badge.svg)
![Pylint](https://github.com/erikbryant/siglent_emulator/actions/workflows/pylint.yml/badge.svg)
![Tests](https://github.com/erikbryant/siglent_emulator/actions/workflows/tests.yml/badge.svg)

# Siglent Emulator

Software emulator for [Siglent Technologies](https://siglentna.com/) test and measurement equipment. Use the emulator to test your code before deploying. The emulator is written in Python, but your code can be in any language.

# Supported Equipment

## Siglent Function Generator

* SDG1000x series

## Siglent Oscilloscope

* Coming soon!

# Using the Emulator to test Your Code

The emulator mimics your Siglent device. Start the emulator.

```python
from siglent_emulator import emulator

PORT=21111
emulator.start(port=PORT, daemon=True)
```

Then execute your code giving the IP address and port of the emulator. Your code will behave just as if it was talking to a physical Siglent device. For instance, if you have a Python source file named `siglent_device` that has a class `Amplitude` you could write a test like this:

```python
  IP_ADDR="127.0.0.1"

  device = siglent_device.Amplitude()
  device.connect(ip_addr=IP_ADDR, port=PORT)
  device.set_amplitude(channel=1, amplitude=13.67)
  self.assertEqual(device.get_amplitude(channel=1), 13.67)
  device.close()
```

Look in the [examples](examples) directory for a fully working example that uses the Python unittest framework.

# Contributing to the Emulator

Pull requests are welcome!

## Testing the emulator

From the root directory of your checkout, type:

```shell
make all
```
