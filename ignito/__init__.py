
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

    def spawn(self, actor, *args):
        return Address(actor, self, self.registry.next_id())

    def __enter__(self):
        # make a database connection and return it
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # make sure the dbconnection gets closed
        line_width = len(self.name) + 29
        print '-' * line_width
        print "--- terminating %s's actors ---" % self.name
        print '-' * line_width


class Address:
    def __init__(self, actor, sys, key):
        self.actor = actor

    def call(self, message):
        self.actor.call(message)

    def get_state(self):
        return self.actor.state


class Actor:
    def __init__(self, name, state_func, messages=None):
        self.state = state_func()
        self.handlers = []

    def handle(self, pattern):
        def wrapper(fn):
            self.handlers.append((pattern, fn))
        return wrapper

    def call(self, message):
        for _type, handler in self.handlers:
            if isinstance(message, _type):
                handler(self, message)


class Message(object):
    def __init__(self, *args):
        for arg in args:
            setattr(self, 'value', arg)


# Message Factory
def message(name, *arg_types):
    return type(name, (Message,), {
        'types': arg_types
    })
