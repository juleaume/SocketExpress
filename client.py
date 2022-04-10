import socket
import threading
from typing import Iterable, Tuple, Union


class Client:
    def __init__(self, signal=None):
        self.socket = socket.socket()
        self._message = ""
        self.reading_thread = None
        self.signal = signal
        self._ip = ""
        self._port = 9898

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
            print("message", value)

    def start(self):
        self.reading_thread = threading.Thread(target=self._run)
        self.reading_thread.start()

    def send_message(self, message: str):
        try:
            self.socket.send(message.encode())
        except (socket.timeout, BrokenPipeError, ConnectionError):
            print("Warning no route to host")

    def _run(self):
        self.socket.connect(self.address)
        print("connected to server")
        while True:
            self.message = self.socket.recv(4096).decode()
            if self.signal is not None:
                self.signal.emit(self.message)
