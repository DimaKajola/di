from unittest import TestCase
from di import di
import inspect


class SomeClass:

    def __init__(self, number: int, item, default: str = 'some default string'):
        self.number = number
        self.default = default
        self.item = item


class TestDependenciesInjectorGetValue(TestCase):

    def setUp(self) -> None:
        self.class_signature = inspect.signature(SomeClass)

    def test_get_passed_value(self):
        passed_value = 'some string'
        res = di._get_value(self.class_signature.parameters['number'], passed_value, SomeClass)

        self.assertIs(res, passed_value)

    def test_get_default_value(self):
        parameter = self.class_signature.parameters['default']
        res = di._get_value(parameter, parameter.empty, SomeClass)

        self.assertIs(res, SomeClass(item=None, number=3).default)

    def test_no_annotation(self):
        with self.assertRaises(TypeError):
            di._get_value(self.class_signature.parameters['item'], None, SomeClass)
