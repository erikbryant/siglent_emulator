"""Emulate a Siglent test and measurement device."""

# pylint: disable=broad-except


import logging
import socket
import sys
from _thread import start_new_thread
import threading
from typing import Any

from siglent_emulator.function_generator import sdg1032x
from siglent_emulator.function_generator import sdg1062x

EMULATORS = {
    "sdg1032x": sdg1032x,
    "sdg1062x": sdg1062x,
}


class Emulator:
    """Emulate a Siglent test and measurement device over a socket."""

    device: Any

    def __init__(self, device: str) -> None:
        """Load the emulation code for this device."""
        self.device = EMULATORS[device.lower()].new()

    def client_handler(self, connection: socket.socket) -> None:
        """Receive a command from the client, process, and respond."""
        while True:
            try:
                data = connection.recv(2048)
                message = data.decode("utf-8").strip().upper()
                if message == "":
                    continue
                # Sometimes messages come in so quickly they stack up
                # before we can get back around to read them.
                for msg in message.split("\n"):
                    result = self.device.process(command=msg)
                    if result != "":
                        if not result.endswith("\n"):
                            result += "\n"
                        connection.sendall(str.encode(result))
            except (ConnectionResetError, BrokenPipeError):
                errlog.info("Client closed connection")
                break
        connection.close()

    def accept_connections(self, connection: socket.socket) -> None:
        """Accept a new connection from a client."""
        client, address = connection.accept()
        errlog.info("New connection from: %s:%s", address[0], address[1])
        start_new_thread(self.client_handler, (client,))

    def bind(self, ip_addr: str = "127.0.0.1", port: int = 21111) -> socket.socket:
        """Bind to a socket (retrying on failure). Return that socket."""
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind((ip_addr, port))
                break
            except Exception as err:
                if sock is not None:
                    sock.close()
                errlog.error("Failed to bind to %s:%s. Retrying...", ip_addr, port)
                errlog.exception(err)
        return sock

    def run(self, port: int) -> None:
        """Listen for incoming connections."""
        server_socket = self.bind(port=port)
        errlog.info("Server is listing on port %d...", port)
        server_socket.listen()

        while True:
            try:
                self.accept_connections(connection=server_socket)
            except Exception as err:
                errlog.exception(err)
                break
        server_socket.close()


def _run(device: str, port: int) -> None:
    """Run the emulator."""
    emulator = Emulator(device=device)
    emulator.run(port=port)


def start(device: str, port: int = 21111, daemon: bool = False) -> None:
    """Start the emulator inline or on a separate thread."""
    if daemon:
        thread = threading.Thread(target=_run, args=(device, port))
        thread.daemon = True
        thread.start()
    else:
        _run(device=device, port=port)


def main() -> None:
    """Start the emulator (when invoked from the command line)."""
    # Set the logging configuration for all modules in this program
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(name)s:%(message)s",
        datefmt="%Y%m%dT%H%M%S%z",
        level=logging.INFO,
    )

    if len(sys.argv) != 2:
        errlog.error("Usage: emulator device")
        sys.exit(1)

    start(port=21111, device=sys.argv[1])


errlog = logging.getLogger(__name__)

if __name__ == "__main__":
    main()
