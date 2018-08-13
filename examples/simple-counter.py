from ignito import System, Actor, message


class Messages:
    increment = message('increment', int)
    decrement = message('decrement', int)


def initial_state():
    return 0

counter = Actor("counter", initial_state, messages=Messages)


@counter.handle(Messages.increment)
def increment(self, message):
    self.state += message.value


@counter.handle(Messages.decrement)
def decrement(self, message):
    self.state -= message.value


def main():
    with System("main") as sys:
        addr = sys.spawn(counter)
        addr.call(Messages.increment(1))
        print "new state %d" % addr.get_state()
        assert addr.get_state() == 1, "Should have a state value of 1"

main()
