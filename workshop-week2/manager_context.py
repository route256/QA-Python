from contextlib import contextmanager


class Indenter:

    def __init__(self):
        self.level = 0

    def __enter__(self):
        self.level += 4
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.level -= 4

    def print(self, text):
        print(f"{' ' * self.level}{text}")


with Indenter() as indenter:
    indenter.print('!Hello')
    with indenter:
        indenter.print("Привет!")
        with indenter:
            indenter.print("Bye!")
    indenter.print('Hello!')


@contextmanager
def my_context_manager(filename):
    f = open(filename)
    yield f
    f.close()

