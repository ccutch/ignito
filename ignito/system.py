import socket
import multiprocessing


class System:
    def __init__(self, name, master_node=None):
        self.name = name
        self.is_master = master_node is None
        self.master_node = master_node
        self.net_process = None

    def connect_to_master(self):
        pass

    def listen_for_nodes(self):
        s = socket.socket()
        s.bind(('', 0))
        print(s.getsockname()[1])

    def __enter__(self):
        if self.is_master:
            process = multiprocessing.Process(target=self.listen_for_nodes)
        else:
            process = multiprocessing.Process(target=self.connect_to_master)
        self.net_process = process
        self.net_process.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.net_process.kill()


with System("testing"):
    import time
    while True:
        time.sleep(1)
