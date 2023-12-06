"""Set and get amplitude on a Siglent device."""

import socket


class Amplitude:
    sock: socket.socket

    def connect(self, ip_addr: str, port: int) -> None:
        """Open a socket connection."""
        self.sock = socket.create_connection((ip_addr, port), timeout=10.0)

    def close(self) -> None:
        """Close the socket connection."""
        self.sock.close()

    def format_command(self, cmd: str) -> bytes:
        """Format a command to send.
        Given a string, append a newline and convert the string to utf-8 bytes.
        """
        cmd += "\n"
        cmd_bytes = cmd.encode("utf-8")
        return cmd_bytes

    def write(self, cmd: str) -> None:
        """Write a command."""
        self.sock.sendall(self.format_command(cmd))

    def query(self, cmd: str = "") -> str:
        """Write cmd (if provided) and return the response."""
        self.write(cmd)
        return self.sock.recv(4096).decode("utf-8")

    def get_amplitude(self, channel: int) -> float:
        """Return amplitude in volts."""
        status = self.query("C" + str(channel) + ":BSWV?")
        index = status.find("AMP,")
        if index < 0:
            # The status was not what we expected it to be
            return -1
        status = status[index + 4 :]
        status = status.split(",")[0]
        # Strip the 'V' off
        status = status[:-1]
        result = float(status)
        return result

    def set_amplitude(self, channel: int, amplitude: float) -> None:
        """Set the channel amplitude in volts."""
        self.write(f"C{channel}:BSWV AMP,{amplitude}")
