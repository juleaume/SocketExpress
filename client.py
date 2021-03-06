import os
import socket
import threading
from typing import Tuple, Union


class Client:
    is_running = True

    def __init__(self, signal=None):
        self.socket = socket.socket()
        self._message = ""
        self.reading_thread = None
        self.signal = signal
        self._ip = ""
        self._port = 9898
        self._name = f"{os.getlogin()}@{socket.gethostname()}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value == self._name:
            self.send_message(f"<{self.name} is now {value}>\n")
            self._name = value

    @property
    def address(self):
        return self._ip, self._port

    @address.setter
    def address(self, value: Tuple[str, Union[str, int]]):
        ip, port = value
        if isinstance(ip, str):
            self._ip = ip
        if isinstance(port, int):
            self._port = port
        elif isinstance(port, str) and port.isdigit():
            self._port = int(port)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if value:
            self._message = value

    def start(self):
        self.reading_thread = threading.Thread(target=self._run, name="Client")
        self.reading_thread.start()

    def send_message(self, message: str):
        try:
            self.socket.send(message.encode())
        except (socket.timeout, BrokenPipeError, ConnectionError, OSError):
            print("Warning no route to host")

    def _run(self):
        try:
            self.socket.connect(self.address)
        except (socket.timeout, ConnectionError, OSError):
            print("Cannot connect to server")
            return
        print("connected to server")
        self.send_message(f"<{self.name} has entered the chat>\n")
        while self.is_running:
            self.message = self.socket.recv(4096).decode()
            if self.signal is not None:
                self.signal.emit(self.message)

    def __del__(self):
        self.send_message(f"<{self.name} has left the chat>\n")
