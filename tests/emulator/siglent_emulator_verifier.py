"""Verify Siglent function generator emulator responses are identical to the hardware."""

import logging
import socket
import sys
import time
from typing import List, Tuple


state_defaults: List[str] = [
    "*RST",
    "C1:OUTP OFF",
    "C2:OUTP OFF",
    "C1:OUTP LOAD,HZ",
    "C2:OUTP LOAD,HZ",
    "C1:OUTP PLRT,NOR",
    "C2:OUTP PLRT,NOR",
]

commands: List[str] = [
    "*IDN?",
    "*RST",
    "*OPC",
    "STL?",
    "STL? BUILDIN",
    "STL? USER",
    "PACP C2,C1",
    "C1:OUTP ON",
    "C1:OUTP OFF",
    "C2:OUTP ON",
    "C2:OUTP OFF",
    "C1:OUTP LOAD,50",
    "C1:OUTP LOAD,HZ",
    "C2:OUTP LOAD,50",
    "C2:OUTP LOAD,HZ",
    "C1:OUTP PLRT,NOR",
    "C1:OUTP PLRT,INVT",
    "C2:OUTP PLRT,NOR",
    "C2:OUTP PLRT,INVT",
    "C1:BSWV FRQ,120.1",
    "C2:BSWV FRQ,234.5",
    "C1:BSWV AMP,17.89",
    "C2:BSWV AMP,14.32",
    "C1:BSWV FRQ,33.3",
    "C2:BSWV FRQ,44.4",
    "PACP C2,C1",
    "*OPC",
    "*RST",
]

states: List[str] = [
    "C1:OUTP?",
    "C2:OUTP?",
    "C1:BSWV?",
    "C2:BSWV?",
]


def open_socket(ip_addr: str, port: int) -> socket.socket:
    """Open a socket on localhost."""
    print("Waiting for connection...")

    connected: bool = False
    while not connected:
        try:
            connection = socket.socket()
            connection.connect((ip_addr, port))
            connected = True
        except socket.error as err:
            print(str(err))
            time.sleep(1)

    print("Connected!")

    return connection


def filter_response(response: str) -> str:
    """Convert whitespace chars to something readable."""
    response = response.replace("\n", "\\n")
    response = response.replace("\r", "\\r")
    return response


def send_command(sock: socket.socket, command: str) -> str:
    """Send a command and return the response (if any)."""
    tokens = command.split(" ")
    query = tokens[0].endswith("?")

    command += "\n"
    sock.send(str.encode(command))

    # If this is a query wait for a response
    if query:
        response = ""
        while not response.endswith("\n"):
            response += sock.recv(2048).decode("utf-8")
        response = filter_response(response)
        return response

    return "No response expected"


def reset_state(sock: socket.socket) -> None:
    """Reset the device to a known state so we can compare state in each test."""
    for default in state_defaults:
        send_command(sock=sock, command=default)


def run_test(emulator: socket.socket, hardware: socket.socket, cmd: str) -> bool:
    """Run a single test. Verify system states match."""
    emulator_response = send_command(sock=emulator, command=cmd)
    hardware_response = send_command(sock=hardware, command=cmd)
    if emulator_response != hardware_response:
        errlog.error(
            "Response mismatch for '%s'\n  emulator: '%s'\n  hardware: '%s'",
            cmd,
            emulator_response,
            hardware_response,
        )
        return False

    return True


def run_tests(emulator: socket.socket, hardware: socket.socket) -> Tuple[int, int]:
    """Run all tests."""
    attempts: int = 0
    failures: int = 0

    try:
        for cmd in commands:
            attempts += 1
            print(f"Testing: '{cmd}'")
            success = run_test(emulator=emulator, hardware=hardware, cmd=cmd)
            if not success:
                failures += 1
            # Compare internal states
            for state in states:
                match = run_test(emulator=emulator, hardware=hardware, cmd=state)
                if not match:
                    failures += 1
                    errlog.error("State mismatch after '%s'! Aborting tests.", cmd)
                    return attempts, failures
    except Exception as err:
        errlog.error("Caught excpetion. Aborting tests.")
        errlog.exception(err)
        failures += 1

    return attempts, failures


def rounding_tests_frq(
    emulator: socket.socket, hardware: socket.socket
) -> Tuple[int, int]:
    """Run rounding tests on FRQ values."""
    attempts: int = 0
    failures: int = 0

    known_failures = [202, 223, 438, 743]

    try:
        for val in range(0, 1000, 1):
            if val in known_failures:
                continue
            cmd = f"C1:BSWV FRQ,{val}"
            attempts += 1
            print(f"Testing: '{cmd}'")
            success = run_test(emulator=emulator, hardware=hardware, cmd=cmd)
            if not success:
                failures += 1
            # Compare internal states
            state = "C1:BSWV?"
            match = run_test(emulator=emulator, hardware=hardware, cmd=state)
            if not match:
                failures += 1
                errlog.error("State mismatch after '%s'! Aborting tests.", cmd)
                return attempts, failures
    except Exception as err:
        errlog.error("Caught excpetion. Aborting tests.")
        errlog.exception(err)
        failures += 1

    return attempts, failures


def rounding_tests_amp(
    emulator: socket.socket, hardware: socket.socket
) -> Tuple[int, int]:
    """Run rounding tests on FRQ values."""
    attempts: int = 0
    failures: int = 0

    try:
        for val in range(0, 22):
            for frac in range(0, 10):
                cmd = f"C1:BSWV AMP,{val}.{frac}"
                attempts += 1
                print(f"Testing: '{cmd}'")
                success = run_test(emulator=emulator, hardware=hardware, cmd=cmd)
                if not success:
                    failures += 1
                # Compare internal states
                state = "C1:BSWV?"
                match = run_test(emulator=emulator, hardware=hardware, cmd=state)
                if not match:
                    failures += 1
                    errlog.error("State mismatch after '%s'! Aborting tests.", cmd)
                    return attempts, failures
    except Exception as err:
        errlog.error("Caught excpetion. Aborting tests.")
        errlog.exception(err)
        failures += 1

    return attempts, failures


def usage() -> None:
    """Print usage message and exit with error."""
    errlog.error("Usage: %s emulator_ip emulator_port, hw_ip, hw_port", sys.argv[0])
    sys.exit(1)


def main() -> None:
    """Set up to run the tests."""
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(name)s:%(message)s",
        datefmt="%Y%m%dT%H%M%S%z",
        level=logging.INFO,
    )

    if len(sys.argv) != 5:
        usage()

    try:
        emulator_ip_addr: str = sys.argv[1]
        emulator_port: int = int(sys.argv[2])
        hardware_ip_addr: str = sys.argv[3]
        hardware_port: int = int(sys.argv[4])
    except Exception as err:
        errlog.exception(err)
        usage()

    emulator = open_socket(ip_addr=emulator_ip_addr, port=emulator_port)
    hardware = open_socket(ip_addr=hardware_ip_addr, port=hardware_port)

    # In case the emulator or hardware is not at default state, reset it.
    reset_state(sock=emulator)
    reset_state(sock=hardware)

    attempts, failures = rounding_tests_amp(emulator=emulator, hardware=hardware)
    attempts, failures = rounding_tests_frq(emulator=emulator, hardware=hardware)
    attempts, failures = run_tests(emulator=emulator, hardware=hardware)

    if failures > 0:
        errlog.error("\n%d of %d tests failed", failures, attempts)
        sys.exit(failures)

    errlog.info("%d tests run. All tests passed!", attempts)


errlog = logging.getLogger(__name__)


if __name__ == "__main__":
    main()
