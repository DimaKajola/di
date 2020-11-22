from tests.snippets.baz import Baz
from tests.snippets.bar import Bar


class Foo:

    def __init__(self,
                 bar: Bar,
                 baz: Baz,
                 test_int: int = 3,
                 test_str: str = 'default string'):
        self.bar = bar
        self.baz = baz
        self.test_int = test_int
        self.test_str = test_str
