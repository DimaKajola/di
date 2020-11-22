class Bar:

    def __init__(self, test_var: str = 'test'):
        self.test_var = test_var

    def test(self):
        return self.__class__.__name__
