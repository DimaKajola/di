from unittest import TestCase
from di.dependency_injector import DependenciesInjector


class SomeClass:
    pass


class TestDependenciesInjectorTestCase(TestCase):

    def test_get_class_from_the_same_file(self):
        self.assertIs(DependenciesInjector.get_class('tests.test_di.SomeClass'), SomeClass)

    def test_get_class_dynamically_imported(self):
        class_obj = DependenciesInjector.get_class('tests.code.Bar')

        from tests.code.bar import Bar
        self.assertIs(class_obj, Bar)

