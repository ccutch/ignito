from ignito import System, reducer, message


class Messages:
    increment = message('increment', int)
    decrement = message('decrement', int)


# def initial_state():
#     return 0
# counter1 = Reducer("counter", initial_state)
# counter2 = Reducer("counter", lambda: 0)

@reducer()
def counter():
    return 0


@counter.handle(Messages.increment)
def increment(self, message):
    self.state += message.value


@counter.handle(Messages.decrement)
def decrement(self, message):
    self.state -= message.value


def main():
    print(counter)
    with System("main") as sys:
        addr = sys.spawn(counter)
        addr.call(Messages.increment(1))
        # print("new state {}".format(addr.get_state()))
        # assert addr.get_state() == 1, "Should have a state value of 1"


main()
