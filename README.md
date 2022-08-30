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

# Installing the Emulator

```shell
python3 -m pip install git+https://github.com/erikbryant/siglent_emulator@0b5e28bfbc6506828f8323a2878d9af708678dd0
```

# Using the Emulator in Tests

The emulator mimics your Siglent device. Your tests will communicate with the emulator just as they would communicate with your Siglent device. The emulator can be started from within the test. There is no need to have it running separately. The emulator is started with just a few lines of Python:

```python
from siglent_emulator import emulator

PORT=21111
emulator.start(device="SDG1032X", port=PORT, daemon=True)
```

Pass the IP address and port of the emulator to your functions. Your code will behave just as if it was talking to a physical Siglent device. For instance, if you have a Python source file named `siglent_device` that has a class `Amplitude` you could write a test like this:

```python
  IP_ADDR="127.0.0.1"

  device = siglent_device.Amplitude()
  device.connect(ip_addr=IP_ADDR, port=PORT)
  device.set_amplitude(channel=1, amplitude=13.67)
  self.assertEqual(device.get_amplitude(channel=1), 13.67)
  device.close()
```

Look in the [tests/examples](tests/examples) directory for a fully working example that uses the Python unittest framework.

# Contributing to the Emulator

Pull requests are welcome!

## Testing the emulator

From the root directory of your checkout, type:

```shell
make all
```
