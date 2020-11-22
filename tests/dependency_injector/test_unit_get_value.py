from unittest import TestCase
from tests.snippets.bar import Bar
from di import DependenciesInjector, DIRegistry
import inspect


class SomeClass:

    def __init__(self, number: int, bar: Bar,
                 item, default: str = 'some default string'):
        self.number = number
        self.bar = bar
        self.default = default
        self.item = item


class TestDependenciesInjectorGetValue(TestCase):

    def setUp(self) -> None:
        self.di = DependenciesInjector(DIRegistry())
        self.class_signature = inspect.signature(SomeClass)

    def test_get_passed_value(self):
        passed_value = 'some string'
        res = self.di._get_value(self.class_signature.parameters['number'], passed_value, SomeClass)

        self.assertIs(res, passed_value)

    def test_get_default_value(self):
        parameter = self.class_signature.parameters['default']
        res = self.di._get_value(parameter, parameter.empty, SomeClass)

        self.assertIs(res, SomeClass(item=None, number=3, bar=Bar()).default)

    def test_recursive_load(self):
        parameter = self.class_signature.parameters['bar']
        res = self.di._get_value(parameter, parameter.empty, SomeClass)
        self.assertIsInstance(res, Bar)

    def test_no_annotation(self):
        with self.assertRaises(TypeError):
            self.di._get_value(self.class_signature.parameters['item'], None, SomeClass)
