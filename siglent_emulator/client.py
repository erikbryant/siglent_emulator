"""Connect to the bs_emulator in commandline mode for debugging."""

# pylint: disable=unused-import,broad-except

import logging
import readline  # magically provides command history for input()
import socket
import sys
import time


def connect(ip_addr: str, port: int):
    """Connect to the emulator."""
    emulator = socket.socket()

    print("Waiting for connection")

    connected = False
    while not connected:
        try:
            emulator.connect((ip_addr, port))
            connected = True
        except socket.error as err:
            print(str(err))
            time.sleep(1)

    return emulator


def interactive(emulator: socket.socket) -> None:
    """Interactive session with the emulator."""
    while True:
        try:
            command = input("Siglent> ").strip().upper()
        except EOFError:
            break

        if command == "EXIT":
            break
        if command == "":
            continue

        try:
            tokens = command.split(" ")
            query = tokens[0].endswith("?")
            command += "\n"
            emulator.send(str.encode(command))
            # If this is a query wait for a response
            if query:
                response = ""
                while not response.endswith("\n"):
                    response += emulator.recv(2048).decode("utf-8")
                print(response)
        except Exception as err:
            errlog.exception(err)
            break


def main() -> None:
    """Do all the things."""
    # Set the logging configuration for all modules in this program
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(name)s:%(message)s",
        datefmt="%Y%m%dT%H%M%S%z",
        level=logging.INFO,
    )

    try:
        ip_addr = sys.argv[1]
        port = int(sys.argv[2])
    except Exception as err:
        errlog.exception(err)
        errlog.error("Usage: client ip_addr port")
        sys.exit(1)

    emulator = connect(ip_addr=ip_addr, port=port)

    print("Connected! For help, type: 'help?' or '?'. To exit, type 'exit'")

    interactive(emulator)

    emulator.close()


errlog = logging.getLogger(__name__)


if __name__ == "__main__":
    main()
