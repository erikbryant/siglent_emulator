"""Emulate a Siglent lab device."""

# pylint: disable=broad-except


import logging
import socket
import sys
from _thread import start_new_thread
import threading

from emulator.function_generator import sdg1032x


class Emulator:
    """Emulate a lab device over a socket."""

    ThreadCount = 0
    func_gen = sdg1032x.SiglentDevice()

    def client_handler(self, connection: socket.socket) -> None:
        """Receive a command from the client, process, and respond."""
        while True:
            try:
                data = connection.recv(2048)
                message = data.decode("utf-8").strip().upper()
                if message == "":
                    continue
                # Sometimes messages com in so quickly they stack up
                # before we can get back around to read them.
                for msg in message.split("\n"):
                    result = self.func_gen.dispatch(msg)
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

    def start_server(self, port: int) -> None:
        """Start the server."""
        server_socket = self.bind(port=port)
        errlog.info("Server is listing on port %d...", port)
        server_socket.listen()

        while True:
            try:
                self.accept_connections(server_socket)
            except Exception as err:
                errlog.exception(err)
                break
        server_socket.close()


def start_emulator(port: int = 21111) -> None:
    """Start the emulator."""
    emulator = Emulator()
    emulator.start_server(port)


def start(port: int = 21111, daemon: bool = False) -> None:
    """Start the program (when invoked from code)."""
    if daemon:
        thread = threading.Thread(target=start, args=(port,))
        thread.daemon = True
        thread.start()
    else:
        start_emulator(port=port)


def main() -> None:
    """Start the program (when invoked from the command line)."""
    # Set the logging configuration for all modules in this program
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(name)s:%(message)s",
        datefmt="%Y%m%dT%H%M%S%z",
        level=logging.INFO,
    )

    port: int = 21111
    if len(sys.argv) == 2:
        try:
            port = int(sys.argv[1])
        except Exception as err:
            errlog.exception(err)
            errlog.error("Usage: emulator [port]")
            sys.exit(1)
    elif len(sys.argv) > 2:
        errlog.error("Too many arguments. Usage: emulator [port]")
        sys.exit(1)

    start(port=port)


errlog = logging.getLogger(__name__)

if __name__ == "__main__":
    main()
