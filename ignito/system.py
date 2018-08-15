import socket
import multiprocessing


class System:
    def __init__(self, name, known_nodes=[]):
        self.name = name
        self.known_nodes = known_nodes
        self.connections = []

    @property
    def address(self):
        if hasattr(self, '_listen_address'):
            return self._listen_address
        return None

    def connect_to_node(self, host):
        addr, port = ":".split(host)
        s = socket.socket()
        s.connect((addr, int(port)))
        self.connections.append()

    def listen_for_nodes(self):
        s = socket.socket()
        s.bind(('', 0))
        self._listen_address = s.getsockname()[1]
        while True:
            connection, _address = s.accept()
            self.connections.append(connection)

    def __enter__(self):
        for node in self.known_nodes:
            self.connect_to_node(node)

        self.listener = multiprocessing.Process(target=self.listen_for_nodes)
        self.listener.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("killing " + self.name)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    with System("main") as sys:
        with System("sys2", known_nodes=[sys.address]):
            import time
            while True:
                time.sleep(1)
