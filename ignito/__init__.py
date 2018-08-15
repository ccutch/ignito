from multiprocessing import Pipe, Process as MProcess

# from eventlet import greenthread


class Registry:
    def __init__(self, sys):
        self.sys = sys
        self._next_id_counter = 0

    def next_id(self):
        self._next_id_counter += 1
        return self._next_id_counter


class System:
    def __init__(self, name):
        self.name = name
        self.registry = Registry(self)
        # self.pool = eventlet.GreenPool()

    def spawn(self, reducer, *args, **kwargs):
        process = Process(reducer, args, kwargs)
        print(process.lifecycle)
        p = MProcess(target=process.lifecycle)
        p.start()
        return Address(process, self, self.registry.next_id())

    def __enter__(self):
        # make a database connection and return it
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # make sure the dbconnection gets closed
        line_width = len(self.name) + 29
        print('-' * line_width)
        print("--- terminating {}'s actors ---".format(self.name))
        print('-' * line_width)


class Address:
    def __init__(self, process, sys, key):
        self.process = process

    def call(self, message):
        self.process.call(message)

    def get_state(self):
        return self.process.state


class Reducer:
    def __init__(self, name, state_func):
        self.state_func = state_func
        self.handlers = []

    def handle(self, pattern):
        def wrapper(fn):
            self.handlers.append((pattern, fn))
        return wrapper

    def call(self, state, message):
        for _type, handler in self.handlers:
            if isinstance(message, _type):
                handler(state, message)


def reducer():
    def decorator(fn):
        return Reducer(fn.__name__, fn)
    return decorator


class Process:
    def __init__(self, reducer, args, kwargs):
        self.state = reducer.state_func(*args, **kwargs)
        self.reducer = reducer
        self.pipe = Pipe()

    def call(self, message):
        self.pipe[1].send("calling message")
        # self.reducer.call(self, message)

    def lifecycle(self):
        print("waiting form messages")
        while True:
            internal_message = self.pipe[0].recv()
            print("message" + internal_message)


class Message(object):
    def __init__(self, *args):
        for arg in args:
            setattr(self, 'value', arg)


# Message Factory
def message(name, *arg_types):
    return type(name, (Message,), {
        'types': arg_types
    })
